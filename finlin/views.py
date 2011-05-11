from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.renderers import get_renderer
from pyramid.renderers import render
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.traversal import resource_path
from pyramid.security import remember
from pyramid.security import forget

import datetime

import re
import cryptacular.bcrypt

import formencode
from formencode.schema import Schema
from formencode.validators import String, PlainText, MaxLength, MinLength, Email
from formencode.validators import Invalid, FancyValidator 
from formencode import variabledecode 
from formencode import htmlfill
from formencode.foreach import ForEach
from formencode.api import NoDefault

from markdown import markdown
from BeautifulSoup import BeautifulSoup, Tag

from finlin.models import Root
from finlin.models import Company
from finlin.models import User
from finlin.models import Comment

import logging
from pprint import pprint
log = logging.getLogger(__name__)

import locale
locale.setlocale(locale.LC_ALL, '')


#____________________________________________________________________Utilities

def slugify(name):
    filter = { 
        '&+' : 'and', # replace & with 'and'              
        '[^a-zA-Z0-9]+' : '_', # non-alphanumeric characters with a hyphen
        '-+' : '_' # replace multiple hyphens with a single hyphen
    }
    for k, v in filter.items():
        name = re.sub(k, v, name)
    name = name.strip('_') 
    return name	

   
#_____________________________________________________________________Homepage

@view_config(context=Root, renderer='finlin:templates/home_page.pt')
def home_page(context, request):
    main = get_renderer('finlin:templates/master.pt').implementation()
    return {'main': main} 


#______________________________________________________________________Company

class UniqueCompanyName(FancyValidator):
    def _to_python(self, value, state):
        result = state.db.company.find_one({'name':value})
        if result is not None:
            raise Invalid(
                'That company name already exists',
                 value, state)
        return value


class CompanyForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.All(String(not_empty=True), 
                          UniqueCompanyName()) 
    ticker = String()
    overview = String()
    competitive_advantage = String()
    growth_strategy = String()
 

@view_config(name='list', context=Root, renderer='templates/company_list.pt')
def list_company(context, request):
    main = get_renderer('finlin:templates/master.pt').implementation()
    return dict(main = main)    



#negative net income uses ()
def remove_parens(elem):
    if elem.find("(") is not -1:
        elem = elem.strip("()")
        elem = '-%s' % elem
    return elem

def make_usable(x):
    for key in x:
        x[key].reverse()
        if key == 'dates':
            x[key] = [datetime.datetime.strptime(elem, "%b %d, %Y") for elem in x[key]]
        elif key == 'rev':
            x[key] = [locale.atof(elem) for elem in x[key]] 
        elif key =='net':
            x[key] = [locale.atof(remove_parens(elem)) for elem in x[key] ]
    return x 

def percent_change(Vpresent, Vpast):
    percent = (Vpresent-Vpast)/Vpast*100
    percent = round(percent, 2)
    return percent

 
def change_quarterly(x):
    growth = {}
    for key in x:
        if key is not 'dates':
            first  = x[key][0]
            second = x[key][1]
            third  = x[key][2]
            fourth = x[key][3]

            yr_chg = percent_change(fourth, first)
            qtr_chg = percent_change(fourth, third) 
            growth[key] = {'qtr_chg': qtr_chg, 'yr_chg':yr_chg}
    return growth

@view_config(name='', context='finlin.models.Company', 
             renderer='templates/company_homepage.pt' )
def company_homepage(context, request):
    
    context.data['competitive_advantage'] = markdown(context.data['competitive_advantage'])
    context.data['growth_strategy'] = markdown(context.data['growth_strategy'])
    context.data['overview'] = markdown(context.data['overview'])

    #quarterly 
    q = {}
    q['dates'] = ['Dec 31, 2010', 'Sep 30, 2010', 'Jun 30, 2010', 'Mar 31, 2010']
    q['rev'] = ['36,585', '35,782', '36,027', '36,009']
    q['net'] = ['(4,066)', '(4,814)', '(1,646)', '(774)'] 
    #annually
    a = {}
    a['dates'] = ['Jun 30, 2010', 'Jun 30, 2009', 'Jun 30, 2008']
    a['rev'] = ['143,007', '136,827', '115,619']
    a['net'] = ['(3,969)', '(4,461)', '(18,882)']

    q = make_usable(q)

    q['exp'] = [i-j for i,j in zip(q['rev'], q['net'])]

    context.growth = change_quarterly(q)
    q['dates'] =  [datetime.datetime.strftime(elem, "%b %d, %Y") for elem in q['dates']]

    conv = locale.localeconv()  # get map of conventions
    locale.LC_MONETARY
    conv['frac_digits'] = 0
    conv['n_sign_posn'] = 0
    q['rev'] = [ locale.format("%s%.*f", (conv['currency_symbol'], conv['frac_digits'], elem), grouping=True) 
        for elem in q['rev'] ] 
    
    q['net'] = [locale.format("%s%.*f", (conv['currency_symbol'], conv['frac_digits'], elem), grouping=True) 
        for elem in q['net'] ]

    q['exp'] = [locale.format("%s%.*f", (conv['currency_symbol'], conv['frac_digits'], elem), grouping=True) 
        for elem in q['exp'] ]


    context.q = q

    return {
        'main': get_renderer('templates/master.pt').implementation(),
        'company_layout': get_renderer('templates/company_master.pt').implementation(),
        }



@view_config(name='', context='finlin.models.CompanyPage', 
             renderer='templates/company_page.pt' )
def view_page(context, request):
    try:
        context.page = markdown(context.page)
    except AttributeError: #is list
        management = {}
        for index, value in enumerate(context.page):
            management = markdown(value['bio'])
    return {
        'main': get_renderer('templates/master.pt').implementation(),
        'company_layout': get_renderer('templates/company_master.pt').implementation(),
        }


@view_config(name='add', context=Root)
def add_company(context, request):
    tpl = 'finlin:templates/company_form.pt'
    tpl_vars = { 
        'main': get_renderer('templates/master.pt').implementation(),
        'save_url': request.path_url,
        'submit_label': 'add company'} 

    if 'form.submitted' in request.params:
        schema = CompanyForm() 
        try:
            params = schema.to_python(request.params, request)
        except formencode.Invalid, e:
            html = htmlfill.render(
                                render(tpl, tpl_vars, request),
                                defaults=e.value,
                                errors=e.error_dict) 
            return Response(html)
        else:
            params['created'] = datetime.datetime.now()  
            params['slug']    = slugify(params['name'])
            request.db.company.save(params)
            request.session.flash(params['name'] + ' created')
            return HTTPFound(location = resource_url(
                                    context, 
                                    request, 
                                    params['name']))
    return Response(render(tpl, tpl_vars, request))


@view_config(name='edit', context=Company)
def edit_company(context, request):
    tpl = 'finlin:templates/company_form.pt'
    tpl_vars = { 
        'main': get_renderer('templates/master.pt').implementation(),
        'save_url': request.path_url,
        'submit_label': 'edit'} 
    if 'form.submitted' in request.params:
        schema = CompanyForm() 
        # look into below. If I take it out, it says the company name already exists
        schema.fields['name'] = String(not_empty=True)
        try:
            params = schema.to_python(request.params, request)
        except formencode.Invalid, e:
            htmlfilled = htmlfill.render(
                                render(tpl, tpl_vars, request),
                                defaults=e.value,
                                errors=e.error_dict) 
            return Response(htmlfilled)
        else:
            #need to use context bc the _id is already set
            data = {}
            for key, value in params.items():
                try:
                    #check to see if a value exists and if it has changed
                    original_value = context.data[key]
                    edited_value = params[key]
                    if original_value != edited_value:
                        data[key] = edited_value 
                except AttributeError:
                    #the value does not already exist, so set it
                    data[key] = value  

            request.db.company.update({'_id': context.data['_id']}, {'$set': data })
            request.session.flash(context.data['name'] + ' saved')
            return HTTPFound(location = resource_url(
                                            context.__parent__, 
                                            request, 
                                            context.__name__))
    html = htmlfill.render(
                      render(tpl, tpl_vars, request),
                      defaults=context.data)
    return Response(html)


@view_config(name='delete', context=Company)
def delete_company(context, request):
    request.db.company.remove({'slug':context.__name__})
    request.session.flash(context.name + ' deleted')
    return HTTPFound(location = resource_url(
                                    context.__parent__, 
                                    request, 
                                    'list'))


#__________________________________________________________Company Dashboard__
class CompanyDashboard(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    analysis = String()
 

#____________________________________________________________________Comment__

class CommentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.All(PlainText(not_empty=True),
                              MaxLength(50),
                              MinLength(2))
    email = formencode.All(Email(not_empty=True),
                              MaxLength(100),
                              MinLength(3))
    body = formencode.All(String(not_empty=True),
                              MaxLength(3000))


def comment_form(context, request):
    tpl = 'finlin:templates/comment_form.pt'
    tpl_vars = { 
        'save_url': resource_url(context, request, 'add_comment'),
        'submit_label': 'add comment'} 
    try:
        errors = request.session.pop('errors')
        values = request.session.pop('values')
        log.debug(errors)
        html = htmlfill.render(
                            render(tpl, tpl_vars, request),
                            defaults=values,
                            errors=errors) 
        return html
    except KeyError:
        return render(tpl, tpl_vars, request)


@view_config(name='add_comment', context=Company)
def add_comment(context, request):
    schema = CommentForm() 
    try:
        params = schema.to_python(request.params)
    except formencode.Invalid, e:
        request.session['errors'] = e.unpack_errors()
        request.session['values'] = e.value
        return HTTPFound(location = resource_url(context, request, anchor='comment-form'))
    else:
        comment = Comment(params, context)
        request.db.comment.insert(comment) 
        anchor = 'comment_' + str(comment['_id'])
        return HTTPFound(location = resource_url(context, request, anchor=anchor))




#___________________________________________________________________Register__

class UniqueUsername(formencode.FancyValidator):
    def _to_python(self, value, state):
        result = state.db.user.find_one({'username':value})
        if result is not None:
            raise formencode.Invalid(
                'That username already exists',
                 value, state)
        return value

class AddAccountForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.All(PlainText(not_empty=True),
                              MaxLength(50),
                              MinLength(3),
                              UniqueUsername())
    password = formencode.All(PlainText(not_empty=True),
                              MaxLength(50),
                              MinLength(3))

@view_config(name='add_account', context=Root)
def add_account(context, request):
    tpl = 'finlin:templates/login_form.pt'
    tpl_vars = { 
        'main': get_renderer('templates/master.pt').implementation(),
        'save_url': resource_url(context, request, self.__name__),
        'submit_label': 'create account'} 

    if 'form.submitted' in request.params:
        schema = CreateAccountForm() 
        try:
            params = schema.to_python(request.params, request)
        except formencode.Invalid, e:
            html = htmlfill.render(
                                render(tpl, tpl_vars, request),
                                defaults=e.value,
                                errors=e.error_dict) 
            return Response(html)
        else:
            params['created'] = datetime.datetime.now()
            params['password']= User.set_password(params['password']) 
            request.db.user.save(params)
            request.session.flash('Welcome ' + params['username'])
            return HTTPFound(location = request.application_url)
    return Response(render(tpl, tpl_vars, request))


#_____________________________________________________________________Login___

class Login(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.All(PlainText(not_empty=True))
    password = formencode.All(PlainText(not_empty=True))


@view_config(name='login', context=Root)
@view_config(context='pyramid.exceptions.Forbidden')
def login(context, request):
    login_url = resource_url(request.context, request, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)

    tpl = 'finlin:templates/login_form.pt'
    tpl_vars = { 
        'main': get_renderer('templates/master.pt').implementation(),
        'save_url': login_url,
        'came_from': came_from,
        'submit_label': 'Login'} 

    if 'form.submitted' in request.params:
        schema = LoginForm() 
        try:
            params = schema.to_python(request.params, request)
        except (formencode.Invalid), e:
            htmlfilled = htmlfill.render(   
                                   render(tpl, tpl_vars, request),
                                   defaults=e.value,
                                   errors=e.error_dict) 
            return Response(htmlfilled)
        try:
            doc = collection.find_one({'username':params['username']})
            if doc is None:
                raise Exception
            result = User.check_password(doc['password'], value)
            if result is False:
                raise Exception
        except (ValueError, TypeError, Exception): 
            htmlfilled = htmlfill.render(
                                render(tpl, tpl_vars, request),
                                defaults=params)
            message = ['The username or password you ',
                       'provided does not match our records.']
            request.session.flash(''.join(message))
            return Response(htmlfilled)
        else:
           headers = remember(request, username)
           return HTTPFound(location = came_from, headers = headers)
    return Response(render(tpl, tpl_vars, request))


#____________________________________________________________________Contact__


class ContactForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.All(PlainText(not_empty=True),
                              MaxLength(50),
                              MinLength(2))
    email = formencode.All(Email(not_empty=True),
                              MaxLength(100))
    body = formencode.All(String(not_empty=True),
                              MaxLength(3000))

@view_config(context='finlin.models.Root', name='contact')
def contact(context, request):
    tpl = 'finlin:templates/contact.pt'
    tpl_vars = { 
        'main': get_renderer('templates/master.pt').implementation(),
        'save_url': request.path_url,
        'submit_label': 'Send'} 

    if 'form.submitted' in request.params:
        schema = ContactForm() 
        try:
            params = schema.to_python(request.params, request)
        except formencode.Invalid, e:
            html = htmlfill.render(
                                render(tpl, tpl_vars, request),
                                defaults=e.value,
                                errors=e.error_dict) 
            return Response(html)
        else:
            import smtplib

            sender = params['email']
            receivers = ['bobby.chambers33@gmail.com']

            message = "name: %s ----"  % params['name']
            message += params['body']
            
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message)         
            request.session.flash('Thank you!')

            return HTTPFound(location = resource_url(
                                    context, 
                                    request,
                                    'contact'))
    return Response(render(tpl, tpl_vars, request))



#____________________________________________________________________Strategy_

@view_config(name='strategy', context='finlin.models.Root', 
             renderer='templates/strategy.pt')
def strategy(context, request):
    return { 'main': get_renderer('templates/master.pt').implementation() }
   

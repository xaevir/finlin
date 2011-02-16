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

import cryptacular.bcrypt

import formencode
from formencode import validators
from formencode import htmlfill

import markdown
from BeautifulSoup import BeautifulSoup, Tag

from finlin.models import Company
from finlin.models import User
from finlin.models import Comment

import logging
from pprint import pprint
log = logging.getLogger(__name__)

md = markdown.Markdown(
        extensions=['toc'], 
        safe_mode='remove',
)


class UniqueCompanyName(formencode.FancyValidator):
    def _to_python(self, value, state):
        result = state.db.company.find_one({'name':value})
        if result is not None:
            raise formencode.Invalid(
                'That company name already exists',
                 value, state)
        return value

class CompanyForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    analysis = validators.String(
        not_empty=True,
        messages={
            'empty':'Please enter some content for the page.'
        }
    )
    name = formencode.All(validators.String(not_empty=True), 
                             UniqueCompanyName()) 

@view_config(context='finlin.models.Root',
            renderer='finlin:templates/home_page.pt')
def home_page(context, request):
    main = get_renderer('templates/master.pt').implementation()
    return dict(main = main)    


@view_config(context='finlin.models.Root',
            name='list',
            renderer='finlin:templates/company_list.pt')
def list_company(context, request):
    main = get_renderer('finlin:templates/master.pt').implementation()
    return dict(main = main)    


class CommentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.All(validators.PlainText(not_empty=True),
                              validators.MaxLength(50),
                              validators.MinLength(2))
    email = formencode.All(validators.Email(not_empty=True),
                              validators.MaxLength(100),
                              validators.MinLength(3))
    body = formencode.All(validators.String(not_empty=True),
                              validators.MaxLength(3000))



@view_config(context='finlin.models.Company', name='')
def view_company(context, request):
    try:
        comment = request.session['errors']
        request.session['errors'] = None
    except:
        comment = comment_form(context, request) 

    whole_page = md.convert(context['analysis'])

    soup = BeautifulSoup(whole_page)
    toc = soup.find('div', 'toc')
    toc.extract()

    li_list = toc.findAll('li')
    li_list = reversed(li_list)

    beautiful = BeautifulSoup()
    ul = Tag(beautiful, "ul")
    beautiful.insert(0, ul)
    for li in li_list:
        ul.insert(0, li)

    toc = ul

    context['analysis'] = soup
    context['toc'] = toc
    return render_to_response('finlin:templates/company_view.pt',
            dict(
                main = get_renderer('templates/master.pt').implementation(),
                comment_form = comment,
               ),
               request)

def comment_form(context, request):
    tpl = 'finlin:templates/comment_form.pt'
    tpl_vars = { 
        'save_url': resource_url(context, request, 'add_comment'),
        'submit_label': 'add comment'} 
    return render(tpl, tpl_vars, request)


@view_config(context='finlin.models.Company', name='add_comment')
def add_comment(context, request):
    schema = CommentForm() 
    try:
        params = schema.to_python(request.params)
    except formencode.Invalid, e:
        html = htmlfill.render(
                            comment_form(context, request),
                            defaults=e.value,
                            errors=e.error_dict) 
        request.session['errors'] = html
        return HTTPFound(location = resource_url(context, request))
    else:
        comment = Comment(params, context)
        comment.save()
        return HTTPFound(location = resource_url(context, request))




@view_config(name='add', context='finlin.models.Root')
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
            company = Company(params)
            request.db.company.save(company)
            request.session.flash(company['name'] + ' created')
            return HTTPFound(location = resource_url(
                                    context, 
                                    request, 
                                    company.__name__))
    return Response(render(tpl, tpl_vars, request))


@view_config(name='edit', context='finlin.models.Company')
def edit_company(context, request):
    tpl = 'finlin:templates/company_form.pt'
    tpl_vars = { 
        'main': get_renderer('templates/master.pt').implementation(),
        'save_url': request.path_url,
        'submit_label': 'edit'} 
    if 'form.submitted' in request.params:
        schema = CompanyForm() 
        schema.fields['name'] = validators.String(not_empty=True)
        try:
            params = schema.to_python(request.params, request)
        except formencode.Invalid, e:
            htmlfilled = htmlfill.render(
                                render(tpl, tpl_vars, request),
                                defaults=e.value,
                                errors=e.error_dict) 
            return Response(htmlfilled)
        else:
            for key, value in params.items():
                context[key] = value
            request.db.company.save(context)
            request.session.flash(context['name'] + ' saved')
            return HTTPFound(location = resource_url(
                                            context.__parent__, 
                                            request, 
                                            context.__name__))
    html = htmlfill.render(
                      render(tpl, tpl_vars, request),
                      defaults=context,)
    return Response(html)


@view_config(name='delete', context='finlin.models.Company')
def delete_company(context, request):
    request.db.company.remove({'__name__':context.__name__})
    request.session.flash(context['name'] + ' deleted')
    return HTTPFound(location = resource_url(
                                    context.__parent__, 
                                    request, 
                                    'list'))


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
    username = formencode.All(validators.PlainText(not_empty=True),
                              validators.MaxLength(50),
                              validators.MinLength(3),
                              UniqueUsername())
    password = formencode.All(validators.PlainText(not_empty=True),
                              validators.MaxLength(50),
                              validators.MinLength(3))

@view_config(name='add_account', context='finlin.models.Root')
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


class Login(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.All(validators.PlainText(not_empty=True))
    password = formencode.All(validators.PlainText(not_empty=True))
 
@view_config(context='finlin.models.Root', name='login')
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




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
from finlin.models import Cms

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
    tpl = 'finlin:templates/comment/form.pt'
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
        'main': get_renderer('finlin:templates/master.pt').implementation(),
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
        'main': get_renderer('finlin:templates/master.pt').implementation(),
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
        'main': get_renderer('finlin:templates/master.pt').implementation(),
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
             renderer='finlin:templates/strategy.pt')
def strategy(context, request):
    return { 'main': get_renderer('finlin:templates/master.pt').implementation() }
   

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


import formencode
from formencode import validators
from formencode import htmlfill
from docutils.core import publish_parts

from finlin.models import Company
from finlin.models import User
import logging
log = logging.getLogger(__name__)

class CompanyForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    analysis = validators.String(
        not_empty=True,
        messages={
            'empty':'Please enter some content for the page.'
        }
    )
    name = validators.String(not_empty=True)


@view_config(context='finlin.models.Root',
            renderer='finlin:templates/home_page.pt')
def home_page(context, request):
    log.debug('viewing the homepage')
    main = get_renderer('templates/master.pt').implementation()
    return dict(main = main)    


@view_config(context='finlin.models.Root',
            name='list_company',
            renderer='finlin:templates/list_company.pt')
def list_company(context, request):
    main = get_renderer('finlin:templates/master.pt').implementation()
    return dict(main = main)    


@view_config(context='finlin.models.Company',
            renderer='finlin:templates/show_company.pt')
def show_company(context, request):
    main = get_renderer('templates/master.pt').implementation()
    edit_url = resource_url(context, request, 'edit_company')
    context.analysis = publish_parts(context.analysis, writer_name='html')['html_body']
    return dict(main = main)    


@view_config(name='new_company', context='finlin.models.Root')
def new_company(context, request):
    main = get_renderer('templates/master.pt').implementation()
    save_url = resource_url(context, request, 'new_company')
    def render_page():
        return render('finlin:templates/company_form.pt',
                      {'main':main, 'save_url':save_url}, 
                      request=request)
    if 'form.submitted' in request.params:
        schema = CompanyForm() 
        try:
            form = schema.to_python(request.params)
        except formencode.Invalid, e:
            html = htmlfill.render(
                                render_page(),
                                defaults=e.value,
                                errors=e.error_dict) 
            return Response(html)
        else:
            company = Company(form)
            request.db.company.save(company.__dict__)
            request.session.flash(company.name + ' created')
            return HTTPFound(location = resource_url(
                                    context, 
                                    request, 
                                    company.__name__))
    return Response(render_page())



@view_config(name='edit_company', context='finlin.models.Company')
def edit_company(context, request):
    main = get_renderer('templates/master.pt').implementation()
    save_url = resource_url(context, request, 'edit_company')
    def render_page():
        return render('finlin:templates/company_form.pt',
                      {'main':main, 'save_url':save_url}, 
                      request=request)
    if 'form.submitted' in request.params:
        schema = CompanyForm() 
        try:
            form = schema.to_python(request.params)
        except formencode.Invalid, e:
            html = htmlfill.render(
                                render_page(),
                                defaults=e.value,
                                errors=e.error_dict) 
            return Response(html)
        else:
            log.debug('not getting thru')
            company = Company(form)
            request.db.company.save(company.__dict__)
            request.session.flash(company.name + ' saved')
            return HTTPFound(location = resource_url(
                                    context.__parent__, 
                                    request, 
                                    company.__name__))
    html = htmlfill.render(
                        render_page(),
                        defaults=context.__dict__) 
    return Response(html)


@view_config(name='delete_company', context='finlin.models.Company')
def delete_company(context, request):
    request.db.company.remove({'__name__':context.__name__})
    request.session.flash(context.name + ' deleted')
    return HTTPFound(location = resource_url(
                                    context.__parent__, 
                                    request, 
                                    'list_company'))


class UniqueUsername(formencode.FancyValidator):
    def _to_python(self, value, state):
        result = state.db.user.find_one({'username':value})
        if result is not None:
            raise formencode.Invalid(
                'That username already exists',
                 value, state)
        return value

class CreateAccountForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.All(validators.PlainText(not_empty=True),
                              validators.MaxLength(50),
                              validators.MinLength(3),
                              UniqueUsername())
    password = formencode.All(validators.PlainText(not_empty=True),
                              validators.MaxLength(50),
                              validators.MinLength(3))

@view_config(name='create_account', context='finlin.models.Root')
def create_account(context, request):
    main = get_renderer('templates/master.pt').implementation()
    save_url = resource_url(context, request, 'create_account')
    def render_page():
        return render('finlin:templates/login_form.pt',
                      {'main':main, 'save_url':save_url, 
                       'submit_label': 'Create Account'}, 
                      request=request)
    if 'form.submitted' in request.params:
        schema = CreateAccountForm() 
        try:
            form = schema.to_python(request.params, request)
        except formencode.Invalid, e:
            html = htmlfill.render(
                                render_page(),
                                defaults=e.value,
                                errors=e.error_dict) 
            return Response(html)
        else:
            user = User(form)
            request.db.user.save(user.__dict__)
            request.session.flash('Welcome ' + user.username)
            log.debug('request application: ' + request.application_url)
            return HTTPFound(location = request.application_url)
    return Response(render_page())


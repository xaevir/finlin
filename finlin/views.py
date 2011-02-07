from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.renderers import get_renderer
from pyramid.renderers import render
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.traversal import resource_path
import formencode
from formencode import htmlfill
from docutils.core import publish_parts

from finlin.models import Company
import logging
log = logging.getLogger(__name__)

class CompanyForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    analysis = formencode.validators.String(
        not_empty=True,
        messages={
            'empty':'Please enter some content for the page.'
        }
    )
    title = formencode.validators.String(not_empty=True)


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
    log.debug('context.names:')
    log.debug(context.names)
    return dict(main = main)    


@view_config(context='finlin.models.Company',
            renderer='finlin:templates/show_company.pt')
def show_company(context, request):
    log.debug('got to view!')
    main = get_renderer('templates/master.pt').implementation()
    edit_url = resource_url(context, request, 'edit_company')
    context.analysis = publish_parts(context.analysis, writer_name='html')['html_body']
    return dict(main = main)    

@view_config(name='new_company', 
            context='finlin.models.Root',
            renderer='finlin:templates/company_form.pt')
def new_company(context, request):
    main = get_renderer('templates/master.pt').implementation()
    save_url = resource_url(context, request, 'create_company')
    return dict(save_url = save_url, main = main)    


@view_config(name='create_company', 
            context='finlin.models.Root')
def create_company(context, request):
        schema = CompanyForm() 
        try:
            form = schema.to_python(request.params)
            company = Company(form)
            request.db.company.save(company.__dict__)
            request.session.flash(company.title + ' saved')
            return HTTPFound(location = resource_url(context, request, company.__name__ ))
        except formencode.Invalid, error:
            result = new_company(context, request)
            htmlfilled = htmlfill.render(
                result.body,
                defaults=error.value,
                errors=error.error
            ) 
            return Response(htmlfilled)


@view_config(name='edit_company', 
            context='finlin.models.Company',
            renderer='finlin:templates/company_form.pt')
def edit_company(context, request):
    main = get_renderer('templates/master.pt').implementation()
    save_url = resource_url(context, request, 'update_company')
    html = render('finlin:templates/company_form.pt', 
                    {'main':main, 'save_url':save_url}, 
                    request=request)
    htmlfilled = htmlfill.render(
            html,
            defaults=context.__dict__
        ) 
    return Response(htmlfilled)

@view_config(name='update_company', 
            context='finlin.models.Company',
            renderer='finlin:templates/company_form.pt')
def update_company(context, request):
        schema = CompanyForm() 
        try:
            form = schema.to_python(request.params)
            company = Company(form)
            request.db.company.save(company.__dict__)
            request.session.flash(company.title + ' saved')
            return HTTPFound(location = resource_url(
                                    context.__parent__, 
                                    request, 
                                    company.__name__))
        except formencode.Invalid, error:
            result = edit_company(context, request)
            htmlfilled = htmlfill.render(
                result.body,
                defaults=error.value,
                errors=error.error
            ) 
            return Response(htmlfilled)


@view_config(name='delete_company', 
            context='finlin.models.Company',
            renderer='finlin:templates/company_form.pt')
def delete_company(context, request):
    request.db.company.remove({'__name__':context.__name__})
    request.session.flash(context.title + ' deleted')
    return HTTPFound(location = resource_url(
                                    context.__parent__, 
                                    request, 
                                    'list_company'))
 

from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.renderers import get_renderer
from pyramid.renderers import render
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

import formencode
from formencode import htmlfill

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

@view_config(context='finlin.models.Company',
            renderer='finlin:templates/show_company.pt')
def show_company(context, request):
    log.debug('got to view!')
    main = get_renderer('templates/master.pt').implementation()
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
            return HTTPFound(location = resource_url(company, request, 'show_company', company.__name__ ))
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


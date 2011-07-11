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

import formencode
from formencode.schema import Schema
from formencode.validators import String, PlainText, MaxLength, MinLength, Email
from formencode.validators import Invalid, FancyValidator 
from formencode import variabledecode 
from formencode import htmlfill
from formencode.foreach import ForEach
from formencode.api import NoDefault

from markdown import markdown

from finlin.models import Root
from finlin.models import Company

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
    name = formencode.All(String(not_empty=True), UniqueCompanyName()) 
    ticker = String()
    website = String()
    description = String()
    significant_developments = String()
    business_strategy = String()
    competition = String()
    questions = String()
    street = String()
    street2 = String()
    city = String()
    state = String()
    zip = String()
 

@view_config(name='list', context=Root, renderer='finlin:templates/company/list.pt')
def list_company(context, request):
    return {}    


@view_config(name='', context='finlin.models.Company', 
             renderer='finlin:templates/company/homepage.pt' )
def company_homepage(context, request):
    context.data['description'] = markdown(context.data['description'])
    context.data['significant_developments'] = markdown(context.data['significant_developments'])
    context.data['business_strategy'] = markdown(context.data['business_strategy'])
    context.data['competition'] = markdown(context.data['competition'])
    context.data['questions'] = markdown(context.data['questions'])
    return {'hd': header_view(request)}


@view_config(name='', context='finlin.models.CompanyPage', 
             renderer='finlin:templates/company/page.pt' )
def view_page(context, request):
    context.page = markdown(context.page)
    return {'hd': header_view(request)}


def header_view(request):
    return render('finlin:templates/company/hd.pt', '', request)

def editing_nav_view(request):
    return render('finlin:templates/company/editing_nav.pt', '', request)

@view_config(name='add', context=Root)
def add_company(context, request):
    tpl = 'finlin:templates/company/form.pt'
    tpl_vars = {
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
            params['slug'] = slugify(params['name'])
            request.db.company.save(params)
            request.session.flash(params['name'] + ' created')
            return HTTPFound(location = resource_url(
                                    context,
                                    request,
                                    params['name']))
    return Response(render(tpl, tpl_vars, request))


@view_config(name='edit', context=Company)
def edit_company(context, request):
    tpl = 'finlin:templates/company/form.pt'
    tpl_vars = {
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
                except KeyError:
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

   

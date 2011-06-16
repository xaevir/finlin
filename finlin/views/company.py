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
    competitive_advantage_summary = String()
    growth_strategy = String()
    growth_strategy_summary = String()
 

@view_config(name='list', context=Root, renderer='finlin:templates/company/list.pt')
def list_company(context, request):
    main = get_renderer('finlin:templates/master.pt').implementation()
    return dict(main = main)    


@view_config(name='', context='finlin.models.Company', 
             renderer='finlin:templates/company/homepage.pt' )
def company_homepage(context, request):
    context.data['competitive_advantage_summary'] = markdown(context.data['competitive_advantage_summary'])
    context.data['growth_strategy_summary'] = markdown(context.data['growth_strategy_summary'])
    context.data['overview'] = markdown(context.data['overview'])
    return {'hd': header_view(request)}


@view_config(name='', context='finlin.models.CompanyPage', 
             renderer='finlin:templates/company/page.pt' )
def view_page(context, request):
    context.page = markdown(context.page)
    return {'hd': header_view(request)}


def header_view(request):
    return render('finlin:templates/company/hd.pt', '', request)

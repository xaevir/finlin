from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.renderers import get_renderer
from pyramid.renderers import render
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.traversal import resource_path

import datetime

import formencode
from formencode.schema import Schema
from formencode.validators import String, PlainText, MaxLength, MinLength, Email
from formencode.validators import Invalid, FancyValidator 
from formencode import variabledecode 
from formencode import htmlfill
from formencode.foreach import ForEach
from formencode.api import NoDefault

from finlin.models import Cms

import logging
from pprint import pprint
log = logging.getLogger(__name__)



@view_config(context=Cms, renderer='finlin:templates/cms/home.pt')
def home_page(context, request):
    return {} 


@view_config(context='finlin.models.QuestionsIndex', renderer='finlin:templates/cms/questions/list.pt')
def list(context, request):
    return {}


class QuestionForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    question = String()


@view_config(name='add', context='finlin.models.QuestionsIndex')
def add_question(context, request):
    tpl = 'finlin:templates/cms/questions/form.pt'
    tpl_vars = { 
        'save_url': request.path_url}

    if 'form.submitted' in request.params:
        schema = QuestionForm() 
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
            request.db.questions.insert(params)
            request.session.flash('Question created')
            return HTTPFound(location = resource_url(
                                    context, 
                                    request))
    return Response(render(tpl, tpl_vars, request))


@view_config(name='edit', context='finlin.models.Question')
def edit_question(context, request):
    tpl = 'finlin:templates/cms/questions/form.pt'
    tpl_vars = { 
        'save_url': request.path_url,
        } 
    if 'form.submitted' in request.params:
        schema = QuestionForm() 
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

            request.db.questions.update({'_id': context.data['_id']}, {'$set': data })
            request.session.flash('Question saved')
            return HTTPFound(location = resource_url(
                                            context.__parent__, 
                                            request))
    html = htmlfill.render(
                      render(tpl, tpl_vars, request),
                      defaults=context.data)
    return Response(html)


@view_config(name='delete', context='finlin.models.Question')
def delete_company(context, request):
    request.db.questions.remove({'_id': context.data['_id']})
    request.session.flash('Question deleted')
    return HTTPFound(location = resource_url(
                                    context.__parent__, 
                                    request))



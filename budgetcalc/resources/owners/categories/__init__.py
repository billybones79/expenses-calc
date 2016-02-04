import budgetcalc.resources.owners
import categories
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

#let's init our blueprint
categories_blueprint = Blueprint('categories', __name__,
                        template_folder='templates', url_prefix="/<owner>/categories")
categories_view = categories.CategoriesViews.as_view('categories', static_folder='static')
    
categories_blueprint.add_url_rule('/',view_func=categories_view, methods=['GET'])
categories_blueprint.add_url_rule('/', view_func=categories_view, methods=['POST'])
categories_blueprint.add_url_rule('/<ObjectId:id>/', view_func=categories_view, methods=['PUT', 'DELETE'])


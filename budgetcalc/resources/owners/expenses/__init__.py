from budgetcalc.resources.owners import  get_owner
import budgetcalc
import expenses
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

#let's init our blueprint
expenses_blueprint = Blueprint('expenses', __name__,
                        template_folder='templates', url_prefix="/<owner>/expenses", static_folder='static')
expenses_view = expenses.ExpensesViews.as_view('expenses')

    
expenses_blueprint.add_url_rule('/',view_func=expenses_view, methods=['GET'])
expenses_blueprint.add_url_rule('/', view_func=expenses_view, methods=['POST'])
expenses_blueprint.add_url_rule('/<ObjectId:id>/', view_func=expenses_view, methods=['PUT', 'DELETE'])
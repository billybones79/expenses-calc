from budgetcalc.resources.owners import  get_owner
import budgetcalc
import budgetcalc.resources.owners.expenses as expenses
import graphs
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

#let's init our blueprint
graphs_blueprint = Blueprint('graphs', __name__,
                        template_folder='templates', url_prefix="/<owner>/", static_folder='static')
graphs_view = graphs.GraphsViews.as_view('graphs')

graphs_blueprint.add_url_rule('charts/', view_func=graphs.GraphsViews.as_view(
    'graphs', template_name='graphs/graphs.html'), methods=['GET', 'POST'])

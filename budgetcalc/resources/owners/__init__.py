
import owners
from flask import Blueprint, render_template, abort, g, jsonify
from jinja2 import TemplateNotFound
import budgetcalc
import flask.ext.login as flask_login






# add before child request to insure that the correct owner is logged in and exists
def get_owner(f):    
    def decorator(*args, **kwargs):
        budgetcalc.app.logger.debug(kwargs)
        g.owner=budgetcalc.db.Owner.find_one({"name" : kwargs["owner"]})
        
        if g.owner == None :
            return  jsonify(messages = "L'utilisateur n'existe pas")
        if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == kwargs["owner"]):
            return flask_login.current_app.login_manager.unauthorized()
        return f(*args, **kwargs)
    return decorator

owners_blueprint = Blueprint('owners', __name__,
                        template_folder='templates', static_folder='static')
owners_view = owners.OwnersViews.as_view('owners')

owners_blueprint.add_url_rule('/',view_func=owners_view, defaults={'name': None}, methods=['GET'])
owners_blueprint.add_url_rule('/', view_func=owners_view, methods=['POST'])
owners_blueprint.add_url_rule('/<name>',view_func=owners_view, methods=['GET'])
owners_blueprint.add_url_rule('/<name>', view_func=owners_view, methods=['PUT', 'DELETE'])
owners_blueprint.add_url_rule('/login', view_func=owners.LoginView.as_view('login'), methods=['GET', 'POST'])



    
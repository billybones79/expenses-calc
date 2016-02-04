from flask import Flask, request, session, g, redirect, url_for, abort,jsonify, \
     render_template, flash
     

from flask.ext.mongokit import MongoKit, Document

from resources.owners import  owners_blueprint
from resources.owners.expenses  import expenses_blueprint 
from resources.owners.categories  import categories_blueprint
from resources.owners.graphs  import graphs_blueprint

from resources.owners.owners import  Owner
from resources.owners.expenses.expenses  import Expense 
from resources.owners.categories.categories  import Category   

from flask.ext.bcrypt import Bcrypt

import flask.ext.login as flask_login
import os

  


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.debug = True

#login and bcrypt information
bcrypt = Bcrypt(app)


login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(name):
    owner=db.Owner.find_one({"name" : name})
    if owner == None :
        return
    user = User()
    user.id = name
    return user


@login_manager.request_loader
def request_loader(request):
    name = request.form.get('name')
    if name == None :
        return
    owner=db.Owner.query.filter(Owner.name == name).first()
    if owner == None :
        return
    user = User()
    user.id = name

    user.is_authenticated = bcrypt.check_password_hash(owner["password"], request.form['password'] )

    return user

login_manager.login_view = "owners.login"
          
db = MongoKit(app)
db.register([Owner])
db.register([Expense])
db.register([Category])
    
app.register_blueprint(owners_blueprint, url_prefix='')
app.register_blueprint(expenses_blueprint)
app.register_blueprint(categories_blueprint)
app.register_blueprint(graphs_blueprint)


if __name__ == '__main__':
    # configuration 
    app.run()

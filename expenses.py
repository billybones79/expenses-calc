from flask import Flask, request, session, g, redirect, url_for, abort,jsonify, \
     render_template, flash
     

from flask.ext.mongokit import MongoKit, Document
     
import flask.ext.login as flask_login
from bson.json_util import dumps
from flask.ext.bcrypt import Bcrypt
  
import json  
import datetime
import logging
import time
import os
import bson



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.debug = True


bcrypt = Bcrypt(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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
    owner=Owner.query.filter(Owner.name == name).first()
    if owner == None :
        return
    user = User()
    user.id = name

    user.is_authenticated = bcrypt.check_password_hash(owner["password"], request.form['password'] )

    return user
    
class Owner(Document):
    __collection__ = 'owners'
    structure = {
        'name': unicode,
        'password': unicode
    }

class Category(Document): 
    __collection__ = 'categories'   
    structure = {
        'name': unicode,
        'color':unicode,
        'owner':unicode
    } 
 
class Expense(Document):
    __collection__ = 'expenses'
    structure = {
        'cost': float,
        'description':unicode,
        'date': datetime.datetime,
        'category': unicode,
        'owner': unicode
    }  
          
db = MongoKit(app)
db.register([Owner])
db.register([Expense])
db.register([Category])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')

    name = request.form['name']
    owner=db.Owner.find_one({"name" : name})
    if owner == None :
        return 'Bad login'
    if bcrypt.check_password_hash(owner["password"], request.form['password'] ):
        owner = User()
        owner.id = name
        flask_login.login_user(owner)
        return redirect(url_for('index_expenses', name=name))

    return 'Bad login'

@app.route('/')
def index_users():
    return render_template('users/index.html')

     
@app.route('/<name>')
def owner(name):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    return redirect(url_for('index_expenses', name=name))

@app.route('/<name>/categories', methods=['GET', 'POST'])
def index_categories(name):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    app.logger.debug(request)
    if request.mimetype != "application/json":
        return render_template('users/categories/index.html', name=name)
    owner=db.Owner.find_one({"name" : name})
    cat = db.Category.find({"owner":owner["name"]})
    return dumps( { "owner" :owner, 
                    "categories" : cat                              
                              })
@app.route('/<name>/expenses', methods=['GET', 'POST'])
def index_expenses(name):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()()
    app.logger.debug(request)
    if request.mimetype != "application/json":
        return render_template('users/expenses/index.html', name=name)
    owner=db.Owner.find_one({"name" : name})
    app.logger.debug(owner);
    cat = db.Category.find({"owner":owner["name"]})
    expenses =  db.Expense.find({"owner":owner["name"]})
    return dumps({ "owner" : owner, 
                  "categories" : cat,
                   "expenses" : expenses
                 })

# routes de json
@app.route('/owners', methods=['GET'])
def all_owners():
    app.logger.debug(db.Owner.find());
    return  dumps({"owners":db.Owner.find()})
@app.route('/owner', methods=['POST'])
def add_owner():
    owner = db.Owner()
    owner['name']=request.json['name']
    owner['password']=unicode(bcrypt.generate_password_hash(request.json['password']))
    owner.save()
    return  dumps({ "owner": owner})
#@app.route('/owner/<id>', methods=['DELETE'])
#def delete_owner(id):
#    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
#        return flask_login.current_app.login_manager.unauthorized()
#    g.couch.delete(Owner.load(id))
#    return  ""
@app.route('/<name>/categories/<ObjectId:id>', methods=['DELETE'])
def delete_category(name, id):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    db.Category.get_from_id(id).delete()
    return  ""
@app.route('/<name>/expenses/<ObjectId:id>', methods=['DELETE'])
def delete_expense(name, id):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    db.Expense.get_from_id(id).delete()
    return  ""
@app.route('/<name>/category', methods=['POST'])
def add_category(name):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    owner=db.Owner.find_one({"name" : name})
    if owner :
         category = db.Category()
         category["name"]=request.json['name']
         category["color"]=request.json['color']
         category["owner"]=owner["name"]
         category.save()
         return  dumps({"category":category})   
    return  jsonify(messages = "L'utilisateur n'existe pas")

@app.route('/<name>/expense', methods=['POST'])
def add_expense(name):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    owner=db.Owner.find_one({"name" : name})
    if owner == None :
        return  jsonify(messages = "L'utilisateur n'existe pas")
    
    cat = db.Category.find_one({"owner": owner["name"]})
    if cat == None :
        return  jsonify(messages = "La categorie n'existe pas")

    expense = db.Expense()
    expense["date"]=datetime.datetime.strptime(request.json['date'],"%Y/%m/%d")
    expense["cost"]=float(request.json['cost'])
    expense["description"]=request.json['description']
    expense['category']=cat["name"]
    expense['owner']=owner["name"]
    expense.save()
    return  dumps({"expense":expense})   
    

if __name__ == '__main__':
    # configuration 
    app.run()

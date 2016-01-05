from flask import Flask, request, session, g, redirect, url_for, abort,jsonify, \
     render_template, flash
     
from couchdb.design import ViewDefinition
from flaskext.couchdb import Document, TextField,CouchDBManager,ViewField,DictField,ListField,Mapping,FloatField,DateField,Row
import flask.ext.login as flask_login
from flask.ext.bcrypt import Bcrypt
  
import json  
import datetime
import logging
import time



app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
"""
CouchDB permanent view
"""

def viewDefToDict(View) : 
    d = []
    for row in View.rows :
      d.append(dict(row.items()))  
      
    return d

def init_db(app):
    """Creates the database views."""
    manager = CouchDBManager()
     # Install the views
    
    manager.setup(app)
    manager.add_viewdef(Owner.all)
    manager.add_viewdef(Category.categories_by_owner)
    manager.add_document(Owner)
    manager.add_document(Category)
    manager.add_document(Expense)
    manager.sync(app)
    
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(name):
    owner = Owner.all[name]
    if owner.rows == [] :
        return
    user = User()
    user.id = name
    return user


@login_manager.request_loader
def request_loader(request):
    name = request.form.get('name')
    owner = Owner.all[name]
    if owner.rows == [] :
        return
    owner=owner.rows[0]
    user = User()
    user.id = name

    user.is_authenticated = bcrypt.check_password_hash(owner["password"], request.form['password'] )

    return user
    
class Owner(Document):
    doc_type = 'owner'
    name = TextField()
    password = TextField()
    all = ViewField('owners', '''function(doc) { if (doc.doc_type == 'owner') {emit(doc.name, doc);}}''')

class Category(Document):  
    doc_type = 'category'
    name=TextField()
    color=TextField()
    owner=TextField()
    
    categories_by_owner = ViewField('categories', '''function(doc) { if (doc.doc_type == 'category') { emit([doc.owner, doc.name], doc);}}''')
    
class Expense(Document):
    doc_type = 'expense'
    cost=FloatField()
    description=TextField()
    date=DateField()
    category=TextField()
    owner=TextField()
    
    expenses_by_owner = ViewField('expenses', '''function(doc) { 
        if (doc.doc_type == 'expense') {emit(doc.owner,doc);}
        }''')
    expenses_by_category = ViewField('expenses', '''function(doc) { 
        if (doc.doc_type == 'expense') {emit(doc.category,doc);}
        }''')
    cost_by_category_by_month = ViewField('expenses', '''
    function(doc) {
        if (doc.doc_type == 'expense') {
            emit({owner : doc.owner, category : doc.category,year: doc.date.getFullYear(), month : doc.time.getMonth()},doc.cost);
        }
     }''',
     '''function (keys, values, rereduce) {return sum(values);}''',
     wrapper=Row, group=True)

    cost_by_category = ViewField('expenses', 
    '''function(doc) { if (doc.doc_type == 'expense') {emit({owner : doc.owner, category : doc.category},doc.cost);}}''',
     '''function (keys, values, rereduce) {return sum(values);}''',
      wrapper=Row, group=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')

    name = request.form['name']
    owner = Owner.all[name]
    if owner.rows == [] :
        return 'Bad login'
    owner=owner.rows[0]
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
    owner=viewDefToDict(Owner.all[name])
    cat = viewDefToDict(Category.categories_by_owner[[name]:[name, {}]])
    
    return jsonify(results = { "owner" :owner, 
                              "categories" : cat
                               
                              })
@app.route('/<name>/expenses', methods=['GET', 'POST'])
def index_expenses(name):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()()
    app.logger.debug(request)
    if request.mimetype != "application/json":
        return render_template('users/expenses/index.html', name=name)
    owner=viewDefToDict(Owner.all[name])
    app.logger.debug(owner);
    cat = viewDefToDict(Category.categories_by_owner[[name]:[name,{}]])
    expenses = viewDefToDict(Expense.expenses_by_owner[name])   
    return jsonify(results = { "owner" :owner, 
                              "categories" : cat,
                               "expenses" : expenses
                              })

# routes de json
@app.route('/owners', methods=['GET'])
def all_owners():
    return  jsonify(results = viewDefToDict(Owner.all()))
@app.route('/owner', methods=['POST'])
def add_owner():
    owner = Owner(name=request.json['name'], password=bcrypt.generate_password_hash(request.json['password']))
    owner.store()
    return  jsonify(results = dict(owner.items()))
@app.route('/owner/<id>', methods=['DELETE'])
def delete_owner(id):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    g.couch.delete(Owner.load(id))
    return  ""
@app.route('/<name>/categories/<id>', methods=['DELETE'])
def delete_category(id):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    g.couch.delete(Category.load(id))
    return  ""
@app.route('/<name>/category', methods=['POST'])
def add_category(name):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    owner = Owner.all[name]
    if owner.rows !=[] :
         owner = owner.rows[0]
         category = Category(name=request.json['name'], color=request.json['color'], owner=owner.name)
         category.store()
         return  jsonify(results = dict(category.items()))   
    return  jsonify(messages = "L'utilisateur n'existe pas")

@app.route('/<name>/expense', methods=['POST'])
def add_expense(name):
    if not  (flask_login.current_user.is_authenticated and flask_login.current_user.id == name):
        return flask_login.current_app.login_manager.unauthorized()
    owner = Owner.all[name]
    if owner.rows ==[] :
        return  jsonify(messages = "L'utilisateur n'existe pas")
    
    owner = owner.rows[0]
    cat = Category.categories_by_owner[[name, request.json['category']]]
    if cat.rows ==[] :
        return  jsonify(messages = "La categorie n'existe pas")
    cat =cat.rows[0]
    expense = Expense(date=datetime.datetime.strptime(request.json['date'],"%Y/%m/%d").date(), cost=request.json['cost'], description=request.json['description'], owner=owner.name, category=cat.name)
    expense.store()
    return  jsonify(results = dict(expense.items()))   
    

if __name__ == '__main__':
    # configuration
    app.config.update(
       COUCHDB_DATABASE = 'expenses_calc',
       COUCHDB_SERVER = 'http://localhost:5984/',
       DEBUG = True,
       SECRET_KEY = '|T]>_~pz7r`]q6Tq1f%kxQoY(Ad-e-#U=g5?RO]pkgMBD&^Rt+&N(&mNGRY zo,d'

    )
    init_db(app)
    app.run(debug=True)

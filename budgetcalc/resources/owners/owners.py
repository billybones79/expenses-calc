
from flask.ext.mongokit import MongoKit, Document
from flask.views import MethodView, View
from flask import Flask, request, session, g, redirect, url_for, abort,jsonify, \
     render_template, flash
import flask.ext.login as flask_login
from bson.json_util import dumps

import budgetcalc

import logging
import owners


class Owner(Document):
    __collection__ = 'owners'
    structure = {
        'name': unicode,
        'password': unicode
    }

    
    
class OwnersViews(MethodView):

    def get(self, name):
        budgetcalc.app.logger.debug(request.headers["Accept"])
        if name is None:
            if "json" not in  request.headers["Accept"] :
                return render_template('owners/index.html')
            return  dumps({"owners":budgetcalc.db.Owner.find()})
        else:
            return redirect(url_for('categories.categories', owner=name))
            

    def post(self):
        owner = budgetcalc.db.Owner()
        owner['name']=request.json['name']
        owner['password']=unicode(bcrypt.generate_password_hash(request.json['password']))
        owner.save()
        return  dumps({ "owner": owner})

    def delete(self, name):
        # delete a single user
        pass

    def put(self, name):
        # update a single user
        pass
    
class LoginView(View):
    def dispatch_request(self):
        if request.method == 'GET':
            return render_template('owners/login.html')
    
        name =request.form['name']
        owner=budgetcalc.db.Owner.find_one({"name" : name})
        if owner == None :
            return 'Bad login'
        if budgetcalc.bcrypt.check_password_hash(owner["password"], request.form['password'] ):
            owner = budgetcalc.User()
            owner.id = name
            flask_login.login_user(owner)
            return redirect(url_for('expenses.expenses', owner=name))
    
        return 'Bad login'

from flask.ext.mongokit import MongoKit, Document
from flask.views import MethodView
from flask import Flask, request, session, g, redirect, url_for, abort,jsonify, \
     render_template, flash
from budgetcalc.resources.owners import get_owner

from bson.json_util import dumps
     
import json  
import datetime
import logging
import time
import budgetcalc

class Expense(Document):
    __collection__ = 'expenses'
    structure = {
        'cost': float,
        'description':unicode,
        'date': datetime.datetime,
        'category': unicode,
        'owner': unicode
    }  
 
    
class ExpensesViews(MethodView):
    decorators = [get_owner]

    def get(self, owner = None, expenses = None):
        if expenses is None:
             #index
            if "json" not in  request.headers["Accept"] :
                #rendering because it is a html request,
                #would probalby want to have angular handle this itself
                return render_template('expenses/index.html', owner=g.owner["name"])
            #dumping expenses, owner and categories in a json doc           
            cat = budgetcalc.db.Category.find({"owner":g.owner["name"]})
            expenses =  budgetcalc.db.Expense.find({"owner":g.owner["name"]})
            return dumps({ "owner" : g.owner, 
                          "categories" : cat,
                           "expenses" : expenses
                         })
        else:
            pass
           
    def post(self,owner):                          
        cat = budgetcalc.db.Category.find_one({"owner": g.owner["name"], "name": request.json['category']})
        if cat == None :
            return  jsonify(messages = "La categorie n'existe pas")
        expense = budgetcalc.db.Expense()
        expense["date"]=datetime.datetime.strptime(request.json['date'],"%Y/%m/%d")
        expense["cost"]=float(request.json['cost'])
        expense["description"]=request.json['description']
        expense['category']=cat["name"]
        expense['owner']=g.owner["name"]
        expense.save()
        return  dumps({"expense":expense})   

    def delete(self, owner):
        #deleting
        budgetcalc.db.Expense.get_from_id(id).delete()
        return  ""
        pass

    def put(self, owner):
        # update a single user
        pass
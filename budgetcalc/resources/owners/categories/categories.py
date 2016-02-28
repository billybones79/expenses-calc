
from flask.ext.mongokit import MongoKit, Document
from flask.views import MethodView
from flask import Flask, request, session, g, redirect, url_for, abort,jsonify, \
     render_template, flash
import flask.ext.login as flask_login
from bson.json_util import dumps
from budgetcalc.resources.owners import get_owner
import datetime

import budgetcalc

import logging
import budgetcalc.resources.owners

class Category(Document): 
    __collection__ = 'categories'  
    __total = None 
    __expenses = None
    structure = {
        'name': unicode,
        'color':unicode,
        'owner':unicode, 
        "type" :unicode
    }
    @staticmethod
    def totals_by_categorie( catCond, expCond ):
        catCond.update( {'owner':g.owner['name']} )        
        cat = budgetcalc.db.Category.find(catCond)
        budgetcalc.app.logger.debug(catCond)
        totals = []
        for c in cat: totals.insert(0,{"Key" : c["name"], "y" : c.total_expenses(expCond), "color" : "#"+c["color"]})
        return  totals   
    def total_expenses(self,cond): 
        cond.update( {"owner":self["owner"], "category":self["name"]} )
        expenses = budgetcalc.db.Expense.find(cond)
        return sum(ex["cost"] for ex in expenses)
    @property
    def expenses(self):
        if self .__expenses ==None:
             self.__expenses =  budgetcalc.db.Expense.find({"owner":self["owner"], "category":self["name"]})
        return self.__expenses
    @property 
    def total(self):
        if self.__total==None:
            self.__total = sum(ex["cost"] for ex in self.expenses)   
        return self.__total
    
    
class CategoriesViews(MethodView):
    decorators = [get_owner]

    def get(self, owner=None, id =None):
        budgetcalc.app.logger.debug(request.headers["Accept"])
        if id is None:
            #if asking for json we'll ruteurn a list of categories for the current owner
            #if not render the view
            if "json" not in  request.headers["Accept"] :
                return render_template('categories/index.html', owner=g.owner["name"])
            cat = budgetcalc.db.Category.find({"owner":g.owner["name"]}).sort('type', 1)
            return dumps( { "owner" :g.owner, 
                           "categories" : cat                              
                              })
        else:
            return
            

    def post(self, owner):
         category = budgetcalc.db.Category()
         category["name"]=request.json['name']
         category["color"]=request.json['color']
         category["type"]=request.json['type']
         category["owner"]=g.owner["name"]
         category.save()
         return  dumps({"category":category})   

    def delete(self, owner, id ):
        budgetcalc.db.Category.get_from_id(id).delete()
        return  ""

    def put(self, name):
        # update a single user
        pass
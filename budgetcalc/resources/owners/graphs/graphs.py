
from flask.ext.mongokit import MongoKit, Document
from flask.views import View
from flask import Flask, request, session, g, redirect, url_for, abort,jsonify, \
     render_template, flash
import flask.ext.login as flask_login
from bson.json_util import dumps
from budgetcalc.resources.owners import get_owner
import budgetcalc
import datetime
from datetime import date
import calendar
from budgetcalc.resources.owners.categories.categories  import Category

import logging

class GraphsViews(View):
    decorators = [get_owner]
    
    def __init__(self, template_name):
        self.template_name = template_name
    def dispatch_request(self, owner):
        if "json" not in  request.headers["Accept"] :
            return render_template(self.template_name, owner=g.owner["name"])
        '''if(!request.json['from'] && !request.json['to']):'''
            
        date_from = datetime.datetime.strptime(request.json['from'] if request.json['from'] else date(date.today().year, date.today().month, 1),"%Y/%m/%d")        
        date_to = datetime.datetime.strptime(request.json['to'] if request.json['to'] else date(date.today().year, date.today().month, 1), "%Y/%m/%d")
        
        date_range = {"date":{"$gte":date_from, "$lt":date_to}}
        
        totalsExpenses = Category.totals_by_categorie({'type': {'$ne' : "earnings"}}, date_range)
        totalsEarnings = Category.totals_by_categorie({'type':"earnings"}, date_range)
        
        return dumps({ "owner" : g.owner, 
                       "expenses" : totalsExpenses,
                       "earnings" : totalsEarnings
                     })
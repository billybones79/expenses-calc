
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
        date_range = {}
        
        if request.json['from']:
            date_range["$gte"]=datetime.datetime.strptime(request.json['from'], "%Y/%m/%d")
        if request.json['to']:                                                     
            date_range["$lt"]=datetime.datetime.strptime(request.json['to'], "%Y/%m/%d")
        cond = {} if date_range=={} else {"date" : date_range}   
          
        budgetcalc.app.logger.debug(date_range)
        totalsExpenses = Category.totals_by_categorie({'type': {'$ne' : "earnings"}}, cond)
        totalsEarnings = Category.totals_by_categorie({'type':"earnings"}, cond)
        
        return dumps({ "owner" : g.owner, 
                       "expenses" : totalsExpenses,
                       "earnings" : totalsEarnings
                     })
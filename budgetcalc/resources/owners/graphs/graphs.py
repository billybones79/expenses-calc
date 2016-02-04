
from flask.ext.mongokit import MongoKit, Document
from flask.views import View
from flask import Flask, request, session, g, redirect, url_for, abort,jsonify, \
     render_template, flash
import flask.ext.login as flask_login
from bson.json_util import dumps

from budgetcalc.resources.owners import get_owner

import budgetcalc

import logging

class GraphsViews(View):
    decorators = [get_owner]
    
    def __init__(self, template_name):
        self.template_name = template_name
    def dispatch_request(self, owner):
        if "json" not in  request.headers["Accept"] :
            return render_template(self.template_name, owner=g.owner["name"])
        
        cat = budgetcalc.db.Category.find({"owner":g.owner["name"]})
        totals = []
        for c in cat: totals.insert(0,{"Key" : c["name"], "y" : c.total, "color" : "#"+c["color"]})
        return dumps({ "owner" : g.owner, 
                      "categories" : cat,
                       "totals" : totals
                     })
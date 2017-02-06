#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.user.user import UserModel
from egb.generic.employee import GenderType

class SalaryTrs(messages.Message):
    salary = messages.FloatField(1, required=False)
    bonus = messages.FloatField(2, required=False)
    commission = messages.FloatField(3, required=False) 
    
class Employee(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    employee_id = messages.IntegerField(2, required=True)
    job_title = messages.StringField(3, repeated=True)
    start_date = messages.StringField(4, required=True)
    end_date = messages.StringField(5, required=False)
    annual_salary = messages.FloatField(6, required=True)
    hourly_rate = messages.FloatField(7, required=True)
    currency = messages.StringField(8, required=True)
    bonus = messages.FloatField(9, required=True)
    commission = messages.FloatField(10, required=True)
    overtime = messages.FloatField(11, required=True)
    weekly_hours = messages.FloatField(12, required=True)
    gender = messages.EnumField(GenderType, 13, required=True)
    
    
class EmployeeList(messages.Message):
    employee_list = messages.MessageField(Employee, 1, repeated=True)

    
class EmployeeModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    gender = msgprop.EnumProperty(GenderType, required=True)
    employee_id = ndb.IntegerProperty(required=True)
    job_title = ndb.StringProperty(repeated=True)    
    start_date = ndb.DateProperty(required=True)
    end_date = ndb.DateProperty(required=True)
    salary = ndb.FloatProperty(required=True)
    hourly_rate = ndb.FloatProperty(required=True)
    currency = ndb.StringProperty(required=True, default='£')
    bonus = ndb.FloatProperty(required=True, default=0)
    commission = ndb.FloatProperty(required=True, default=0)
    overtime = ndb.FloatProperty(required=True, default=0)
    weekly_hours = ndb.FloatProperty(required=True, default=999)
    submitted = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_count(cls):
        return cls.query().count()
    
    @classmethod
    def get_submitted(cls):
        dateSubmitted = cls.query().order(-cls.submitted).get();
        if dateSubmitted:
            return dateSubmitted.submitted
        else:
            return False
        
    @classmethod
    def get_employee_salary(cls, user_key, user_id):
        
        print cls.query(cls.user == user_key, cls.user_id == user_id).get()
        
        return cls.query(cls.user == user_key,
                         cls.user_id == user_id).get().salary

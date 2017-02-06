"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 1 Feb 2017

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
from egb.generic.whitegood import StatusType
from egb.user.user import UserModel
from egb.name_field.name_field import ManagerField, EmployeeField


class WhiteGoodSignupResponse(messages.Message):   
    message = messages.StringField(1, required=True)
    
    
class WhiteGood(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    provider_name = messages.StringField(2, required=False)
    product_type = messages.EnumField(ProductType, 3, required=False)
    product_variation = messages.EnumField(ProductVariation, 4, required=False)
    gross_cost = messages.FloatField(5, required=False)
    status = messages.EnumField(StatusType, 6, required=False)
    submitted = messages.StringField(7, required=True)
    
class WhiteGoodList(messages.Message):
    whitegood_list = messages.MessageField(WhiteGood, 1, repeated=True)
    

class WhitegoodSignup(messages.Message):
    whitegood_signup_key = messages.IntegerField(1, required=True)
    user_id = messages.IntegerField(2, required=True)
    provider_name = messages.StringField(3, required=False)
    product_type = messages.EnumField(ProductType, 4, required=False)
    product_variation = messages.EnumField(ProductVariation, 5, required=False)
    gross_cost = messages.FloatField(6, required=False)
    status = messages.EnumField(StatusType, 7, required=False)
    submitted = messages.StringField(8, required=True)
    employee = messages.MessageField(EmployeeField, 9)
    manager = messages.MessageField(ManagerField, 10)
    token = messages.StringField(11, required=True)
    
class WhitegoodSignupList(messages.Message):
    whitegood_signup_list = messages.MessageField(WhitegoodSignup, 1, repeated=True)
                                     
                                     
class WhitegoodModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    gross_cost = ndb.FloatProperty(required=True)
    status = msgprop.EnumProperty(StatusType, required=True, indexed=True)
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


class WhitegoodSignupModel(ndb.Model):
    whitegood =  ndb.KeyProperty(kind=WhitegoodModel)
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    gross_cost = ndb.FloatProperty(required=True)
    status = msgprop.EnumProperty(StatusType, required=True, indexed=True)
    token = ndb.StringProperty(required=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True) 
    manager = ndb.KeyProperty(kind=UserModel, required=False) 


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
    
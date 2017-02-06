"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 22 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages
from egb.user.user import UserModel
from google.appengine.ext import ndb
from egb.pension.pension import PensionModel 
from egb.life.life import LifeModel

class Beneficiary(messages.Message):
    message = messages.StringField(1, required=True)

class BeneficiaryModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel)
    user_id = ndb.IntegerProperty(required=True)
    relationship = ndb.StringProperty(repeated=True)
    firstname = ndb.StringProperty(repeated=True)
    lastname = ndb.StringProperty(repeated=True)
    dob = ndb.DateProperty(repeated=True)
    pension_perecent = ndb.FloatProperty(repeated=True)
    life_percent = ndb.FloatProperty(repeated=True)
        
        





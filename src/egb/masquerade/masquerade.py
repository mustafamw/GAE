"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 7 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from egb.user.user import UserModel
from google.appengine.ext import ndb 
from protorpc import messages


class Masquerade(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    token = messages.StringField(2, required=True)
    
class MasqueradeResponse(messages.Message):
    message = messages.StringField(1, required=True)

class MasqueradeModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    user_id_as = ndb.IntegerProperty(required=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)





"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 26 Oct 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from google.appengine.ext import ndb
from protorpc import messages
from egb.user.user import UserModel
from egb.utils.error import ErrorHelper

import endpoints

class LogoutResponse(messages.Message):
    message = messages.StringField(1, required=True)
    
class BlacklistToken(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel)
    user_id = ndb.IntegerProperty(required=True)
    token = ndb.StringProperty(required=True)
    expires = ndb.DateTimeProperty(required=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def check_flood(cls, token):
        
        if token:
            
            tokenArr = token.split('.')
        
        if len(tokenArr) == 3:
                    
            qryBlackListToken = cls.query(cls.token==tokenArr[1]).get()
            
            if qryBlackListToken:
                
                raise ErrorHelper.token_unuthorised()
            
        else:
            
            raise ErrorHelper.invalid_token()   
        
        

LOGOUT_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))






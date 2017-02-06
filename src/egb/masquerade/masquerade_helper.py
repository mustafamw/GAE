"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 7 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from google.appengine.ext import ndb
from egb.masquerade.masquerade import Masquerade
from egb.masquerade.masquerade import MasqueradeModel
from egb.user.user import UserModel
from protorpc import messages
from libs.secure.jwt_helper import JwtHelper
from libs.jwt import jwt
import endpoints
import time


class MaqueradeHelper():
    
    MASQUERADE_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                       user_id_as=messages.IntegerField(2, variant=messages.Variant.INT32, required=True))

    def get_maquerade_list(self, user_id):
                           
        qryUsers = UserModel.query(UserModel.user_id == user_id).get()
        
        return qryUsers


    def construct_masquerade_token(self, maquerade, ip_address):
        #Current Date & Time
        iat = int(time.time());          
        #Issuer
        iss =  'www.platform.com/tokens'
        #Audience
        aud = ip_address
        #Issued at
        iat = iat
        #Token expires 
        exp = int(iat + JwtHelper.get_token_expiry())
        #Not before
        nbf = iat
        token = jwt.encode({'client_id': maquerade.key.id(),
                              'user_id':maquerade.user_id,
                              'employee_id':maquerade.employee_id,
                              'iss':iss,
                              'aud':aud,
                              'sub':'Platform Detail',
                              'access':maquerade.access_token,
                              'roles': maquerade.roles,
                              'iat':iat,
                              'nbf':nbf,
                              'exp': exp},
                               JwtHelper.get_secret_key(), 
                               algorithm='HS256')
        return Masquerade(user_id=maquerade.user_id, token=token)
    
    
    
    def construct_masquerade(self, client_id, user_id, user_id_as):
        
        masquerade = MasqueradeModel(user=ndb.Key('UserModel', client_id),
                                     user_id=user_id,
                                     user_id_as=user_id_as).put()
        
        return masquerade
                        
            
        





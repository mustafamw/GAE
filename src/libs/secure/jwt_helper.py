"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 24 Oct 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from libs.jwt import jwt
from google.appengine.ext import ndb
from egb.logout.logout import BlacklistToken
from egb.utils.error import ErrorHelper

TOKEN_EXPIRES = 60 * 2

#from egb.logout.logout import BlacklistToken

from egb.user.user import UserModel

SECRET_KEY = "Fc4SGcl1j4Kmq65LT5Jfl3X9RhV27pHx3ati3yM5g2CaIPsmY02Mgumkbf0ORkO"

class JwtHelper(BlacklistToken):
    
    @staticmethod
    def get_token_expiry():
        return TOKEN_EXPIRES
    
    @staticmethod
    def get_secret_key():
        return SECRET_KEY
        

    def decode_jwt(self, token, ip_address):
        
        #self.check_flood(token)
    
        # Decode and verify the token
        try:
            
            payload = jwt.decode(token, SECRET_KEY, audience = ip_address)

#             client_id = payload['client_id'];
#             user_id = payload['user_id'];
#             access_token = payload['access'];
#             roles = payload['roles'];
            
#             qryUser = UserModel.query(UserModel.key==ndb.Key('UserModel', client_id), 
#                                       UserModel.user_id==user_id, 
#                                       UserModel.status == 1,  
#                                       UserModel.access_token==access_token).fetch()
                
            return payload

            
            
        except jwt.InvalidTokenError:
            
            raise ErrorHelper.token_unuthorised()
        


    def decode_jwt_admin(self, token, ip_address):
        
        self.check_flood(token)
        
        # Decode and verify the token
        try:
            payload = jwt.decode(token, SECRET_KEY, audience = ip_address)

#             client_id = payload['client_id'];
#             user_id = payload['user_id'];
#             access_token = payload['access'];
# #                     roles = payload['roles'];
#             qryUser = UserModel.query(UserModel.key==ndb.Key('UserModel', client_id), 
#                                       UserModel.user_id==user_id, 
#                                       UserModel.status == 1,
#                                       UserModel.access_token == access_token,  
#                                       UserModel.roles.IN(['administration'])).get()
            return payload
                
                
        except jwt.InvalidTokenError:
                
            raise ErrorHelper.token_unuthorised()
        
    
    def decode_jwt_admin_import(self, token, ip_address):
        
        self.check_flood(token)
        
        # Decode and verify the token
        try:
            payload = jwt.decode(token, SECRET_KEY, audience = ip_address)

#             client_id = payload['client_id'];
#             user_id = payload['user_id'];
#             access_token = payload['access'];
# #                     roles = payload['roles'];
#             qryUser = UserModel.query(UserModel.key==ndb.Key('UserModel', client_id), 
#                                       UserModel.user_id==user_id, 
#                                       UserModel.status == 1,
#                                       UserModel.access_token == access_token,  
#                                       UserModel.roles.IN(['administration'])).get()
            return payload
                
                
        except jwt.InvalidTokenError:
                
            return False

        
    def decode_holiday_auth_jwt(self, token, ip_address):
        
        self.check_flood(token)
        
        try:
            
            payload = jwt.decode(token, SECRET_KEY, audience = ip_address)
        
            return payload
        
                
        except jwt.InvalidTokenError:
                
                raise ErrorHelper.token_unuthorised()

        
    
    @staticmethod
    def decode_masquerade_auth_jwt(token, ip_address):
        
        if token:
            tokenArr = token.split('.')
            qryBlackListToken = BlacklistToken.query(BlacklistToken.token==tokenArr[1]).get()
        
            if not qryBlackListToken:
                # Decode and verify the token
                try:
                    payload = jwt.decode(token, SECRET_KEY, audience = ip_address)
                    client_id = payload['client_id'];
                    user_id = payload['user_id'];
                    access_token = payload['access'];
#                     roles = payload['roles'];
                    qryUser = UserModel.query(UserModel.key==ndb.Key('UserModel', client_id), 
                                              UserModel.user_id==user_id, 
                                              UserModel.status == 1, 
                                              UserModel.access_token==access_token,
                                              UserModel.roles.IN(['administration'])).fetch()
                    if qryUser:
                        return payload
                    else:
                        return False
                    
                except jwt.InvalidTokenError:
                    return False
        else:
            
            raise ErrorHelper.maquerade_not_found()
        
    
    @staticmethod
    def decode_notification_auth_jwt(token, ip_address):
        tokenArr = token.split('.')
        if len(tokenArr) == 3:
            qryBlackListToken = BlacklistToken.query(BlacklistToken.token==tokenArr[1]).get()
        
            if not qryBlackListToken:
                # Decode and verify the token
                try:
                    payload = jwt.decode(token, SECRET_KEY, audience = ip_address)
                    client_id = payload['client_id'];
                    user_id = payload['user_id'];
                    access_token = payload['access'];
#                     roles = payload['roles'];
                    qryUser = UserModel.query(UserModel.key==ndb.Key('UserModel', client_id), 
                                              UserModel.user_id==user_id, 
                                              UserModel.status == 1, 
                                              UserModel.access_token==access_token,
                                              UserModel.roles.IN(['administration'])).fetch()
                    if qryUser:
                        return payload
                    else:
                        return False
                    
                except jwt.InvalidTokenError:
                    return False
        else:
            return False
        
    
    @staticmethod
    def decode_reset_jwt(token):
        # Decode and verify the token
        try:
            payload = jwt.decode(token, SECRET_KEY)
            token = payload['token'];
            tokenArr = token.split('-')
            client_id = int(tokenArr[0])
            user_id = int(tokenArr[1])
            hashed = tokenArr[2]
            qryUser = UserModel.query(UserModel.key == ndb.Key('UserModel', client_id), 
                                      UserModel.user_id == user_id, 
                                      UserModel.hash == hashed).get()
                                      
            if qryUser:
                
                return qryUser
            
            raise ErrorHelper.reset_unauthorised()
            
        except jwt.InvalidTokenError:
            
            raise ErrorHelper.reset_unauthorised()





"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 24 Oct 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from egb.user.user import UserModel
from egb.logout.logout_helper import LogoutHelper
from libs.date_time.date_time import DateTime
from libs.secure.jwt_helper import JwtHelper
from libs.jwt import jwt
from egb.login.login import LoginDesktopResponse
from egb.login.login import LoginMobileResponse
# from egb.login.login import LoginBody
from protorpc import messages
import endpoints


class LoginHelper:

    
    LOGIN_CONTAINER = endpoints.ResourceContainer(username=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                  password=messages.StringField(2, variant=messages.Variant.STRING, required=True))
    
    def login_check(self, username, password):
        
        qryLogin = UserModel.query(UserModel.username==username, 
                                   UserModel.password==password,
                                   UserModel.status == 1).get()
                                   
        if qryLogin:
            
            return qryLogin
        
        else:
            
            return False
            
    
    def encode_desktop(self, qryUser, ip_address):
        
        #Current Date & Time
        iat = DateTime.getCurrentUnixDateTime()        
        #Issuer
        iss =  'www.platform.com/tokens'
        #Audience
        aud = ip_address
        #Issued at
        iat = int(iat)
        #Token expires 
        exp = int(iat + JwtHelper.get_token_expiry())
        #Not before
        nbf = int(iat)
        
        LogoutHelper().delete_expired_token(qryUser.key.id(), qryUser.user_id)
        
        encoded = jwt.encode({'client_id': qryUser.key.id(),
                              'user_id':qryUser.user_id,
                              'employee_id':qryUser.employee_id,
                              'iss':iss,
                              'aud':aud,
                              'sub':'Platform Detail',
                              'access':qryUser.access_token,
                              'roles': qryUser.roles,
                              'iat':iat,
                              'nbf':nbf,
                              'exp': exp},
                               JwtHelper.get_secret_key(), 
                               algorithm='HS256')
        
        return LoginDesktopResponse(token=encoded, expiry=exp) 
    
    
    
    def encode_mobile(self, qryUser, ip_address):
        
        #Current Date & Time
        iat = DateTime.getCurrentUnixDateTime()        
        #Issuer
        iss =  'www.platform.com/tokens'
        #Audience
        aud = ip_address
        #Issued at
        iat = iat
        #Token expires 
        #exp = int(iat + JwtHelper.get_token_expiry())
        #Not before
        nbf = iat
        
        LogoutHelper().delete_expired_token(qryUser.key.id(), qryUser.user_id)
        
        encoded = jwt.encode({'client_id': qryUser.key.id(),
                              'user_id':qryUser.user_id,
                              'employee_id':qryUser.employee_id,
                              'iss':iss,
                              'aud':aud,
                              'sub':'Platform Detail',
                              'access':qryUser.access_token,
                              'roles': qryUser.roles,
                              'iat':iat,
                              'nbf':nbf},
                               JwtHelper.get_secret_key(), 
                               algorithm='HS256')
        
        return LoginMobileResponse(token=encoded) 






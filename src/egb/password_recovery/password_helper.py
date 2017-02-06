"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 28 Oct 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from libs.jwt import jwt
from libs.secure.jwt_helper import JwtHelper
from libs.date_time.date_time import DateTime
from egb.password_recovery.password_recovery import ResetPasswordResponse
from protorpc import messages
import endpoints

RESET_TOKEN_EXPIRES = 60 * 60 * 24

class PasswordReset:
    
    RESET_CONTAINER = endpoints.ResourceContainer(email=messages.StringField(1, variant=messages.Variant.STRING, required=True))

    RESET_TOKEN_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    RESET_PASSWORD_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                        password=messages.StringField(2, variant=messages.Variant.STRING, required=True))
    
    CHANGE_PASSWORD_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                        password=messages.StringField(2, variant=messages.Variant.STRING, required=True))
    

    def get_token_reset_expiry(self):
        
        return RESET_TOKEN_EXPIRES
    
    
    def reset_password_encode(self, token):
        
        #Issued at
        iat = DateTime.getCurrentUnixDateTime()
        #Token expires 
        exp = int(DateTime.getCurrentUnixDateTime() + self.get_token_reset_expiry())
        #Not before
        nbf = iat
        
        encoded = jwt.encode({'sub':'Reset password',
                              'token':token,
                              'iat':iat,
                              'exp':exp,
                              'nbf':nbf},
                               JwtHelper.get_secret_key(), 
                               algorithm='HS256')

        return ResetPasswordResponse(message=encoded)
        





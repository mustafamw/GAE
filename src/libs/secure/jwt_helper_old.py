'''
Copyright (C) 2016 EG Benefits. All rights reserved.
 
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 28 Jan 2016

@author: benrandall76@gmail.com
'''

from egb.utils.helper import UtilsHelper

from libs import jwt

import logging
import time

EXP = 'exp'
NBF = 'nbf'
ISS = 'iss'
AUD = 'aud'
IAT = 'iat'

CLIENT_SECRET = 'MassiveSmellyFart'
CLIENT_ID = 'client_id'

EXPIRY_HOURS = 24
EGB = 'egb'
EGB_WEB_APP = 'egb-web-app'

ALGORITHM = 'HS256'

AUTHORIZATION = 'authorization'

DEBUG = logging.getLogger().isEnabledFor(UtilsHelper.get_level())

class JWTHelper():
    
    @staticmethod
    def validate(header):
        if DEBUG:
            logging.info("in validate")
         
        # THIS WILL SKIP AUTH!!!!!!!!!!!!!!!!!!!   
        if DEBUG:
            return True
            
        auth_header = header.request_state.headers.get(AUTHORIZATION)
        
        if not auth_header:
            if DEBUG:
                logging.info("auth_header missing?")
            
            return False
    
        return JWTHelper.validate_jwt(auth_header)

    @staticmethod
    def validate_jwt(auth_header):
        if DEBUG:
            logging.info("in validate_jwt")
            
        # Get the encoded jwt token.
        auth_token = auth_header.split(' ').pop()
        
        if DEBUG:
            logging.info("auth_token: " + str(auth_token))
        
        # Decode and verify the token
        try:
            decoded = jwt.decode(auth_token, CLIENT_SECRET, algorithms=[ALGORITHM])
            
            if DEBUG:
                logging.info("decoded: " + str(decoded))
                
            return True
            
        except:
            # TODO - log all possible exceptions
            # Is the token invalid or has it expired etc
            # The difference could cause the client to behave differently
            
            return False
        
        return False
        
    @staticmethod
    def create_jwt(user_key):
        if DEBUG:
            logging.info("in create_jwt")
            logging.info("user_key: " + user_key)
        
        # token expiry time           
        exp = JWTHelper.get_expiry_time()
        # token 'not created before'
        nbf = JWTHelper.get_version_release_time()
        # issuer
        iss = EGB
        # audience
        aud = EGB_WEB_APP
        # issued at time
        iat = int(time.time())
        
        encoded = jwt.encode({CLIENT_ID: user_key,
                              EXP: exp,
                              NBF: nbf,
                              ISS: iss,
                              AUD: aud,
                              IAT: iat},
                             CLIENT_SECRET,
                             algorithm=ALGORITHM)
        
        if DEBUG:
            logging.info("encoded: " + encoded)
        
        return encoded
        
    @staticmethod
    def get_expiry_time(): 
        if DEBUG:
            logging.info("in get_expiry_time")
            
        return int(time.time() + (3600000 * EXPIRY_HOURS)) 
    
    @staticmethod
    def get_version_release_time():
        if DEBUG:
            logging.info("in get_version_release_time")
            
        # Ensures all tokens are invalidated if the app has been updated
        return int(time.time())
        

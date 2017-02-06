"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 9 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from google.appengine.ext import ndb
from egb.logout.logout import BlacklistToken
from libs.date_time.date_time import DateTime


class LogoutHelper():
    
    @staticmethod
    def delete_expired_token(client_id, user_id):
        
        current_datetime = DateTime.getCurrentDateTime()
        
        qryBlackListToken = BlacklistToken.query(BlacklistToken.user==ndb.Key('UserModel', client_id),
                                                 BlacklistToken.user_id==user_id,
                                                 BlacklistToken.expires < current_datetime).fetch()
        if qryBlackListToken:
            
            for blackListToken in qryBlackListToken:
                blackListToken.key.delete()
    
    @staticmethod
    def logout(client_id, user_id, token, expiry):
        
        current_datetime = DateTime.getCurrentDateTime()
        expiry = DateTime.getUnixToDateTime(expiry)
        tokenArr = token.split('.')
        token=tokenArr[1]
        
        qryBlackListToken = BlacklistToken.query(BlacklistToken.user==ndb.Key('UserModel', client_id),
                                                 BlacklistToken.user_id==user_id,
                                                 BlacklistToken.expires < current_datetime).fetch()
        if qryBlackListToken:
            
            for blackListToken in qryBlackListToken:
                blackListToken.key.delete()
        
        BlacklistToken(user=ndb.Key('UserModel', client_id),
                       user_id=user_id,
                       token=token,
                       expires=expiry).put()





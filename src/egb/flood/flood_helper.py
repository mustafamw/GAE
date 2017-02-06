"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 9 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from egb.user.user import UserModel
from libs.date_time.date_time import DateTime
from egb.flood.flood import FloodModel
from egb.utils.error import ErrorHelper


class Flood():

    @staticmethod
    def checkFlood(username, ip_address):
        current_datetime = DateTime.getCurrentDateTime()
        qryFlood = FloodModel.query(FloodModel.ip_address == ip_address, FloodModel.username==username).get()
        if qryFlood and  current_datetime > qryFlood.expiry:
            qryFlood.key.delete()
        elif qryFlood and  current_datetime < qryFlood.expiry:
            raise ErrorHelper.account_locked
        
    @staticmethod        
    def createFlood(username, ip_address):
        
        current_datetime = DateTime.getCurrentDateTime()
        expires_time = current_datetime + DateTime.addDateTimeMinute(5)
        
        qryUsername = UserModel.query(UserModel.username==username).get()
        qryFlood = FloodModel.query(FloodModel.ip_address == ip_address, FloodModel.username==username).get()
        
        if qryFlood and qryUsername:
            
            if qryFlood.attempt > 4: 
                if current_datetime < qryFlood.expiry:
                    return True
                if current_datetime > qryFlood.expiry:
                    qryFlood.attempt = 0
                    qryFlood.put()
             
            if qryFlood.attempt == 4:
                qryFlood.expiry = expires_time
                qryFlood.put();

            qryFlood.attempt = qryFlood.attempt + 1
            qryFlood.put()
            
        elif qryFlood:
            qryFlood.attempt = qryFlood.attempt + 1
            qryFlood.put()
            
        else:
            FloodModel(ip_address=ip_address,username=username,attempt=1).put()
        





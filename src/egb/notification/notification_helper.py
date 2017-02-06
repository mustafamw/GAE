"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 9 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from egb.notification.notification import NotificationResponse
from egb.notification.notification import Notification
from egb.notification.notification import NotificationList
from egb.notification.notification import NotificationModel
from protorpc import messages
from google.appengine.ext import ndb
import endpoints
from egb.user.user import UserModel
from egb.utils.error import ErrorHelper

class NotificationHelper:
    
    NOTIFICATION_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                     registration_id=messages.StringField(2, variant=messages.Variant.STRING, required=True))

    NOTIFICATION_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                          user_id=messages.IntegerField(2, variant=messages.Variant.INT32, required=False))
    
    def insert_registration_id(self, client_id, user_id, registration_id):
        
        qryNotification = NotificationModel.query(NotificationModel.user==ndb.Key('UserModel', client_id),
                                                  NotificationModel.user_id==user_id).get()
        
        if qryNotification:
            qryNotification.registration_id.append(registration_id)
            qryNotification.put()
            
        else:
            registration_id = registration_id.split()
            NotificationModel(user=ndb.Key('UserModel', client_id),
                              user_id=user_id,
                              registration_id=registration_id).put()
                            
        return NotificationResponse(message="Successfully notification inserted")
    
    
    def get_registration_id(self, user_id):
        
        if user_id and user_id != None:
            
            qryNotification = NotificationModel.query(NotificationModel.user_id==user_id).fetch()
            
        else:
            
            qryNotification = NotificationModel.query().fetch()
        
        return qryNotification
    
    
    def construct_registration_id(self, qryNotificationList):
        
        userArr = []
        
        qryUser = UserModel.query(UserModel.status == 1).fetch()
        
        for user in qryUser:
            
            userArr.append(user.user_id)
        
        notificationListArr = []
        
        for notificationList in qryNotificationList:
            if notificationList.user_id in userArr:
                notification = Notification(user_id=notificationList.user_id,
                                            registration_id=notificationList.registration_id)
                notificationListArr.append(notification)
            
        if len(notificationListArr) > 0:
            
            return NotificationList(notification = notificationListArr)
        
        else:
            
            raise ErrorHelper.notification_not_found()
        
        
        




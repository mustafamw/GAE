"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 9 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from egb.user.user import UserModel
from google.appengine.ext import ndb
from protorpc import messages

class NotificationResponse(messages.Message):
    message = messages.StringField(1, required=False)

class Notification(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    registration_id = messages.StringField(2, repeated=True)       

class NotificationList(messages.Message):
    notification = messages.MessageField(Notification, 1, repeated=True)
    
class NotificationModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    registration_id = ndb.StringProperty(repeated=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)





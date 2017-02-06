"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 22 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from egb.generic.reward_point import RewardPointStatus
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages

from egb.user.user import UserModel

class RewardPoint(messages.Message):
    granted_by = messages.StringField(1, required=False)
    points = messages.IntegerField(2, required=False)
    reason = messages.StringField(3, required=False)
    submitted = messages.StringField(4, required=False)
    
class RewardPointList(messages.Message):
    rewards_point_list = messages.MessageField(RewardPoint, 1, repeated=True)
    

class RewardPointResponse(messages.Message):
    message = messages.StringField(1, required=False)


class RewardPointModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    granted_to = ndb.KeyProperty(kind=UserModel, required=True)
    points = ndb.IntegerProperty(required=True)
    reason = ndb.StringProperty(default="Reward Point")
    status = msgprop.EnumProperty(RewardPointStatus, repeated=True)
    token = ndb.StringProperty(required=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)






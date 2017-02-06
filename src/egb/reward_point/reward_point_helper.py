"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 22 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from libs.tokenGenerate.token import Token
from egb.user.user import UserModel
from egb.reward_point.reward_point import RewardPointResponse
from egb.reward_point.reward_point import RewardPointModel
from egb.reward_point.reward_point import RewardPoint
from egb.reward_point.reward_point import RewardPointList
from egb.utils.error import ErrorHelper
from egb.generic.reward_point import RewardPointTypeHelper
from libs.parse.parse import Parse
from google.appengine.ext import ndb
from protorpc import messages
import endpoints


class RewardPointHelper(Parse):
    
    REWARD_POINT_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                     granted_to=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                     points=messages.IntegerField(3, variant=messages.Variant.INT32, required=True),
                                                     reason=messages.StringField(4, variant=messages.Variant.STRING, required=False))

    REWARD_POINT_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    REWARD_POINT_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                  reward_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                  status=messages.IntegerField(3, variant=messages.Variant.INT32, required=True),
                                                                  hash=messages.StringField(4, variant=messages.Variant.STRING, required=True),
                                                                  reason=messages.StringField(5, variant=messages.Variant.STRING, required=False))
    
    def insert_reward_point(self, client_id, user_id, granted_to, points, reason):
        
        status = [RewardPointTypeHelper.get_reward_point(1)]
        tokenVar = Token.generate_token()
        
        RewardPointModel(user=ndb.Key('UserModel', client_id),
                         user_id=user_id,
                         status=status,
                         granted_to=ndb.Key('UserModel', granted_to),
                         points=points,
                         token=tokenVar,
                         reason=reason).put()
                         
        return RewardPointResponse(message="Successfully Inserted")
    
    
    def reward_points_approval_update(self, reward_point_key, hashed, status, reason):
        
        qryRewardPoint = RewardPointModel.query(RewardPointModel.key==ndb.Key('RewardPointModel', reward_point_key),
                                                RewardPointModel.token==hashed).get()
        
        if qryRewardPoint:
            tokenVar = Token.generate_token()
            status = [RewardPointTypeHelper.get_reward_point(status)]
            qryRewardPoint.status = status
            qryRewardPoint.token = tokenVar
            qryRewardPoint.put()
            
            return RewardPointResponse(message="Successfully ....")
        
        raise ErrorHelper.reward_point_not_found()
        

    def get_reward_points_list(self, client_id):
        
        qryRewardPointList = RewardPointModel.query(RewardPointModel.granted_to==ndb.Key('UserModel', client_id)).fetch()
        
        if qryRewardPointList:
            
            return qryRewardPointList
        
        raise ErrorHelper.reward_point_not_found()
        
        
    def contruct_list_point(self, list_rewards_point):
        
        rewardPointsArr = []
        
        for reward_point in list_rewards_point:
            
            qryUser = UserModel.query(UserModel.key==reward_point.user).get()
            
            reward_point = RewardPoint(granted_by = qryUser.email,
                                       points = reward_point.points,
                                       reason = reward_point.reason,
                                       submitted = self.parseDateFormatHyphen(reward_point.submitted))
            
            rewardPointsArr.append(reward_point)
            
        return RewardPointList(rewards_point_list=rewardPointsArr)
            
            
            
            
    
    






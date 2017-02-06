"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 22 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from protorpc import messages


class RewardPointStatus(messages.Enum):
    pending = 1
    accept = 2
    cancel = 3
    redeem = 4


class RewardPointTypeHelper():
    
    @staticmethod
    def get_reward_point(reward_status):
            
        if reward_status == 1:
            return RewardPointStatus.pending
        elif reward_status == 2:
            return RewardPointStatus.accept
        elif reward_status == 3:
            return RewardPointStatus.cancel
        elif reward_status == 4:
            return RewardPointStatus.redeem
        
        return RewardPointStatus.pending
    
        





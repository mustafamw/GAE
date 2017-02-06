"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 29 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages

class WhoLevel(messages.Enum):
    NONE = 0
    SELF_AND_CHILDREN = 1
    SELF_AND_PARTNER = 2
    

class CoverLevel(messages.Enum):
    NONE = 0
    BRONZE = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4
    

class StatusType(messages.Enum):
    accept = 1
    cancel = 2
    pending = 3
    withdraw = 4


class CashplanTypeHelper():
    
    @staticmethod
    def get_who_type(who_type):
        if who_type == 0:
            return WhoLevel.NONE            
        elif who_type == 1:
            return WhoLevel.SELF_AND_CHILDREN
        elif who_type == 2:
            return WhoLevel.SELF_AND_PARTNER

        return WhoLevel.NONE
    
    
    @staticmethod
    def get_status_type(status):
        
        if status == 1:
            return StatusType.accept
        
        elif status == 2:
            return StatusType.cancel
        
        elif status == 3:
            return StatusType.pending
        
        elif status == 4:
            return StatusType.withdraw
        
        else:
            return StatusType.pending
        
    
    @staticmethod
    def get_cover_level(cover_level):
        
        if cover_level == 1:
            return CoverLevel.BRONZE
        elif cover_level == 2:
            return CoverLevel.SILVER
        elif cover_level == 3:
            return CoverLevel.GOLD
        
        return CoverLevel.BRONZE





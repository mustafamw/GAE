"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 30 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages

class WhoLevel(messages.Enum):
    NONE = 0
    SELF = 1
    SELF_AND_PARTNER = 2
    SELF_AND_CHILDREN = 3
    FAMILY = 4
    

class StatusType(messages.Enum):
    accept = 1
    cancel = 2
    pending = 3
    withdraw = 4
    
class CoverLevel(messages.Enum):
    NONE = 0
    KEY = 1
    ELEMENTARY = 2
    ESSENTIAL = 3
    ESSENTIAL_PLUS = 4
    EXTENSIVE = 5
    EXTENSIVE_PLUS = 6
    
class CoverWhere(messages.Enum):
    LIMITED = 1
    NATIONAL = 2
    PRIVATE = 3


class DentalTypeHelper():
    
    @staticmethod
    def get_who_type(who_type):
        
        if who_type == 0:
            return WhoLevel.NONE  
                  
        elif who_type == 1:
            return WhoLevel.SELF
        
        elif who_type == 2:
            return WhoLevel.SELF_AND_PARTNER
        
        elif who_type == 3:
            return WhoLevel.SELF_AND_CHILDREN
        
        elif who_type == 4:
            return WhoLevel.FAMILY

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
    def get_cover_where(cover_where):
            
        if cover_where == 1:
            return CoverWhere.LIMITED
        elif cover_where == 2:
            return CoverWhere.NATIONAL
        elif cover_where == 3:
            return CoverWhere.PRIVATE
        
        return CoverWhere.LIMITED
    
    @staticmethod
    def get_cover_level(cover_level):
        
        if cover_level == 0:
            return CoverLevel.NONE
        elif cover_level == 1:
            return CoverLevel.KEY
        elif cover_level == 2:
            return CoverLevel.ELEMENTARY
        elif cover_level == 3:
            return CoverLevel.ESSENTIAL
        elif cover_level == 4:
            return CoverLevel.ESSENTIAL_PLUS
        elif cover_level == 5:
            return CoverLevel.EXTENSIVE
        elif cover_level == 6:
            return CoverLevel.EXTENSIVE_PLUS
        
        return CoverLevel.BRONZE






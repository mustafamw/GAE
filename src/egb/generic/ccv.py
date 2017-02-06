"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 25 Jan 2017

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages


class StatusType(messages.Enum):
    accept = 1
    cancel = 2
    pending = 3
    withdraw = 4
    
    
class CcvTypeHelper():
    
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






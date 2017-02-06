"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 23 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from protorpc import messages

class TaxSavingType(messages.Enum):
    SALARY_SACRIFICE = 1
    NET_SAVING = 2
    
    
class StatusType(messages.Enum):
    accept = 1
    cancel = 2
    pending = 3
    withdraw = 4
    

class PensionTypeHelper:
    
    def get_tax_saving_type(self, tax_saving_type):
        if tax_saving_type == 1:
            return TaxSavingType.SALARY_SACRIFICE
        elif tax_saving_type == 2:
            return TaxSavingType.NET_SAVING
        else:
            return TaxSavingType.SALARY_SACRIFICE
        

    def get_status_type(self, status):
        
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
    
        
        






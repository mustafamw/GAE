"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 1 Dec 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages
    
class DeferredType(messages.Enum):
    NONE = 0
    MONTH_1 = 1
    MONTH_3 = 2
    MONTH_6 = 3
    
class PaymentTermType(messages.Enum):
    YEAR_1 = 1
    YEAR_2 = 2
    YEAR_5 = 3
    STATE_PENSION_AGE = 4
    
class StatusType(messages.Enum):
    accept = 1
    cancel = 2
    pending = 3
    withdraw = 4
    
class GipTypeHelper():    
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
        
    def get_deferred_type(self, deferred):
        if deferred == 0:
            return DeferredType.NONE
        elif deferred == 1:
            return DeferredType.MONTH_1
        elif deferred == 2:
            return DeferredType.MONTH_3
        elif deferred == 3:
            return DeferredType.MONTH_6
        else:
            return DeferredType.MONTH_1  
        
    def get_payment_term_type(self, payment_term):
        if payment_term == 1:
            return PaymentTermType.YEAR_1
        elif payment_term == 2:
            return PaymentTermType.YEAR_2
        elif payment_term == 3:
            return PaymentTermType.YEAR_5
        elif payment_term == 4:
            return PaymentTermType.STATE_PENSION_AGE
        else:
            return PaymentTermType.YEAR_1     
    
    






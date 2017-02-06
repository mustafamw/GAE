from protorpc import messages

class Allowance(messages.Enum):
    day = 1
    hour = 2
    
class HolidayHalfDay(messages.Enum):
    false = 1
    morning = 2
    afternoon = 3

class Status(messages.Enum):
    pending = 1
    cancel = 2
    withdrawn = 3
    accept = 4
    

class HolidayTypeHelper():
    
    @staticmethod
    def get_allowance_type(allowance_type):
        
        if allowance_type == 1:
            return Allowance.day
        elif allowance_type == 2:
            return Allowance.hour
        return Allowance.day
    
    @staticmethod
    def get_halfday_type(halfday_type):
        
        if halfday_type == 1:
            return HolidayHalfDay.false
        elif halfday_type == 2:
            return HolidayHalfDay.morning
        elif halfday_type == 3:
            return HolidayHalfDay.afternoon
        else:
            return halfday_type.false
    
    @staticmethod
    def get_status_type(status_type):  
        
        if status_type == 1:
            return Status.pending
        elif status_type == 2:
            return Status.cancel
        elif status_type == 3:
            return Status.withdrawn
        elif status_type == 4:
            return Status.accept
        
        return Status.pending
    
    

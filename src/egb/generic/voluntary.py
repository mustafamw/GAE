from protorpc import messages

from egb.utils.helper import UtilsHelper 

import logging

DEBUG = logging.getLogger().isEnabledFor(UtilsHelper.get_level())

class VoluntaryType(messages.Enum):
    VOL1 = 1
    VOL2 = 2
    VOL3 = 3
    
    
class VoluntaryTypeHelper():
    
    @staticmethod
    def get_voluntary_type(voluntary_type):
        if DEBUG:
            logging.info("in get_voluntary_type " + voluntary_type)
            
        voluntary_type = int(voluntary_type)    
            
        if voluntary_type == 1:
            return VoluntaryType.VOL1
        elif voluntary_type == 2:
            return VoluntaryType.VOL2
        elif voluntary_type == 3:
            return VoluntaryType.VOL3
        
        if DEBUG:
            logging.info("in get_voluntary_type returning default")
        
        return VoluntaryType.VOL1
    
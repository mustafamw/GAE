from protorpc import messages

from egb.utils.helper import UtilsHelper 

import logging

DEBUG = logging.getLogger().isEnabledFor(UtilsHelper.get_level())

class RoleWho(messages.Enum):
    ADMINISTRATOR = 1
    AUTHENTICATED = 2
    ANONYMOUS = 3
    ROLE4 = 4
    ROLE5 = 5
    ROLE6 = 6
    ROLE7 = 7
    ROLE8 = 8
    ROLE9 = 9
    ROLE10 = 10
    ROLE11 = 11
    ROLE12 = 12
    ROLE13 = 13
    ROLE14 = 14
    ROLE15 = 15
    ROLE1 = 16

class RoletypeHelper():
    
    @staticmethod
    def get_role_type(role_type):
        if DEBUG:
            logging.info("in get_who_type " + role_type)
            
        role_who = int(role_type)    
            
        if role_who == 1:
            return RoleWho.ADMINISTRATOR
        elif role_who == 2:
            return RoleWho.AUTHENTICATED
        elif role_who == 3:
            return RoleWho.AUTHENTICATED
        elif role_who == 4:
            return RoleWho.ROLE4
        elif role_who == 5:
            return RoleWho.ROLE5
        elif role_who == 6:
            return RoleWho.ROLE6
        elif role_who == 7:
            return RoleWho.ROLE7
        elif role_who == 8:
            return RoleWho.ROLE8
        elif role_who == 9:
            return RoleWho.ROLE9
        elif role_who == 10:
            return RoleWho.ROLE10
        elif role_who == 11:
            return RoleWho.ROLE11
        elif role_who == 12:
            return RoleWho.ROLE12
        elif role_who == 13:
            return RoleWho.ROLE13
        elif role_who == 14:
            return RoleWho.ROLE14
        elif role_who == 15:
            return RoleWho.ROLE15
        
        return role_who.AUTHENTICATED
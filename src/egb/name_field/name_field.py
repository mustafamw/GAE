"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 1 Dec 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages
# from egb.ess.ess import ESSModel

class ManagerField(messages.Message):
    firstname = messages.StringField(1)
    lastname = messages.StringField(2)
    

class EmployeeField(messages.Message):
    firstname = messages.StringField(1)
    lastname = messages.StringField(2)
    
class NameFieldHelper():
    
    def get_key_list(self, key_list):
        
        key_listArr = []
        
        for key in key_list:
            
            if hasattr(key, 'user'):
                key_listArr.append(key.user)
                
            if hasattr(key, 'manager'):
                key_listArr.append(key.manager)
                
        return key_listArr
            
            
        
        
    
    


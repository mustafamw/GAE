"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 26 Oct 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

class CheckRoles():
    
    @staticmethod
    def roles(userRole, listRoles):
        
        for role in userRole:
            
            if role in listRoles:
                
                return True
            
                break




"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 3 Jan 2017

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages

class GenderType(messages.Enum):
    male = 1
    female = 2
    

class EmployeeTypeHelper():
    
    def get_geneder_type(self, gender):
        
        if gender == 1:
            return GenderType.male
        elif gender == 2:
            return GenderType.female
        else:
            return GenderType.male





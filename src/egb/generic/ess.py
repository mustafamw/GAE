"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 3 Jan 2017

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages

class TitleType(messages.Enum):
    mr = 1
    mrs = 2
    miss = 3
    ms = 4
    dr = 5
    
    
class EssTypeHelper():
    
    def get_title_type(self, title):
        
        if title == 1:
            return TitleType.mr
        elif title == 2:
            return TitleType.mrs
        elif title == 3:
            return TitleType.miss
        elif title == 4:
            return TitleType.ms
        elif title == 5:
            return TitleType.dr
        else:
            return TitleType.mr
            






"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 22 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages

class RelationshipHelper:
    
    self = "Self"
    partner = "Self & Partner"
    children = "Self & Children"
    family = "Family"
    
    def getRelationship(self, relationshipType):
        
        if relationshipType == 1:    
            return self.self;
        
        elif relationshipType == 2:
            return self.partner
        
        elif relationshipType == 3:
            return self.children

        elif relationshipType == 4:
            return self.family
        
        else:
            return self.self;
            
            
            
    




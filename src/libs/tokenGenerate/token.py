"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 24 Oct 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
import uuid

class Token():
    
    @staticmethod
    def generate_token():
        return uuid.uuid4().hex;









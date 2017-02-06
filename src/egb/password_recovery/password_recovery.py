"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 28 Oct 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from protorpc import messages

class ResetPasswordResponse(messages.Message):
    message = messages.StringField(1, required=True)
    

class ChangePasswordResponse(messages.Message):
    message = messages.StringField(1, required=True)






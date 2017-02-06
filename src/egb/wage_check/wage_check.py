"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 27 Jan 2017

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from protorpc import messages

class WageCheck(messages.Message):
    client_id = messages.IntegerField(1, required=False)
    user_id = messages.IntegerField(2, required=False)
    firstname = messages.StringField(3, required=False)
    lastname = messages.StringField(4, required=False)
    salary = messages.FloatField(5, required=False)
    weekly_hours = messages.FloatField(6, required=False)
    car = messages.FloatField(7, required=False)
    ccv = messages.FloatField(8, required=False)
    ctw = messages.FloatField(9, required=False)
    pension = messages.FloatField(10, required=False)
    total_sacrificed = messages.FloatField(11, required=False)
    

class WageCheckList(messages.Message):
    wage_check_list = messages.MessageField(WageCheck, 1, repeated=True)
    







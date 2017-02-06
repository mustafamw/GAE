"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 1 Feb 2017

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages
from egb.whitegood.whitegood import WhiteGood, WhiteGoodList, WhitegoodModel, WhitegoodSignupModel, WhitegoodSignup, WhitegoodSignupList, WhiteGoodSignupResponse
from egb.generic.whitegood import WhitegoodTypeHelper, StatusType
from egb.ess.ess import EssModel
from egb.user.user import UserModel
from google.appengine.ext import ndb
from libs.parse.parse import Parse
from libs.tokenGenerate.token import Token
from egb.utils.error import ErrorHelper
from egb.name_field.name_field import ManagerField, EmployeeField, NameFieldHelper
from egb.user.user_helper import UserHelper
from libs.date_time.date_time import DateTime
import endpoints
    
class WhitegoodHelper(Parse, WhitegoodTypeHelper, UserHelper, NameFieldHelper):
    
    WHITEGOOD_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    WHITEGOOD_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))

    WHITEGOOD_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                       user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                       whitegood_signup_status=messages.EnumField(StatusType, 3, repeated=True))

    WHITEGOOD_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                      whitegood_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                      hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                      status=messages.EnumField(StatusType, 4, required=True))
    
    
    def get_whitegood(self, client_id, user_id):
                                           
        cars = WhitegoodModel.query(WhitegoodModel.user == ndb.Key('UserModel', client_id),
                                    WhitegoodModel.status.IN([self.get_status_type(5),
                                                              self.get_status_type(1)])).fetch()

        if cars:
            
            return cars
        
        raise ErrorHelper.white_goods_not_found()
    
    def construct_whitegood(self, cars):
        
        carsArr = []
        
        for car in cars:
            
            submitted = self.parseDateFormatHyphen(car.submitted)
            
            car = WhiteGood(user_id=car.user_id,
                            provider_name=car.provider_name,
                            product_type=car.product_type,
                            product_variation=car.product_variation,
                            gross_cost=car.gross_cost,
                            status=car.status,
                            submitted=submitted)
            
            carsArr.append(car)
            
        return WhiteGoodList(whitegood_list = carsArr)
    

    def whitegood_signup_list_get(self, client_id, user_id):
        
        qryWhiteGoodsSignup = WhitegoodSignupModel.query(WhitegoodSignupModel.user == ndb.Key('UserModel', client_id),
                                                         WhitegoodSignupModel.user_id==user_id).fetch()
        
        if qryWhiteGoodsSignup:
            
            return qryWhiteGoodsSignup
        
        raise ErrorHelper.whitegood_signup_not_found()
    
    
    def whitegood_signup_list_auth_get(self, user_status, whitegood_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryWhitegoodSignup = WhitegoodSignupModel.query(WhitegoodSignupModel.user.IN(qryUser),
                                                        WhitegoodSignupModel.status.IN(whitegood_signup_status)).fetch()
        
        if qryWhitegoodSignup:
            
            return qryWhitegoodSignup
        
        raise ErrorHelper.whitegood_signup_not_found()
    
    
    def construct_whitegood_signup_list(self, whitegood_signup_list):

        whitegood_signup_listArr = []

        ess_list = EssModel.get_ess(self.get_key_list(whitegood_signup_list))
        
        for whitegood_signup in whitegood_signup_list:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if whitegood_signup.manager:
                
                manager_key = whitegood_signup.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if whitegood_signup.user:
                
                employee_key = whitegood_signup.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
            
            submitted = self.parseDateTimeFormatHyphen(whitegood_signup.submitted)
                        
            whitegood_signup_list = WhitegoodSignup(user_id=whitegood_signup.user_id,
                                                    whitegood_signup_key=whitegood_signup.key.id(),
                                                    gross_cost=whitegood_signup.gross_cost,
                                                    token=whitegood_signup.token,
                                                    submitted=submitted,
                                                    status=whitegood_signup.status,
                                                    manager=ManagerField(firstname=manager_firstname, 
                                                                        lastname=manager_lastname),
                                                    employee=EmployeeField(firstname=employee_firstname, 
                                                                           lastname=employee_lastname))
            
            whitegood_signup_listArr.append(whitegood_signup_list) 
            
        return WhitegoodSignupList(whitegood_signup_list=whitegood_signup_listArr)


    def white_good_signup_approval_update(self, client_id, user_id, whitegood_signup_key, hashed, status):
        
        qryWhiteGoodSignup = WhitegoodSignupModel.query(WhitegoodSignupModel.key == ndb.Key('WhitegoodSignupModel', whitegood_signup_key),
                                                        WhitegoodSignupModel.token == hashed,
                                                        WhitegoodSignupModel.status == self.get_status_type(3)).get()
        
        
        if qryWhiteGoodSignup:
            
            whitegood_key = WhitegoodModel(provider_name=qryWhiteGoodSignup.provider_name,
                                            product_type=qryWhiteGoodSignup.product_type,
                                            product_variation=qryWhiteGoodSignup.product_variation,
                                            user=qryWhiteGoodSignup.user,
                                            user_id=qryWhiteGoodSignup.user_id,
                                            status=status,
                                            gross_cost=qryWhiteGoodSignup.gross_cost)
                     
            whitegood_key.put()
            
            tokenVar = Token.generate_token()
            qryWhiteGoodSignup.white_good = whitegood_key.key
            qryWhiteGoodSignup.token = tokenVar
            qryWhiteGoodSignup.status = status
            qryWhiteGoodSignup.submitted = DateTime.getCurrentDateTime()
            qryWhiteGoodSignup.manager = ndb.Key('UserModel', client_id)
            qryWhiteGoodSignup.put()               
        
            return WhiteGoodSignupResponse(message="Successfully %s" % (status))
        
        
        raise ErrorHelper.whitegood_signup_not_found()
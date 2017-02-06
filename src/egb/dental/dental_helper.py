from protorpc import messages
from egb.dental.dental import DentalModel, Dental, DentalList, DentalSignupModel, DentalSignupResponse, DentalSignup, DentalSignupList
from egb.generic.dental import DentalTypeHelper, WhoLevel, CoverLevel, StatusType
from google.appengine.ext import ndb
from libs.tokenGenerate.token import Token
from libs.date_time.date_time import DateTime
from libs.parse.parse import Parse
from egb.ess.ess import EssModel
from egb.name_field.name_field import ManagerField, EmployeeField, NameFieldHelper
from egb.utils.error import ErrorHelper
from egb.user.user_helper import UserHelper
from egb.user.user import UserModel
import endpoints
    
class DentalHelper(Parse, DentalTypeHelper, UserHelper, NameFieldHelper):
    
    DENTAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    DENTAL_SIGNUP_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                          who=messages.EnumField(WhoLevel, 2, required=True),
                                                          cover_level=messages.EnumField(CoverLevel, 3, required=True),
                                                          gross_cost=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True))

    DENTAL_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                               dental_signup_status=messages.EnumField(StatusType, 2, repeated=True))
    
    DENTAL_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                    user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                    dental_signup_status=messages.EnumField(StatusType, 3, repeated=True))
    
    
    DENTAL_SIGNUP_CANCEL_WITHDRAW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                        dental_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                        hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True))

    
    DENTAL_SIGNUP_AMEND_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                            dental_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                            who=messages.IntegerField(3, variant=messages.Variant.INT64, required=True),
                                                            level_cover=messages.IntegerField(4, variant=messages.Variant.INT32, required=True),
                                                            gross_cost=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True),
                                                            hashed=messages.StringField(6, variant=messages.Variant.STRING, required=True))
    
    DENTAL_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                   dental_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                   hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                   status=messages.EnumField(StatusType, 4, required=True)) 
    
    def get_dental(self, client_id, user_id):
                                           
        qryDental = DentalModel.query(DentalModel.user == ndb.Key('UserModel', client_id), 
                                      DentalModel.user_id == user_id).fetch()
        
        if qryDental:

            return qryDental
        
        raise ErrorHelper.dental_not_found()
            
            
    def construct_dental(self, dentals):
        
        dentalArr = []
        
        for dental in dentals:
            
            dental = Dental(dental_key=dental.key.id(),
                            user_id=dental.user_id,
                            provider_name=dental.provider_name,
                            product_type=dental.product_type,
                            product_variation=dental.product_variation,
                            who=dental.who,
                            premium_who=dental.premium_who,
                            cover_level=dental.cover_level,
                            premium_cover_level=dental.premium_cover_level,
                            premium_core=dental.premium_core,
                            gross_cost=dental.gross_cost)
            
            dentalArr.append(dental)
         
        return DentalList(dental_list=dentalArr)
    
    
    def dental_signup_insert(self, client_id, user_id, who, cover_level, gross_cost):
    
        qryDental = DentalModel.query(DentalModel.user == ndb.Key('UserModel', client_id),
                                      DentalModel.user_id==user_id).get()
                                          
        if qryDental:
        
            qryDentalSignup = DentalSignupModel.query(DentalSignupModel.dental==qryDental.key,
                                                      DentalSignupModel.user_id==user_id,
                                                      DentalSignupModel.status==self.get_status_type(3)).get() 

            if qryDentalSignup:
                
                    raise ErrorHelper.data_already_exists()
            
            else:
                
                status = self.get_status_type(3)
                
                DentalSignupModel(dental=qryDental.key,
                                  user=qryDental.user,
                                  user_id=user_id,
                                  who=who,
                                  cover_level=cover_level,
                                  gross_cost=gross_cost,
                                  status=status,
                                  token=Token.generate_token()).put()
                                    
                return DentalSignupResponse(message="Successfully signed up")
        
        else:
            
            raise ErrorHelper.dental_not_found()
        
    def dental_signup_list_get(self, user_id, client_id, dental_signup_status):
        
        qryDentalSignup = DentalSignupModel.query(DentalSignupModel.user == ndb.Key('UserModel', client_id),
                                                  DentalSignupModel.user_id == user_id,
                                                  DentalSignupModel.status.IN(dental_signup_status)).fetch()
            
        if qryDentalSignup:
                
            return qryDentalSignup
            
        raise ErrorHelper.dental_signup_not_found()
    

    def dental_signup_list_auth_get(self, user_status, dental_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryDentalSignup = DentalSignupModel.query(DentalSignupModel.user.IN(qryUser),
                                                  DentalSignupModel.status.IN(dental_signup_status)).fetch()
        
        if qryDentalSignup:
            
            return qryDentalSignup
        
        raise ErrorHelper.dental_signup_not_found()
    
    
    
    def construct_dental_signup_list(self, dental_signup_list):
        
        dental_signup_listArr = []

        ess_list = EssModel.get_ess(self.get_key_list(dental_signup_list))
        
        for dental_signup in dental_signup_list:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if dental_signup.manager:
                
                manager_key = dental_signup.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if dental_signup.user:
                
                employee_key = dental_signup.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
             

            submitted = self.parseDateTimeFormatHyphen(dental_signup.submitted)
             
            dental_signup = DentalSignup(user_id=dental_signup.user_id,
                                         dental_signup_key=dental_signup.key.id(),
                                         who=dental_signup.who,
                                         cover_level=dental_signup.cover_level,
                                         gross_cost=dental_signup.gross_cost,
                                         token=dental_signup.token,
                                         status=dental_signup.status,
                                         manager=ManagerField(firstname=manager_firstname, 
                                                              lastname=manager_lastname),
                                         employee=EmployeeField(firstname=employee_firstname, 
                                                                lastname=employee_lastname),
                                         submitted=submitted)
             
            dental_signup_listArr.append(dental_signup)
             
        return DentalSignupList(dental_signup_list=dental_signup_listArr)
    
    
    def dental_signup_approval_update(self, client_id, user_id, dental_signup_key, hashed, status):
        
        qryDentalSignup = DentalSignupModel.query(DentalSignupModel.key == ndb.Key('DentalSignupModel', dental_signup_key),
                                                  DentalSignupModel.token == hashed,
                                                  DentalSignupModel.status == self.get_status_type(3)).get()
        
        
        if qryDentalSignup:
            
            tokenVar = Token.generate_token()
            
            qryDentalSignup.token = tokenVar
            qryDentalSignup.status = status
            qryDentalSignup.submitted = DateTime.getCurrentDateTime()
            qryDentalSignup.manager = ndb.Key('UserModel', client_id)
            qryDentalSignup.put()
        
            return DentalSignupResponse(message="Successfully %s" % (status))
        
        
        else:

            raise ErrorHelper.dental_signup_not_found()
    
    
    def dental_signup_amend_update(self, user_id, dental_signup_key, who_cover, level_cover, gross_cost, hashed):
        
        qryDentalSignup = DentalSignupModel.query(DentalSignupModel.key==ndb.Key('DentalSignupModel', dental_signup_key),
                                                      DentalSignupModel.user_id==user_id,
                                                      DentalSignupModel.token==hashed,
                                                      ndb.OR(DentalSignupModel.status == self.get_status_type(1),
                                                             DentalSignupModel.status == self.get_status_type(3))).get()
        
        if qryDentalSignup:
            
            status = self.get_status_type(3)
            who_cover = self.get_who_type(who_cover)
            
            qryDentalSignup.who = who_cover
            qryDentalSignup.gross_cost = gross_cost
            qryDentalSignup.status = status
            qryDentalSignup.token = Token.generate_token()
            qryDentalSignup.submitted = DateTime.getCurrentDateTime()
            qryDentalSignup.put()
            
            return DentalSignupResponse(message="Successfully amended")
        
        else:
            
            raise ErrorHelper.dental_not_found()
        
    
    
    def dental_signup_cancel_update(self, user_id, dental_signup_key, hashed):
        
        qryDentalSignup = DentalSignupModel.query(DentalSignupModel.key == ndb.Key('DentalSignupModel', dental_signup_key),
                                                      DentalSignupModel.user_id == user_id,
                                                      DentalSignupModel.token == hashed,
                                                      DentalSignupModel.status == self.get_status_type(1)).get()
        
        if qryDentalSignup:
            
            status = self.get_status_type(2)
            
            qryDentalSignup.status = status;
            qryDentalSignup.submitted = DateTime.getCurrentDateTime()
            qryDentalSignup.token = Token.generate_token()
            qryDentalSignup.put()
            
            return DentalSignupResponse(message="Successfully canceled")
    
        else:
            
            raise ErrorHelper.dental_signup_not_found()
        
    
    def dental_signup_withdraw_update(self, user_id, dental_signup_key, hashed):
        
        qryDentalSignup = DentalSignupModel.query(DentalSignupModel.key == ndb.Key('DentalSignupModel', dental_signup_key),
                                                      DentalSignupModel.user_id == user_id,
                                                      DentalSignupModel.token == hashed,
                                                      DentalSignupModel.status == self.get_status_type(3)).get()
        
        if qryDentalSignup:
            
            status = self.get_status_type(4)
            
            qryDentalSignup.status = status;
            qryDentalSignup.submitted = DateTime.getCurrentDateTime()
            qryDentalSignup.token = Token.generate_token()
            qryDentalSignup.put()
            
            return DentalSignupResponse(message="Successfully withdraw")
    
        else:
            
            raise ErrorHelper.dental_signup_not_found()
                

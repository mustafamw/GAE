from protorpc import messages
from egb.cashplan.cashplan import CashplanModel, Cashplan, CashplanList, CashplanSignupModel, CashplanSignupResponse, CashplanSignup, CashplanSignupList
from egb.generic.cashplan import CashplanTypeHelper, WhoLevel, CoverLevel, StatusType
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
    
class CashplanHelper(Parse, CashplanTypeHelper, UserHelper, NameFieldHelper):
    
    CASHPLAN_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    CASHPLAN_SIGNUP_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                            who=messages.EnumField(WhoLevel, 2, required=True),
                                                            cover_level=messages.EnumField(CoverLevel, 3, required=True),
                                                            gross_cost=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True))

    CASHPLAN_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                 cashplan_signup_status=messages.EnumField(StatusType, 2, repeated=True))
    
    CASHPLAN_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                      user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                      cashplan_signup_status=messages.EnumField(StatusType, 3, repeated=True))
    
    
    CASHPLAN_SIGNUP_CANCEL_WITHDRAW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                        cashplan_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                        hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True))

    
    CASHPLAN_SIGNUP_AMEND_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                  cashplan_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                  who=messages.EnumField(WhoLevel, 3, required=True),
                                                                  cover_level=messages.EnumField(CoverLevel, 4, required=True),
                                                                  gross_cost=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True),
                                                                  hashed=messages.StringField(6, variant=messages.Variant.STRING, required=True))
    
    CASHPLAN_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                     cashplan_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                     hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                     status=messages.EnumField(StatusType, 4, required=True)) 
    
    def get_cashplan(self, client_id, user_id):
                                           
        cash_plans = CashplanModel.query(CashplanModel.user == ndb.Key('UserModel', client_id), 
                                         CashplanModel.user_id == user_id).fetch()
        
        if cash_plans:

            return cash_plans
        
        raise ErrorHelper.cp_not_found()
            
            
    def construct_cash_plan(self, cps):
        
        cpsArr = []
        
        for cp in cps:
            
            cp = Cashplan(cashplan_key=cp.key.id(),
                          user_id=cp.user_id,
                          provider_name=cp.provider_name,
                          product_type=cp.product_type,
                          product_variation=cp.product_variation,
                          who=cp.who,
                          premium_who=cp.premium_who,
                          cover_level=cp.cover_level,
                          premium_cover_level=cp.premium_cover_level,
                          premium_core=cp.premium_core,
                          gross_cost=cp.gross_cost)
            
            cpsArr.append(cp)
         
        return CashplanList(cashplan_list=cpsArr)
    
    
    def cashplan_signup_insert(self, user_id, client_id, who, cover_level, gross_cost):
        
        qryCashplan = CashplanModel.query(CashplanModel.user == ndb.Key('UserModel', client_id)).get()
                                          
        if qryCashplan:
        
            qryCashplanSignup = CashplanSignupModel.query(CashplanSignupModel.cashplan==ndb.Key('CashplanModel', qryCashplan.key.id()),
                                                          CashplanSignupModel.user_id==user_id,
                                                          CashplanSignupModel.status==self.get_status_type(3)).get() 

            if qryCashplanSignup:
                
                    raise ErrorHelper.data_already_exists()
            
            else:
                
                status = self.get_status_type(3)
                
                CashplanSignupModel(cashplan=qryCashplan.key,
                                    user=qryCashplan.user,
                                    user_id=user_id,
                                    who=who,
                                    cover_level=cover_level,
                                    gross_cost=gross_cost,
                                    status=status,
                                    token=Token.generate_token()).put()
                                    
                return CashplanSignupResponse(message="Successfully signed up")
        
        else:
            
            raise ErrorHelper.cp_not_found()
        
    def cashplan_signup_list_get(self, user_id, client_id, cashplan_signup_status):
        
        qryCashplanSignup = CashplanSignupModel.query(CashplanSignupModel.user == ndb.Key('UserModel', client_id),
                                                      CashplanSignupModel.user_id == user_id,
                                                      CashplanSignupModel.status.IN(cashplan_signup_status)).fetch()
            
        if qryCashplanSignup:
                
            return qryCashplanSignup
            
        raise ErrorHelper.cp_signup_not_found()
    

    def cashplan_signup_list_auth_get(self, user_status, cashplan_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryCashplanSignup = CashplanSignupModel.query(CashplanSignupModel.user.IN(qryUser),
                                                      CashplanSignupModel.status.IN(cashplan_signup_status)).fetch()
        
        if qryCashplanSignup:
            
            return qryCashplanSignup
        
        raise ErrorHelper.cp_signup_not_found()
    
    
    
    def construct_cashplan_signup_list(self, cashplan_signup_list):
        
        cashplan_signup_listArr = []

        ess_list = EssModel.get_ess(self.get_key_list(cashplan_signup_list))
        
        for cashplan_signup in cashplan_signup_list:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if cashplan_signup.manager:
                
                manager_key = cashplan_signup.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if cashplan_signup.user:
                
                employee_key = cashplan_signup.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
             

            submitted = self.parseDateTimeFormatHyphen(cashplan_signup.submitted)
             
            cashplan_signup = CashplanSignup(user_id=cashplan_signup.user_id,
                                             cashplan_signup_key=cashplan_signup.key.id(),
                                             who=cashplan_signup.who,
                                             cover_level=cashplan_signup.cover_level,
                                             gross_cost=cashplan_signup.gross_cost,
                                             token=cashplan_signup.token,
                                             status=cashplan_signup.status,
                                             manager=ManagerField(firstname=manager_firstname, 
                                                                  lastname=manager_lastname),
                                             employee=EmployeeField(firstname=employee_firstname, 
                                                                    lastname=employee_lastname),
                                             submitted=submitted)
             
            cashplan_signup_listArr.append(cashplan_signup)
             
        return CashplanSignupList(cashplan_signup_list=cashplan_signup_listArr)
    
    
    def cashplan_signup_approval_update(self, client_id, user_id, cashplan_signup_key, hashed, status):
        
        qryCashplanSignup = CashplanSignupModel.query(CashplanSignupModel.key == ndb.Key('CashplanSignupModel', cashplan_signup_key),
                                                      CashplanSignupModel.token == hashed,
                                                      CashplanSignupModel.status == self.get_status_type(3)).get()
        
        
        if qryCashplanSignup:
            
            tokenVar = Token.generate_token()
            
            qryCashplanSignup.token = tokenVar
            qryCashplanSignup.status = status
            qryCashplanSignup.submitted = DateTime.getCurrentDateTime()
            qryCashplanSignup.manager = ndb.Key('UserModel', client_id)
            qryCashplanSignup.put()
        
            return CashplanSignupResponse(message="Successfully %s" % (status))
        
        
        else:

            raise ErrorHelper.cp_signup_not_found()
    
    
    def cashplan_signup_amend_update(self, user_id, cashplan_signup_key, who, cover_level, gross_cost, hashed):
        
        qryCashplanSignup = CashplanSignupModel.query(CashplanSignupModel.key==ndb.Key('CashplanSignupModel', cashplan_signup_key),
                                                      CashplanSignupModel.user_id==user_id,
                                                      CashplanSignupModel.token==hashed,
                                                      CashplanSignupModel.status == self.get_status_type(3)).get()
        
        if qryCashplanSignup:
            
            status = self.get_status_type(3)

            qryCashplanSignup.who = who
            qryCashplanSignup.gross_cost = gross_cost
            qryCashplanSignup.status = status
            qryCashplanSignup.token = Token.generate_token()
            qryCashplanSignup.submitted = DateTime.getCurrentDateTime()
            qryCashplanSignup.put()
            
            return CashplanSignupResponse(message="Successfully amended")
        
        else:
            
            raise ErrorHelper.cp_not_found()
        
    
    
    def cashplan_signup_cancel_update(self, user_id, cashplan_signup_key, hashed):
        
        qryCashplanSignup = CashplanSignupModel.query(CashplanSignupModel.key == ndb.Key('CashplanSignupModel', cashplan_signup_key),
                                                      CashplanSignupModel.user_id == user_id,
                                                      CashplanSignupModel.token == hashed,
                                                      CashplanSignupModel.status == self.get_status_type(1)).get()
        
        if qryCashplanSignup:
            
            status = self.get_status_type(2)
            
            qryCashplanSignup.status = status;
            qryCashplanSignup.submitted = DateTime.getCurrentDateTime()
            qryCashplanSignup.token = Token.generate_token()
            qryCashplanSignup.put()
            
            return CashplanSignupResponse(message="Successfully canceled")
    
        else:
            
            raise ErrorHelper.cp_not_found()
        
    
    def cashplan_signup_withdraw_update(self, user_id, cashplan_signup_key, hashed):
        
        qryCashplanSignup = CashplanSignupModel.query(CashplanSignupModel.key == ndb.Key('CashplanSignupModel', cashplan_signup_key),
                                                      CashplanSignupModel.user_id == user_id,
                                                      CashplanSignupModel.token == hashed,
                                                      CashplanSignupModel.status == self.get_status_type(3)).get()
        
        if qryCashplanSignup:
            
            status = self.get_status_type(4)
            
            qryCashplanSignup.status = status;
            qryCashplanSignup.submitted = DateTime.getCurrentDateTime()
            qryCashplanSignup.token = Token.generate_token()
            qryCashplanSignup.put()
            
            return CashplanSignupResponse(message="Successfully withdraw")
    
        else:
            
            raise ErrorHelper.cp_not_found()
                

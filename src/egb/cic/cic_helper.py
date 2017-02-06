from protorpc import messages
from egb.cic.cic import Cic, CicSignup, CicList, CicSignupList, CicSignupResponse
from egb.cic.cic import CicModel, CicSignupModel
from google.appengine.ext import ndb
from egb.utils.error import ErrorHelper
from libs.tokenGenerate.token import Token
from libs.date_time.date_time import DateTime
from egb.name_field.name_field import EmployeeField, ManagerField, NameFieldHelper
from egb.ess.ess import EssModel
from egb.user.user_helper import UserHelper
from egb.generic.critical_illness import CicTypeHelper, StatusType
from egb.user.user import UserModel
import endpoints
    
class CicHelper(CicTypeHelper, UserHelper, NameFieldHelper):
    
    CIC_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    CIC_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                            cic_signup_status=messages.EnumField(StatusType, 2, repeated=True))
    
    CIC_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                 user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                 cic_signup_status=messages.EnumField(StatusType, 3, repeated=True))
    
    CIC_SIGNUP_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                       window_salary=messages.FloatField(2, variant=messages.Variant.FLOAT, required=True),
                                                       gross_cost=messages.FloatField(3, variant=messages.Variant.FLOAT, required=True),
                                                       multiple=messages.IntegerField(4, variant=messages.Variant.INT32, required=True))
    
    CIC_SIGNUP_AMEND_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                             cic_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                             unit=messages.IntegerField(3, variant=messages.Variant.INT32, required=True),
                                                             gross_cost=messages.FloatField(4, variant=messages.Variant.FLOAT, required=True),
                                                             cover_cost=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True),
                                                             hashed=messages.StringField(6, variant=messages.Variant.STRING, required=True))
    
    CIC_SIGNUP_CANCEL_WITHDRAW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                       cic_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                       hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True))
    
    CIC_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                cic_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                status=messages.EnumField(StatusType, 4, required=True))
    
    
    def get_cic(self, client_id, user_id):
                    
        cics = CicModel.query(CicModel.user == ndb.Key('UserModel', client_id),
                              CicModel.user_id == user_id).fetch()
                              
        if cics:
            
            return cics
        
        raise ErrorHelper.cp_not_found()
    
    
    def construct_cic(self, cics):
        
        cicsArr = []
            
        for cic in cics:
            
            cic = Cic(user_id=cic.user_id,
                    provider_name=cic.provider_name,
                    product_type=cic.product_type,
                    product_variation=cic.product_variation,
                    calculate=cic.calculate,
                    sum_assured=cic.sum_assured,
                    core_multiple=cic.core_multiple,
                    flexible=cic.flexible,
                    flex_multiple=cic.flex_multiple,
                    flex_max_multiple=cic.flex_max_multiple,
                    free_cover_limit=cic.free_cover_limit,
                    cap=cic.cap,
                    premium_core=cic.premium_core,
                    gross_cost=cic.gross_cost,
                    window_salary=cic.window_salary)
            
            cicsArr.append(cic) 
                    
        return CicList(cic_list=cicsArr)
    
    def cic_signup_insert(self, user_id, client_id, window_salary, multiple, gross_cost):
        
        qryCIC = CicModel.query(CicModel.user==ndb.Key('UserModel', client_id)).get()
        
        if qryCIC:
        
            qryCICSignup = CicSignupModel.query(CicSignupModel.cic == qryCIC.key,
                                                CicSignupModel.status == self.get_status_type(3)).get()
        
            if qryCICSignup:

                raise ErrorHelper.data_already_exists()
            
            else:
                
                CicSignupModel(cic=qryCIC.key,
                               user=qryCIC.user,
                               user_id=user_id,
                               window_salary=window_salary,
                               gross_cost=gross_cost,
                               multiple=multiple,
                               status=self.get_status_type(3),
                               token=Token.generate_token()).put()
                
                return CicSignupResponse(message="Successfully signed up")
            
        
    def cic_signup_amend_update(self, user_id, cic_signup_key, unit, gross_cost, cover_cost, hashed):

        qryCICSignup = CicSignupModel.query(CicSignupModel.key==ndb.Key('CicSignupModel', cic_signup_key),
                                              CicSignupModel.user_id==user_id,
                                              CicSignupModel.token==hashed,
                                              ndb.OR(CicSignupModel.status==self.get_status_type(1),
                                                     CicSignupModel.status==self.get_status_type(3))).get()
        
        if qryCICSignup:
            
            status = self.get_status_type(3)
            
            qryCICSignup.unit = unit
            qryCICSignup.gross_cost = gross_cost
            qryCICSignup.cover_cost = cover_cost
            qryCICSignup.status = status
            qryCICSignup.token = Token.generate_token()
            qryCICSignup.submitted = DateTime.getCurrentDateTime()
            qryCICSignup.put()
            
            return CicSignupResponse(message="Successfully amended")
        
        raise ErrorHelper.cic_signup_not_found()
        
    
    
    def cic_signup_approval_update(self, client_id, user_id, cic_signup_key, hashed, status):
        
        qryCICSignup = CicSignupModel.query(CicSignupModel.key == ndb.Key('CicSignupModel', cic_signup_key),
                                            CicSignupModel.token == hashed,
                                            CicSignupModel.status == self.get_status_type(3)).get()
        
        
        if qryCICSignup:
            
            tokenVar = Token.generate_token()
            
            qryCICSignup.token = tokenVar
            qryCICSignup.status = status
            qryCICSignup.submitted = DateTime.getCurrentDateTime()
            qryCICSignup.manager = ndb.Key('UserModel', client_id)
            qryCICSignup.put()
        
            return CicSignupResponse(message="Successfully %s" % (status))
        
        
        raise ErrorHelper.cic_signup_not_found()
        
    
    def cic_signup_list_get(self, user_id, client_id, cic_signup_status):
        
        qryCICSignup = CicSignupModel.query(CicSignupModel.user==ndb.Key('UserModel', client_id),
                                            CicSignupModel.user_id==user_id,
                                            CicSignupModel.status.IN(cic_signup_status)).fetch()
                                                  
        if qryCICSignup:
                
            return qryCICSignup
                                
        raise ErrorHelper.cic_signup_not_found()
                                              
    
    
    def cic_signup_list_auth_get(self, user_status, cic_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryCICSignupAuth = CicSignupModel.query(CicSignupModel.user.IN(qryUser),
                                                CicSignupModel.status.IN(cic_signup_status)).fetch() 

        if qryCICSignupAuth:
            
            return qryCICSignupAuth
            
        raise  ErrorHelper.cic_signup_list_not_found()
    

    def construct_cic_signup_list(self, cic_signup_list):
        
        cic_signup_listArr = []

        ess_list = EssModel.get_ess(self.get_key_list(cic_signup_list))
        
        for cic_signup in cic_signup_list:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if cic_signup.manager:
                
                manager_key = cic_signup.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if cic_signup.user:
                
                employee_key = cic_signup.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
            
            submitted = self.parseDateTimeFormatHyphen(cic_signup.submitted)
                        
            cic_signup_list = CicSignup(user_id=cic_signup.user_id,
                                        cic_signup_key=cic_signup.key.id(),
                                        window_salary=cic_signup.window_salary,
                                        gross_cost=cic_signup.gross_cost,
                                        multiple=cic_signup.multiple,
                                        status=cic_signup.status,
                                        token=cic_signup.token,
                                        submitted=submitted,
                                        manager=ManagerField(firstname=manager_firstname, 
                                                             lastname=manager_lastname),
                                        employee=EmployeeField(firstname=employee_firstname, 
                                                               lastname=employee_lastname))
            
            cic_signup_listArr.append(cic_signup_list) 
            
        return CicSignupList(cic_signup_list=cic_signup_listArr)
        
    
    def cic_signup_cancel_update(self, user_id, cic_signup_key, hashed):

        qryCICSignup = CicSignupModel.query(CicSignupModel.key==ndb.Key('CicSignupModel', cic_signup_key),
                                              CicSignupModel.user_id==user_id,
                                              CicSignupModel.token==hashed,
                                              CicSignupModel.status == self.get_status_type(1)).get()
        
        if qryCICSignup:
            
            status = self.get_status_type(2)

            qryCICSignup.status = status;
            qryCICSignup.submitted = DateTime.getCurrentDateTime()
            qryCICSignup.token = Token.generate_token()
            qryCICSignup.put()
            
            return CicSignupResponse(message="Successfully canceled")
        
        raise ErrorHelper.cic_not_found()
        

    def cic_signup_withdraw_update(self, user_id, cic_signup_key, hashed):
        
        qryCICSignup = CicSignupModel.query(CicSignupModel.key==ndb.Key('CicSignupModel', cic_signup_key),
                                            CicSignupModel.user_id==user_id,
                                            CicSignupModel.token==hashed,
                                            CicSignupModel.status == self.get_status_type(3)).get()
        
        if qryCICSignup:
            
            status = self.get_status_type(4)
            
            qryCICSignup.status = status;
            qryCICSignup.submitted = DateTime.getCurrentDateTime()
            qryCICSignup.token = Token.generate_token()
            qryCICSignup.put()
            
            return CicSignupResponse(message="Successfully withdrawn")
        
        raise ErrorHelper.cic_signup_not_found()


    

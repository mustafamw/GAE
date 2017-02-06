from protorpc import messages
from egb.ctw.ctw import Ctw, CtwList, CtwModel, CtwSignupModel, CtwSignup, CtwSignupList, CtwSignupResponse
from egb.generic.ctw import CtwTypeHelper, StatusType
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
    
class CtwHelper(Parse, CtwTypeHelper, UserHelper, NameFieldHelper):
    
    CTW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    CTW_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))

    CTW_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                 user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                 ctw_signup_status=messages.EnumField(StatusType, 3, repeated=True))

    CTW_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                ctw_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                status=messages.EnumField(StatusType, 4, required=True))
    
    
    def get_ctw(self, client_id, user_id):
                                           
        ctws = CtwModel.query(CtwModel.user == ndb.Key('UserModel', client_id)).fetch()

        if ctws:
            
            return ctws
        
        raise ErrorHelper.ctw_not_found()
    
    def construct_ctw(self, ctws):
        
        ctwsArr = []
        
        for ctw in ctws:
            
            submitted = self.parseDateFormatHyphen(ctw.submitted)
            
            ctw = Ctw(user_id=ctw.user_id,
                      provider_name=ctw.provider_name,
                      product_type=ctw.product_type,
                      product_variation=ctw.product_variation,
                      gross_cost=ctw.gross_cost,
                      status=ctw.status,
                      submitted=submitted)
            
            ctwsArr.append(ctw)
            
        return CtwList(ctw_list = ctwsArr)
    

    def ctw_signup_list_get(self, client_id, user_id):
        
        qryCtwSignup = CtwSignupModel.query(CtwSignupModel.user == ndb.Key('UserModel', client_id),
                                            CtwSignupModel.user_id==user_id).fetch()
        
        if qryCtwSignup:
            
            return qryCtwSignup
        
        raise ErrorHelper.ctw_signup_not_found()
    
    
    def ctw_signup_list_auth_get(self, user_status, ctw_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryCtwSignup = CtwSignupModel.query(CtwSignupModel.user.IN(qryUser),
                                            CtwSignupModel.status.IN(ctw_signup_status)).fetch()
        
        if qryCtwSignup:
            
            return qryCtwSignup
        
        raise ErrorHelper.ctw_signup_not_found()
    
    
    def construct_ctw_signup_list(self, ctw_signup_list):

        ctw_signup_listArr = []
        
        print ctw_signup_list

        ess_list = EssModel.get_ess(self.get_key_list(ctw_signup_list))
        
        for ctw_signup in ctw_signup_list:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if ctw_signup.manager:
                
                manager_key = ctw_signup.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if ctw_signup.user:
                
                employee_key = ctw_signup.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
            
            submitted = self.parseDateTimeFormatHyphen(ctw_signup.submitted)
                        
            ctw_signup_list = CtwSignup(user_id=ctw_signup.user_id,
                                        ctw_signup_key=ctw_signup.key.id(),
                                        gross_cost=ctw_signup.gross_cost,
                                        token=ctw_signup.token,
                                        submitted=submitted,
                                        status=ctw_signup.status,
                                        manager=ManagerField(firstname=manager_firstname, 
                                                             lastname=manager_lastname),
                                        employee=EmployeeField(firstname=employee_firstname, 
                                                               lastname=employee_lastname))
            
            ctw_signup_listArr.append(ctw_signup_list) 
            
        return CtwSignupList(ctw_signup_list=ctw_signup_listArr)


    def ctw_signup_approval_update(self, client_id, user_id, ctw_signup_key, hashed, status):
        
        qryCtwSignup = CtwSignupModel.query(CtwSignupModel.key == ndb.Key('CtwSignupModel', ctw_signup_key),
                                            CtwSignupModel.token == hashed,
                                            CtwSignupModel.status == self.get_status_type(3)).get()
        
        
        if qryCtwSignup:
            
            ctw_key = CtwModel(provider_name=qryCtwSignup.provider_name,
                               product_type=qryCtwSignup.product_type,
                               product_variation=qryCtwSignup.product_variation,
                               user=qryCtwSignup.user,
                               user_id=qryCtwSignup.user_id,
                               status=status,
                               gross_cost=qryCtwSignup.gross_cost)
                     
            ctw_key.put()
            
            tokenVar = Token.generate_token()
            qryCtwSignup.ctw = ctw_key.key
            qryCtwSignup.token = tokenVar
            qryCtwSignup.status = status
            qryCtwSignup.submitted = DateTime.getCurrentDateTime()
            qryCtwSignup.manager = ndb.Key('UserModel', client_id)
            qryCtwSignup.put()               
        
            return CtwSignupResponse(message="Successfully %s" % (status))
        
        
        raise ErrorHelper.ctw_signup_not_found()
    
    
        

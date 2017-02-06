from protorpc import messages
from egb.ccv.ccv import Ccv, CcvList, CcvModel, CcvSignupModel, CcvSignupResponse, CcvSignup, CcvSignupList
from egb.generic.ccv import CcvTypeHelper
from libs.tokenGenerate.token import Token
from libs.date_time.date_time import DateTime
from egb.name_field.name_field import EmployeeField, ManagerField, NameFieldHelper
from egb.user.user_helper import UserHelper
from google.appengine.ext import ndb
from egb.utils.error import ErrorHelper
from egb.generic.ccv import StatusType
from egb.ess.ess import EssModel
from egb.user.user import UserModel
import endpoints
    
class CCVHelper(CcvTypeHelper, UserHelper, NameFieldHelper):
    
    CCV_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    CCV_CONTAINER_SIGNUP = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                       contribution=messages.FloatField(2, variant=messages.Variant.FLOAT, required=True),
                                                       comment=messages.StringField(3, variant=messages.Variant.STRING, required=False))
    
    CCV_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                            ccv_signup_status=messages.EnumField(StatusType, 2, repeated=True))
    
    CCV_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                            user_status=messages.IntegerField(2, required=True),
                                                            ccv_signup_status=messages.EnumField(StatusType, 3, repeated=True))
    
    CCV_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                 user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                 ccv_signup_status=messages.EnumField(StatusType, 3, repeated=True))
    
    CCV_SIGNUP_CANCEL_WITHDRAW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                       ccv_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                       hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True))

    CCV_CONTAINER_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                          ccv_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                          hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                          status=messages.EnumField(StatusType, 4, required=True))
    
    def get_ccv(self, client_id, user_id):
                                           
        qryCcv = CcvModel.query(CcvModel.user == ndb.Key('UserModel',client_id)).fetch()
        
        if qryCcv:
            
            return qryCcv
        
        raise ErrorHelper.ccv_not_found()
    

    def construct_ccv(self, ccvs):
        
        ccvsArr = []
        
        for ccv in ccvs:
            
            ccv = Ccv(user_id=ccv.user_id,
                      provider_name=ccv.provider_name,
                      product_type=ccv.product_type,
                      product_variation=ccv.product_variation,
                      contribution=ccv.contribution,
                      protected_rights=ccv.protected_rights)
            
            ccvsArr.append(ccv)
        
        return CcvList(ccv_list = ccvsArr)
    
    
    def ccv_signup_insert(self, client_id, user_id, contribution, comment):
        
        qryCcv = CcvModel.query(CcvModel.user == ndb.Key('UserModel',client_id)).get()
        
        status = self.get_status_type(3)
        
        if qryCcv:
            
            qryCcvSignup = CcvSignupModel.query(CcvSignupModel.ccv==qryCcv.key,
                                                CcvSignupModel.user_id==user_id,
                                                CcvSignupModel.status==status).get()
            
            if qryCcvSignup:
                
                raise ErrorHelper.data_already_exists()
                
            CcvSignupModel(ccv=qryCcv.key,
                           user=qryCcv.user,
                           user_id=user_id,
                           contribution=contribution,
                           comment=comment,
                           status=status,
                           token=Token.generate_token()).put()
            
            return CcvSignupResponse(message="Successfully signed up")
        
        raise ErrorHelper.ccv_not_found()
    

    def ccv_signup_list_get(self, user_id, client_id, ccv_signup_status):
        
        qryCcvSignup = CcvSignupModel.query(CcvSignupModel.user == ndb.Key('UserModel', client_id),
                                            CcvSignupModel.user_id == user_id,
                                            CcvSignupModel.status.IN(ccv_signup_status)).fetch()
            
        if qryCcvSignup:
                
            return qryCcvSignup
            
        raise ErrorHelper.ccv_signup_not_found()
    

    def ccv_signup_list_auth_get(self, user_status, ccv_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryCcvSignup = CcvSignupModel.query(CcvSignupModel.user.IN(qryUser),
                                            CcvSignupModel.status.IN(ccv_signup_status)).fetch()
        
        if qryCcvSignup:
            
            return qryCcvSignup
        
        raise ErrorHelper.ccv_signup_not_found()
    
    
    
    def construct_ccv_signup_list(self, ccv_signup_list):
        
        ccv_signup_listArr = []

        ess_list = EssModel.get_ess(self.get_key_list(ccv_signup_list))
        
        for ccv_signup in ccv_signup_list:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if ccv_signup.manager:
                
                manager_key = ccv_signup.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if ccv_signup.user:
                
                employee_key = ccv_signup.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
             

            submitted = self.parseDateTimeFormatHyphen(ccv_signup.submitted)
             
            ccv_signup = CcvSignup(user_id=ccv_signup.user_id,
                                   ccv_signup_key=ccv_signup.key.id(),
                                   contribution=ccv_signup.contribution,
                                   comment=ccv_signup.comment,
                                   token=ccv_signup.token,
                                   status=ccv_signup.status,
                                   manager=ManagerField(firstname=manager_firstname, 
                                                        lastname=manager_lastname),
                                   employee=EmployeeField(firstname=employee_firstname, 
                                                          lastname=employee_lastname),
                                   submitted=submitted)
             
            ccv_signup_listArr.append(ccv_signup)
             
        return CcvSignupList(ccv_signup_list=ccv_signup_listArr)
    

    def ccv_signup_approval_update(self, client_id, user_id, ccv_signup_key, hashed, status):
        
        qryCcvSignup = CcvSignupModel.query(CcvSignupModel.key == ndb.Key('CcvSignupModel', ccv_signup_key),
                                            CcvSignupModel.token == hashed,
                                            CcvSignupModel.status == self.get_status_type(3)).get()
        
        
        if qryCcvSignup:
            
            tokenVar = Token.generate_token()
            
            qryCcvSignup.token = tokenVar
            qryCcvSignup.status = status
            qryCcvSignup.submitted = DateTime.getCurrentDateTime()
            qryCcvSignup.manager = ndb.Key('UserModel', client_id)
            qryCcvSignup.put()
        
            if str(status) == 'accept':
                
                qryCcv = CcvModel.query(CcvModel.key == qryCcvSignup.ccv,
                                        CcvModel.user_id == qryCcvSignup.user_id).get()
                print qryCcv                         
                    
                if qryCcv:
                    qryCcv.contribution = qryCcvSignup.contribution
                    qryCcv.put()
            
            return CcvSignupResponse(message="Successfully %s" % (status))
        
        else:

            raise ErrorHelper.ccv_signup_not_found()
        

    def ccv_signup_cancel_update(self, user_id, ccv_signup_key, hashed):
        
        qryCcvSignup = CcvSignupModel.query(CcvSignupModel.key == ndb.Key('CcvSignupModel', ccv_signup_key),
                                               CcvSignupModel.user_id == user_id,
                                               CcvSignupModel.token == hashed,
                                               CcvSignupModel.status == self.get_status_type(1)).get()
        
        if qryCcvSignup:
            
            status = self.get_status_type(2)
            
            qryCcvSignup.status = status;
            qryCcvSignup.submitted = DateTime.getCurrentDateTime()
            qryCcvSignup.token = Token.generate_token()
            qryCcvSignup.put()
            
            return CcvSignupResponse(message="Successfully canceled")
    
        else:
            
            raise ErrorHelper.ccv_signup_not_found()
        
    
    def ccv_signup_withdraw_update(self, user_id, ccv_signup_key, hashed):
        
        qryCcvSignup = CcvSignupModel.query(CcvSignupModel.key == ndb.Key('CcvSignupModel', ccv_signup_key),
                                               CcvSignupModel.user_id == user_id,
                                               CcvSignupModel.token == hashed,
                                               CcvSignupModel.status == self.get_status_type(3)).get()
        
        if qryCcvSignup:
            
            status = self.get_status_type(4)
            
            qryCcvSignup.status = status;
            qryCcvSignup.submitted = DateTime.getCurrentDateTime()
            qryCcvSignup.token = Token.generate_token()
            qryCcvSignup.put()
            qryCcvSignup
            return CcvSignupResponse(message="Successfully withdraw")
    
        else:
            
            raise ErrorHelper.ccv_signup_not_found()

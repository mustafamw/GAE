from google.appengine.ext import ndb
from protorpc import messages
from egb.pmi.pmi import PMI, PMIModel, PMISignup, PMISignupModel, PMISignupResponse, PMISignupList, PMIList
from libs.tokenGenerate.token import Token
from libs.date_time.date_time import DateTime
from egb.generic.pmi import PmiTypeHelper, WhoLevel, StatusType, CoverLevel
from libs.parse.parse import Parse
from egb.ess.ess import EssModel
from egb.name_field.name_field import ManagerField, EmployeeField, NameFieldHelper
from egb.utils.error import ErrorHelper
from egb.user.user_helper import UserHelper
from egb.user.user import UserModel
import endpoints
    
class PmiHelper(Parse, PmiTypeHelper, UserHelper, NameFieldHelper):
    
    PMI_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    PMI_SIGNUP_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                       who=messages.EnumField(WhoLevel, 3, required=True),
                                                       excess=messages.FloatField(4, variant=messages.Variant.FLOAT, required=True),
                                                       gross_cost=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True))
    
    PMI_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                            pmi_signup_status=messages.EnumField(StatusType, 2, repeated=True))
    
    PMI_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                 user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                 pmi_signup_status=messages.EnumField(StatusType, 3, repeated=True))
    
    
    PMI_SIGNUP_CANCEL_WITHDRAW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                       pmi_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                       hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True))

    
    PMI_SIGNUP_AMEND_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                             pmi_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                             who=messages.EnumField(WhoLevel, 3, required=True),
                                                             cover_level=messages.EnumField(CoverLevel, 4, required=True),
                                                             gross_cost=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True),
                                                             hashed=messages.StringField(6, variant=messages.Variant.STRING, required=True))
    
    PMI_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                pmi_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                status=messages.EnumField(StatusType, 4, required=True))
    
    
    def get_pmi(self, client_id, user_id):
        
        pmis = PMIModel.query(PMIModel.user==ndb.Key('UserModel',client_id),
                              PMIModel.user_id == user_id).fetch()
        
        if pmis:

            return pmis
        
        raise ErrorHelper.pmi_not_found()
    
    
    def construct_pmi(self, pmis):
        
        pmisArr = []
        
        for pmi in pmis:
                
            pmi = PMI(pmi_key=pmi.key.id(),
                      user_id=pmi.user_id,
                      provider_name=pmi.provider_name,
                      product_type=pmi.product_type,
                      product_variation=pmi.product_variation,
                      flexible=pmi.flexible,
                      who=pmi.who,
                      premium_who=pmi.premium_who,
                      cover_level=pmi.cover_level,
                      premium_cover_level=pmi.premium_cover_level,
                      where=pmi.where,
                      excess=pmi.excess,
                      premium_core=pmi.premium_core,
                      gross_cost=pmi.gross_cost)
            
            pmisArr.append(pmi)
        
        return PMIList(pmi_list=pmisArr)
    
    
    def pmi_signup_insert(self, user_id, client_id, who, excess, gross_cost):
        
        status = self.get_status_type(3)
        
        qryPMI = PMIModel.query(PMIModel.user == ndb.Key('UserModel', client_id),
                                PMIModel.user_id == user_id).get()
                                
        if qryPMI:
        
            qryPMISignup = PMISignupModel.query(PMISignupModel.pmi==qryPMI.key,
                                                PMISignupModel.user_id==user_id,
                                                PMISignupModel.status==self.get_status_type(3)).get() 
            
            if qryPMISignup:
                
                raise ErrorHelper.data_already_exists()
                
            else:
                
                PMISignupModel(pmi=qryPMI.key,
                               user=qryPMI.user,
                               user_id=user_id,
                               who=who,
                               excess=excess,
                               gross_cost=gross_cost,
                               status=status,
                               token=Token.generate_token()).put()
                
                return PMISignupResponse(message="Successfully signed up")
            
        raise ErrorHelper.pmi_not_found()
        
    def pmi_signup_list_get(self, user_id, client_id, pmi_signup_status):
        
        qryPMISignup = PMISignupModel.query(PMISignupModel.user == ndb.Key('UserModel', client_id),
                                            PMISignupModel.user_id == user_id,
                                            PMISignupModel.status.IN(pmi_signup_status)).order(-PMISignupModel.submitted).fetch()
        
        if qryPMISignup:
        
            return qryPMISignup
        
        raise ErrorHelper.pmi_not_found()
        
    

    def pmi_signup_list_auth_get(self, user_status, pmi_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryPmiSignup = PMISignupModel.query(PMISignupModel.user.IN(qryUser),
                                            PMISignupModel.status.IN(pmi_signup_status)).fetch()
        if qryPmiSignup:

            return qryPmiSignup
        
        raise ErrorHelper.pmi_list_not_found()
            
    
    
    def construct_pmi_signup_list(self, pmi_signup_lists):
        
        pmi_signup_listArr = []
 
        ess_list = EssModel.get_ess(self.get_key_list(pmi_signup_lists))
        
        for pmi_signup_list in pmi_signup_lists:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if pmi_signup_list.manager:
                
                manager_key = pmi_signup_list.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if pmi_signup_list.user:
                
                employee_key = pmi_signup_list.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
            
            submitted = self.parseDateTimeFormatHyphen(pmi_signup_list.submitted)
            
            pmi_signup_list = PMISignup(user_id=pmi_signup_list.user_id,
                                        pmi_signup_key=pmi_signup_list.key.id(),
                                        who=pmi_signup_list.who,
                                        excess=pmi_signup_list.excess,
                                        gross_cost=pmi_signup_list.gross_cost,
                                        token=pmi_signup_list.token,
                                        status=pmi_signup_list.status,
                                        manager=ManagerField(firstname=manager_firstname, 
                                                             lastname= manager_lastname),
                                        employee=EmployeeField(firstname=employee_firstname, 
                                                             lastname=employee_lastname),
                                        submitted=submitted)
            
            pmi_signup_listArr.append(pmi_signup_list)
            
        return PMISignupList(pmi_signup_list=pmi_signup_listArr)
    
    
    def pmi_signup_approval_update(self, client_id, user_id, pmi_signup_key, hashed, status):
        
        qryPMISignup = PMISignupModel.query(PMISignupModel.key == ndb.Key('PMISignupModel', pmi_signup_key),
                                            PMISignupModel.token == hashed,
                                            PMISignupModel.status == self.get_status_type(3)).get()
        
        
        if qryPMISignup:
            
            tokenVar = Token.generate_token()
            
            qryPMISignup.token = tokenVar
            qryPMISignup.status = status
            qryPMISignup.submitted = DateTime.getCurrentDateTime()
            qryPMISignup.manager = ndb.Key('UserModel', client_id)
            qryPMISignup.put()
            
            if str(status) == 'accept':
                
                qryPMI = PMIModel.query(PMIModel.key == qryPMISignup.pmi,
                                        PMIModel.user == qryPMISignup.user,
                                        PMIModel.user_id == qryPMISignup.user_id).get()
                if qryPMI:
                    qryPMI.who = qryPMISignup.who
                    qryPMI.gross_cost = qryPMISignup.gross_cost
                    qryPMI.excess = qryPMISignup.excess
                    qryPMI.put()
        
            return PMISignupResponse(message="Successfully %s" % (status))
        
        
        else:

            raise ErrorHelper.pmi_not_found()
    
    
    def pmi_signup_amend_update(self, user_id, pmi_signup_key, who, cover_level, gross_cost, hashed):
        
        status = self.get_status_type(3)

        qryPMISignup = PMISignupModel.query(PMISignupModel.key==ndb.Key('PMISignupModel', pmi_signup_key),
                                            PMISignupModel.user_id==user_id,
                                            PMISignupModel.token==hashed,
                                            PMISignupModel.status==self.get_status_type(3)).get()
        
        if qryPMISignup:

            qryPMISignup.who = who
            qryPMISignup.gross_cost = gross_cost
            qryPMISignup.status = status
            qryPMISignup.token = Token.generate_token()
            qryPMISignup.submitted = DateTime.getCurrentDateTime()
            qryPMISignup.put()
            
            return PMISignupResponse(message="Successfully amended")
        
        else:
            
            raise ErrorHelper.pmi_not_found()
        
    
    
    def pmi_signup_cancel_update(self, user_id, pmi_signup_key, hashed):
        
        qryPMISignup = PMISignupModel.query(PMISignupModel.key == ndb.Key('PMISignupModel', pmi_signup_key),
                                                      PMISignupModel.user_id == user_id,
                                                      PMISignupModel.token == hashed,
                                                      PMISignupModel.status == PmiTypeHelper.get_status_type(1)).get()
        
        if qryPMISignup:
            
            status = self.get_status_type(2)
            
            qryPMISignup.status = status;
            qryPMISignup.submitted = DateTime.getCurrentDateTime()
            qryPMISignup.token = Token.generate_token()
            qryPMISignup.put()
            
            return PMISignupResponse(message="Successfully canceled")
    
        else:
            
            raise ErrorHelper.pmi_not_found()
        
    
    def pmi_signup_withdraw_update(self, user_id, pmi_signup_key, hashed):
        
        qryPMISignup = PMISignupModel.query(PMISignupModel.key == ndb.Key('PMISignupModel', pmi_signup_key),
                                            PMISignupModel.user_id == user_id,
                                            PMISignupModel.token == hashed,
                                            PMISignupModel.status == PmiTypeHelper.get_status_type(3)).get()
        
        if qryPMISignup:
            
            status = PmiTypeHelper.get_status_type(4)
            
            qryPMISignup.status = status;
            qryPMISignup.submitted = DateTime.getCurrentDateTime()
            qryPMISignup.token = Token.generate_token()
            qryPMISignup.put()
            
            return PMISignupResponse(message="Successfully withdraw")
    
        else:
            
            raise ErrorHelper.pmi_not_found()
                

    
    
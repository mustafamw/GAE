from protorpc import messages
from egb.gip.gip import GipModel, GipSignupModel, GipSignupResponse
from egb.gip.gip import Gip, GipList, GipSignup, GipSignupList
from google.appengine.ext import ndb
from egb.name_field.name_field import ManagerField, EmployeeField, NameFieldHelper
from egb.utils.error import ErrorHelper
from egb.generic.gip import GipTypeHelper, PaymentTermType, DeferredType, StatusType
from libs.parse.parse import Parse
from egb.user.user_helper import UserHelper
from libs.date_time.date_time import DateTime
from libs.tokenGenerate.token import Token
from egb.ess.ess import EssModel
from egb.user.user import UserModel
import endpoints
    
class GipHelper(Parse, GipTypeHelper, UserHelper, NameFieldHelper):
    
    GIP_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    GIP_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                            gip_signup_status=messages.EnumField(StatusType, 2, repeated=True))
    
    GIP_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                 user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                 gip_signup_status=messages.EnumField(StatusType, 3, repeated=True))
    
    GIP_SIGNUP_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                       percentage=messages.FloatField(3, variant=messages.Variant.FLOAT, required=True),
                                                       payment_term=messages.EnumField(PaymentTermType, 4, required=True),
                                                       deferred_period=messages.EnumField(DeferredType, 5, required=False),
                                                       gross_cost=messages.FloatField(6, variant=messages.Variant.FLOAT, required=True))
    
    GIP_SIGNUP_AMEND_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                             gip_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                             earnings=messages.FloatField(3, variant=messages.Variant.FLOAT, required=True),
                                                             deferred=messages.FloatField(4, variant=messages.Variant.FLOAT, required=True),
                                                             payment_term=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True),
                                                             gross_cost=messages.FloatField(6, variant=messages.Variant.FLOAT, required=True),
                                                             hashed=messages.StringField(7, variant=messages.Variant.STRING, required=True))
    
    GIP_SIGNUP_CANCEL_WITHDRAW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                       gip_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                       hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True))
    
    GIP_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                gip_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                status=messages.EnumField(StatusType, 4, required=True))
    
    
    def get_gip(self, client_id, user_id):
                                           
        gips = GipModel.query(GipModel.user == ndb.Key('UserModel', client_id)).fetch()
        
        if gips:
            
            return gips
        
        raise ErrorHelper.gip_not_found()
            
    
    def construct_gip(self, gips):
        
        gipsArr = []
        
        for gip in gips:
            
            gip = Gip(user_id=gip.user_id,
                      provider_name=gip.provider_name,
                      product_type=gip.product_type,
                      product_variation=gip.product_variation,
                      percentage=gip.percentage,
                      premium_percentage=gip.premium_percentage,
                      deferred_period=gip.deferred_period,
                      payment_term=gip.payment_term,
                      flexible=gip.flexible,
                      free_cover_limit=gip.free_cover_limit,
                      payment_period=gip.payment_period,
                      premium_core=gip.premium_core,
                      gross_cost=gip.gross_cost,
                      window_salary=gip.window_salary)
            
            gipsArr.append(gip)
             
            
        return GipList(gip_list=gipsArr)
    
    
    def gip_signup_insert(self, user_id, client_id, percentage, deferred_period, payment_term, gross_cost):
        
        status = self.get_status_type(3)
        
        qryGIP = GipModel.query(GipModel.user == ndb.Key('UserModel', client_id)).get()
        
        if qryGIP:
            
            qryGIPSignup = GipSignupModel.query(GipSignupModel.gip==qryGIP.key,
                                                GipSignupModel.status == self.get_status_type(3)).get()
            
            if qryGIPSignup:
                 
                raise ErrorHelper.data_already_exists()
            
            else:
                
                GipSignupModel(gip=qryGIP.key,
                               user=qryGIP.user,
                               user_id=user_id,
                               percentage=percentage,
                               deferred_period=deferred_period,
                               payment_term=payment_term,
                               gross_cost=gross_cost,
                               status=status,
                               token=Token.generate_token()).put()
                
                return GipSignupResponse(message="Successfully signed up")
        
        raise ErrorHelper.gip_not_found()
            
        
    def gip_signup_amend_update(self, user_id, gip_signup_key, earnings, deferred, payment_term, gross_cost, hashed):

        qryGIPSignup = GipSignupModel.query(GipSignupModel.key==ndb.Key('GipSignupModel', gip_signup_key),
                                            GipSignupModel.user_id==user_id,
                                            GipSignupModel.token==hashed,
                                            ndb.OR(GipSignupModel.status==self.get_status_type(1),
                                                   GipSignupModel.status==self.get_status_type(3))).get()
        
        if qryGIPSignup:
            
            status = self.get_status_type(3)
            earnings = self.get_earnings_type(earnings)
            deferred = self.get_deferred_type(deferred)
            payment_term = self.get_payment_term_type(payment_term)
            
            qryGIPSignup.earnings = earnings
            qryGIPSignup.deferred = deferred
            qryGIPSignup.payment_term = payment_term
            qryGIPSignup.gross_cost = gross_cost
            qryGIPSignup.status = status
            qryGIPSignup.token = Token.generate_token()
            qryGIPSignup.submitted = DateTime.getCurrentDateTime()
            qryGIPSignup.put()
            
            return GipSignupResponse(message="Successfully amended")
        
        raise ErrorHelper.gip_signup_not_found()
        
    
    
    def gip_signup_approval_update(self, client_id, user_id, gip_signup_key, hashed, status):
        
        qryGIPSignup = GipSignupModel.query(GipSignupModel.key == ndb.Key('GipSignupModel', gip_signup_key),
                                            GipSignupModel.token == hashed,
                                            GipSignupModel.status == self.get_status_type(3)).get()

        if qryGIPSignup:
            
            tokenVar = Token.generate_token()
            
            qryGIPSignup.token = tokenVar
            qryGIPSignup.status = status
            qryGIPSignup.submitted = DateTime.getCurrentDateTime()
            qryGIPSignup.manager = ndb.Key('UserModel', client_id)
            qryGIPSignup.put()
            
            if str(status) == 'accept':
                qryGip = GipModel.query(GipModel.key == qryGIPSignup.gip,
                                        GipModel.user_id == qryGIPSignup.user_id).get()
                                        
                qryGip.window_salary = qryGIPSignup.window_salary
                qryGip.payment_term = qryGIPSignup.payment_term
                qryGip.gross_cost = qryGIPSignup.gross_cost
                qryGip.percentage = qryGIPSignup.percentage
                qryGip.put()
        
            return GipSignupResponse(message="Successfully %s" % (status))
        
        
        raise ErrorHelper.gip_signup_not_found()
        
    
    def gip_signup_list_get(self, client_id, user_id, gip_signup_status):
        
        qryGIPSignup = GipSignupModel.query(GipSignupModel.user==ndb.Key('UserModel', client_id),
                                            GipSignupModel.user_id==user_id,
                                            GipSignupModel.status.IN(gip_signup_status)).fetch()
                                                  
        if qryGIPSignup:
                
            return qryGIPSignup
                                                  
        raise ErrorHelper.gip_signup_not_found() 
                                              
    
    
    def gip_signup_list_auth_get(self, user_status, gip_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryGipSignup = GipSignupModel.query(GipSignupModel.user.IN(qryUser),
                                            GipSignupModel.status == self.get_status_type(3)).fetch() 
        
        if qryGipSignup:
            
            return qryGipSignup
        
        
        raise  ErrorHelper.gip_signup_not_found()
    

    def construct_gip_signup_list(self, gip_signup_list):
        
        gip_signup_listArr = []
        
        ess_list = EssModel.get_ess(self.get_key_list(gip_signup_list))
        
        for gip_signup in gip_signup_list:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if gip_signup.manager:
                
                manager_key = gip_signup.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if gip_signup.user:
                
                employee_key = gip_signup.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
            
            submitted = self.parseDateTimeFormatHyphen(gip_signup.submitted)
                        
            gip_signup_list = GipSignup(user_id=gip_signup.user_id,
                                        gip_signup_key=gip_signup.key.id(),
                                        window_salary=gip_signup.window_salary,
                                        percentage=gip_signup.percentage,
                                        deferred_period=gip_signup.deferred_period,
                                        payment_term=gip_signup.payment_term,
                                        gross_cost=gip_signup.gross_cost,
                                        status=gip_signup.status,
                                        token=gip_signup.token,
                                        submitted=submitted,
                                        manager=ManagerField(firstname=manager_firstname, 
                                                             lastname=manager_lastname),
                                        employee=EmployeeField(firstname=employee_firstname, 
                                                               lastname=employee_lastname))
            
            gip_signup_listArr.append(gip_signup_list) 
            
        return GipSignupList(gip_signup_list=gip_signup_listArr)
        
    
    def gip_signup_cancel_update(self, user_id, gip_signup_key, hashed):

        qryGIPSignup = GipSignupModel.query(GipSignupModel.key==ndb.Key('GipSignupModel', gip_signup_key),
                                            GipSignupModel.user_id==user_id,
                                            GipSignupModel.token==hashed,
                                            GipSignupModel.status == self.get_status_type(1)).get()
        
        if qryGIPSignup:
            
            status = self.get_status_type(2)

            qryGIPSignup.status = status;
            qryGIPSignup.submitted = DateTime.getCurrentDateTime()
            qryGIPSignup.token = Token.generate_token()
            qryGIPSignup.put()
            
            return GipSignupResponse(message="Successfully canceled")
        
        raise ErrorHelper.gip_not_found()
        

    def gip_signup_withdraw_update(self, user_id, gip_signup_key, hashed):

        qryGIPSignup = GipSignupModel.query(GipSignupModel.key==ndb.Key('GipSignupModel', gip_signup_key),
                                             GipSignupModel.user_id==user_id,
                                             GipSignupModel.token==hashed,
                                             GipSignupModel.status == self.get_status_type(3)).get()
        
        if qryGIPSignup:
            
            status = self.get_status_type(4)
            
            qryGIPSignup.status = status;
            qryGIPSignup.submitted = DateTime.getCurrentDateTime()
            qryGIPSignup.token = Token.generate_token()
            qryGIPSignup.put()
            
            return GipSignupResponse(message="Successfully withdrawn")
        
        raise ErrorHelper.gip_not_found()




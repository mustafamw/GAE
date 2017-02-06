from protorpc import messages
from egb.life.life import Life, LifeList, LifeSignupResponse, LifeSignup, LifeSignupList
from egb.life.life import LifeModel, LifeSignupModel
from egb.name_field.name_field import ManagerField, EmployeeField, NameFieldHelper
from google.appengine.ext import ndb
import endpoints
from egb.utils.error import ErrorHelper
from libs.date_time.date_time import DateTime
from egb.generic.life import LifeTypeHelper, StatusType
from libs.tokenGenerate.token import Token
from libs.parse.parse import Parse
from egb.user.user_helper import UserHelper
from egb.ess.ess import EssModel
from egb.user.user import UserModel

    
class LifeHelper(Parse, LifeTypeHelper, UserHelper, NameFieldHelper):
    
    LIFE_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    LIFE_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                             life_signup_status=messages.EnumField(StatusType, 2, repeated=True))
    
    LIFE_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                  user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                  life_signup_status=messages.EnumField(StatusType, 3, repeated=True))
    
    LIFE_SIGNUP_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                        multiple=messages.FloatField(2, variant=messages.Variant.FLOAT, required=True),
                                                        gross_cost=messages.FloatField(3, variant=messages.Variant.FLOAT, required=True))
    
    LIFE_SIGNUP_AMEND_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                        life_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                        selected_multiple=messages.FloatField(3, variant=messages.Variant.FLOAT, required=True),
                                                        gross_cost=messages.FloatField(4, variant=messages.Variant.FLOAT, required=True),
                                                        hashed=messages.StringField(5, variant=messages.Variant.STRING, required=True))
    
    LIFE_SIGNUP_CANCEL_WITHDRAW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                        life_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                        hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True))
    
    LIFE_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                        life_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                        hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                        status=messages.EnumField(StatusType, 4, required=True))
    
    def get_life(self, client_id):   
               
        lifes = LifeModel.query(LifeModel.user == ndb.Key('UserModel', client_id)).fetch()
        
        if lifes:
        
            return lifes
        
        raise ErrorHelper.life_not_found()
    
    
    def construct_life(self, lifes):
        
        lifesArr = []
        
        for life in lifes:
                    
            life = Life(life_key=life.key.id(),
                        user_id=life.user_id,
                        provider_name=life.provider_name,
                        product_type=life.product_type,
                        product_variation=life.product_variation,
                        calculate=life.calculate,
                        sum_assured=life.sum_assured,
                        core_multiple=life.core_multiple,
                        flexible=life.flexible,
                        flex_multiple=life.flex_multiple,
                        flex_max_multiple=life.flex_max_multiple,
                        free_cover_limit=life.free_cover_limit,
                        cap=life.cap,
                        premium_core=life.premium_core,
                        gross_cost=life.gross_cost,
                        window_salary=life.window_salary,
                        wish_expression_link=life.wish_expression_link)
            
            lifesArr.append(life) 
            
        return LifeList(life_list=lifesArr)
    
    
    def life_signup_insert(self, user_id, client_id, multiple, gross_cost):
        
        status = self.get_status_type(3)
            
        qryLife = LifeModel.query(LifeModel.user==ndb.Key('UserModel', client_id),
                                  LifeModel.user_id==user_id).get()
        
        if qryLife:
            
            qryLifeSignup = LifeSignupModel.query(LifeSignupModel.life == qryLife.key,
                                                  LifeSignupModel.user_id == user_id,
                                                  LifeSignupModel.status == self.get_status_type(3)).get()
        
            if qryLifeSignup:
                
                raise ErrorHelper.data_already_exists()
        
            else:
                LifeSignupModel(life=qryLife.key,
                                user=ndb.Key('UserModel', client_id),
                                user_id=user_id,
                                multiple=multiple,
                                gross_cost=gross_cost,
                                status=status,
                                token=Token.generate_token()).put()
                                
                return LifeSignupResponse(message="Successfully Signed up") 
            
        raise ErrorHelper.life_not_found()
            
        
    def life_signup_amend_update(self, user_id, life_signup_key, selected_multiple, gross_cost, hashed):

        qryLifeSignup = LifeSignupModel.query(LifeSignupModel.key==ndb.Key('LifeSignupModel', life_signup_key),
                                              LifeSignupModel.user_id==user_id,
                                              LifeSignupModel.token==hashed,
                                              ndb.OR(LifeSignupModel.status==self.get_status_type(1),
                                                     LifeSignupModel.status==self.get_status_type(3))).get()
        
        if qryLifeSignup:
            
            status = self.get_status_type(3)
            
            qryLifeSignup.selected_multiple = selected_multiple
            qryLifeSignup.gross_cost = gross_cost
            qryLifeSignup.status = status
            qryLifeSignup.token = Token.generate_token()
            qryLifeSignup.submitted = DateTime.getCurrentDateTime()
            qryLifeSignup.put()
            
            return LifeSignupResponse(message="Successfully amended")
        
        raise ErrorHelper.life_signup_not_found()
        
    
    
    def life_signup_approval_update(self, client_id, user_id, life_signup_key, hashed, status):
        
        qryLifeSignup = LifeSignupModel.query(LifeSignupModel.key == ndb.Key('LifeSignupModel', life_signup_key),
                                              LifeSignupModel.token == hashed,
                                              LifeSignupModel.status == self.get_status_type(3)).get()
        
        
        if qryLifeSignup:
            
            tokenVar = Token.generate_token()
            
            qryLifeSignup.token = tokenVar
            qryLifeSignup.status = status
            qryLifeSignup.submitted = DateTime.getCurrentDateTime()
            qryLifeSignup.manager = ndb.Key('UserModel', client_id)
            qryLifeSignup.put()
            
            if str(status) == 'accept':
                qryLife = LifeModel.query(LifeModel.key == qryLifeSignup.life,
                                          LifeModel.user_id == user_id).get()
                if qryLife:
                    
                    qryLife.window_salary = qryLifeSignup.window_salary
                    qryLife.flex_multiple  = qryLifeSignup.multiple
                    qryLife.gross_cost = qryLifeSignup.gross_cost
                    qryLife.put()
        
            return LifeSignupResponse(message="Successfully %s" % (status))
        
        
        raise ErrorHelper.life_signup_not_found()
        
    
    def life_signup_list_get(self, user_id, client_id, life_signup_status):
        
        qryLifeSignup = LifeSignupModel.query(LifeSignupModel.user==ndb.Key('UserModel', client_id),
                                              LifeSignupModel.user_id==user_id,
                                              LifeSignupModel.status.IN(life_signup_status)).fetch()
                                                  
        if qryLifeSignup:
                
            return qryLifeSignup
                                                  
        raise ErrorHelper.life_signup_not_found() 
                                              
    
    
    def life_signup_list_auth_get(self, user_status, life_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
            
        qryLifeSignup = LifeSignupModel.query(LifeSignupModel.user.IN(qryUser),
                                              LifeSignupModel.status.IN(life_signup_status)).fetch()
        
        if qryLifeSignup:
            
            return qryLifeSignup
            
        raise  ErrorHelper.life_list_not_found()
    

    def construct_life_signup_list(self, life_signup_list):
        
        life_signup_listArr = []

        ess_list = EssModel.get_ess(self.get_key_list(life_signup_list))
        
        for lifes_signup in life_signup_list:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if lifes_signup.manager:
                
                manager_key = lifes_signup.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if lifes_signup.user:
                
                employee_key = lifes_signup.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
            
            submitted = self.parseDateTimeFormatHyphen(lifes_signup.submitted)
                        
            life_signup_list = LifeSignup(user_id=lifes_signup.user_id,
                                          life_signup_key=lifes_signup.key.id(),
                                          window_salary=lifes_signup.window_salary,
                                          multiple=lifes_signup.multiple,
                                          gross_cost=lifes_signup.gross_cost,
                                          status=lifes_signup.status,
                                          token=lifes_signup.token,
                                          submitted=submitted,
                                          manager=ManagerField(firstname=manager_firstname, 
                                                               lastname=manager_lastname),
                                          employee=EmployeeField(firstname=employee_firstname, 
                                                                 lastname=employee_lastname))
            
            life_signup_listArr.append(life_signup_list) 
            
        return LifeSignupList(life_signup_list=life_signup_listArr)
        
    
    def life_signup_cancel_update(self, user_id, life_signup_key, hashed):

        qryLifeSignup = LifeSignupModel.query(LifeSignupModel.key==ndb.Key('LifeSignupModel', life_signup_key),
                                              LifeSignupModel.user_id==user_id,
                                              LifeSignupModel.token==hashed,
                                              LifeSignupModel.status == self.get_status_type(1)).get()
        
        if qryLifeSignup:
            
            status = self.get_status_type(2)

            qryLifeSignup.status = status;
            qryLifeSignup.submitted = DateTime.getCurrentDateTime()
            qryLifeSignup.token = Token.generate_token()
            qryLifeSignup.put()
            
            return LifeSignupResponse(message="Successfully canceled")
        
        raise ErrorHelper.life_not_found()
        

    def life_signup_withdraw_update(self, user_id, life_signup_key, hashed):

        qryLifeSignup = LifeSignupModel.query(LifeSignupModel.key==ndb.Key('LifeSignupModel', life_signup_key),
                                              LifeSignupModel.user_id==user_id,
                                              LifeSignupModel.token==hashed,
                                              LifeSignupModel.status == self.get_status_type(3)).get()
        
        if qryLifeSignup:
            
            status = self.get_status_type(4)
            
            qryLifeSignup.status = status;
            qryLifeSignup.submitted = DateTime.getCurrentDateTime()
            qryLifeSignup.token = Token.generate_token()
            qryLifeSignup.put()
            
            return LifeSignupResponse(message="Successfully withdrawn")
        
        raise ErrorHelper.life_signup_not_found()


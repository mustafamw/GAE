from protorpc import messages
from egb.ess.ess import EssModel
from egb.pension.pension import PensionModel, PensionSignupModel, PensionSignup, PensionSignupList, FundSelection, ListFund, FundSelectionModel, ListFundModel
from egb.pension.pension import Pension, PensionList, PensionSignupResponse
from egb.generic.pension import PensionTypeHelper, TaxSavingType, StatusType
from egb.utils.error import ErrorHelper
from google.appengine.ext import ndb
from libs.parse.parse import Parse
from libs.tokenGenerate.token import Token
from libs.date_time.date_time import DateTime
from egb.name_field.name_field import ManagerField, EmployeeField, NameFieldHelper
from egb.user.user_helper import UserHelper
import endpoints
from egb.user.user import UserModel
    
class PensionHelper(Parse, PensionTypeHelper, UserHelper, NameFieldHelper):
    
    PENSION_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    PENSION_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                         user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True))
    
    PENSION_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                pension_signup_status=messages.EnumField(StatusType, 2, repeated=True))
    
    PENSION_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                     user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                     pension_signup_status=messages.EnumField(StatusType, 3, repeated=True))
    
    PENSION_SIGNUP_CANCEL_WITHDRAW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                  pension_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                  hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True))
    
    PENSION_SIGNUP_WITHDRAW_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                  pension_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True))
    
    PENSION_SIGNUP_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                           contribution=messages.FloatField(3, variant=messages.Variant.FLOAT, required=True),
                                                           employee_contribution_percent=messages.FloatField(4, variant=messages.Variant.FLOAT, required=True),
                                                           employer_contribution=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True),
                                                           employer_contribution_percent=messages.FloatField(6, variant=messages.Variant.FLOAT, required=True),
                                                           tax_saving=messages.EnumField(TaxSavingType, 8, required=True),
                                                           retirement_age=messages.IntegerField(10, variant=messages.Variant.INT32, required=True),
                                                           list_fund=messages.StringField(11, variant=messages.Variant.STRING, required=False),
                                                           fund_selection=messages.StringField(12, variant=messages.Variant.STRING, required=True))
    
    PENSION_SIGNUP_AMEND_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                 contribution=messages.FloatField(2, variant=messages.Variant.FLOAT, required=True),
                                                                 employee_contribution_percent=messages.FloatField(3, variant=messages.Variant.FLOAT, required=True),
                                                                 employer_contribution=messages.FloatField(4, variant=messages.Variant.FLOAT, required=True),
                                                                 employer_contribution_percent=messages.FloatField(5, variant=messages.Variant.FLOAT, required=True),
                                                                 tax_saving=messages.EnumField(TaxSavingType, 6, required=True),
                                                                 fund_selection=messages.StringField(7, variant=messages.Variant.STRING))
    
    PENSION_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                    pension_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                    hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                    status=messages.EnumField(StatusType, 4, required=True))     
    
    
    
    def get_pension(self, client_id, user_id):
        
        pensions = PensionModel.query(PensionModel.user == ndb.Key('UserModel', client_id)).fetch()
                                      
        if pensions:
            
            return pensions
        
        raise ErrorHelper.pension_not_found()
    
    
    def construct_pension(self, pensions):
        
        pensionsArr = []
        
        for pension in pensions:

        
            start_date = self.parseDateFormatHyphen(pension.start_date)
            end_date = self.parseDateFormatHyphen(pension.end_date)
            valuation_date = self.parseDateFormatHyphen(pension.valuation_date)
            submitted = self.parseDateTimeFormatHyphen(pension.submitted)
            
            list_fundArr = []
            if pension.list_fund:
                for fund in pension.list_fund:
                    list_fundArr.append(ListFund(name=fund.name, value=fund.value))
            
            fund_selectionArr = []
            if pension.fund_selection:
                for selection in pension.fund_selection:
                    fund_selectionArr.append(FundSelection(name=selection.name, percent=selection.percent))
            
            pension = Pension(user_id=pension.user_id,
                              pension_key = pension.key.id(),
                              provider_name=pension.provider_name,
                              product_type=pension.product_type,
                              product_variation=pension.product_variation,
                              start_date=start_date,
                              end_date=end_date,
                              fund_value=pension.fund_value,
                              valuation_date=valuation_date,
                              employee_contribution=pension.employee_contribution,
                              employer_contribution=pension.employer_contribution,
                              employee_contribution_percent=pension.employee_contribution_percent,
                              employer_contribution_percent=pension.employer_contribution_percent,
                              min_employee_contribution_percent=pension.min_employee_contribution_percent,
                              max_employee_contribution_percent=pension.max_employee_contribution_percent,
                              min_employer_contribution_percent=pension.min_employer_contribution_percent,
                              max_employer_contribution_percent=pension.max_employer_contribution_percent,
                              tax_saving = pension.tax_saving,
                              saving_value = pension.saving_value,
                              wish_expression_link=pension.wish_expression_link,
                              list_fund=list_fundArr,
                              fund_selection=fund_selectionArr,
                              submitted=submitted)
            
            pensionsArr.append(pension) 
            
        return PensionList(pension_list = pensionsArr)
    
    
    def pension_signup_insert(self, user_id, client_id, employee_contribution, employee_contribution_percent, employer_contribution, employer_contribution_percent, tax_saving, retirement_age, list_fund, fund_selection):

        status = self.get_status_type(3)

        list_fundArr = []
        if list_fund:
            for fund in list_fund.split(','):
                fund = fund.split('|') 
                list_fundArr.append(ListFundModel(name=fund[0], value=float(fund[1])))
        
        fund_selectionArr = []
        if fund_selection:
            for selection in fund_selection.split(','):
                print selection
                selection = selection.split('|')
                fund_selectionArr.append(FundSelectionModel(name=selection[0], percent=float(selection[1])))
        
        qryPension = PensionModel.query(PensionModel.user == ndb.Key('UserModel', client_id)).get()
        
        if qryPension:
            
            qryPensionSignup = PensionSignupModel.query(PensionSignupModel.pension==ndb.Key('PensionModel', qryPension.key.id()),
                                                        PensionSignupModel.user_id==user_id,
                                                        PensionSignupModel.status == self.get_status_type(3)).get()
            if not qryPensionSignup:
        
                PensionSignupModel(pension=ndb.Key('PensionModel', qryPension.key.id()),
                                   user_id=user_id,
                                   user=ndb.Key('UserModel', client_id),
                                   employee_contribution=employee_contribution,
                                   employee_contribution_percent=employee_contribution_percent,
                                   employer_contribution=employer_contribution,
                                   employer_contribution_percent=employer_contribution_percent,
                                   tax_saving=tax_saving,
                                   retirement_age=retirement_age,
                                   list_fund=list_fundArr,
                                   fund_selection=fund_selectionArr,
                                   token=Token.generate_token(),
                                   status=status).put()
            
                return PensionSignupResponse(message="Successfully signed up")
            
            raise ErrorHelper.pension_signup_pending()
        
        else:
            
            raise ErrorHelper.pension_not_found()


    def pension_signup_amend_update(self, client_id, user_id, employee_contribution, employee_contribution_percent, employer_contribution, employer_contribution_percent, tax_saving, fund_selection):

        fund_selectionArr = []
        if fund_selection:
            for selection in fund_selection.split(','):
                selection = selection.split('|')
                fund_selectionArr.append(FundSelectionModel(name=selection[0], percent=float(selection[1])))

        qryPension = PensionModel.query(PensionModel.user == ndb.Key('UserModel', client_id)).get()
        
        if qryPension:
            
            qryPensionSignupPending = PensionSignupModel.query(PensionSignupModel.pension == ndb.Key('PensionModel', qryPension.key.id()),
                                                               PensionSignupModel.status == self.get_status_type(3)).get()
            
            if qryPensionSignupPending:
                
                raise ErrorHelper.pension_signup_pending()
        
            else:
                
                status = self.get_status_type(3)
            
                PensionSignupModel(pension=ndb.Key('PensionModel', qryPension.key.id()),
                                   user=ndb.Key('UserModel', client_id),
                                   user_id=user_id,
                                   employee_contribution=employee_contribution,
                                   employee_contribution_percent=employee_contribution_percent,
                                   employer_contribution=employer_contribution,
                                   employer_contribution_percent=employer_contribution_percent,
                                   tax_saving=tax_saving,
                                   fund_selection=fund_selectionArr,
                                   token=Token.generate_token(),
                                   status=status).put()
        
                return PensionSignupResponse(message="Successfully amended")
            
            
        raise ErrorHelper.pension_not_found()
        
    
    def pension_signup_approval_update(self, client_id, user_id, pension_signup_key, hashed, status):
        
        qryPensionSignup = PensionSignupModel.query(PensionSignupModel.key == ndb.Key('PensionSignupModel', pension_signup_key),
                                                    PensionSignupModel.token == hashed,
                                                    PensionSignupModel.status == self.get_status_type(3)).get()
                                                    
        if qryPensionSignup:
            
            tokenVar = Token.generate_token()
            
            qryPensionSignup.token = tokenVar
            qryPensionSignup.status = status
            qryPensionSignup.submitted = DateTime.getCurrentDateTime()
            qryPensionSignup.manager = ndb.Key('UserModel', client_id)
            qryPensionSignup.put()
            
            if str(status) == 'accept':
                qryPension = PensionModel.query(PensionModel.key == qryPensionSignup.pension,
                                                PensionModel.user_id == user_id).get()
                                            
                print qryPension
                
                qryPension.contribution = qryPensionSignup.contribution
                qryPension.employer_contribution = qryPensionSignup.employer_contribution 
                qryPension.employee_contribution_percent = qryPensionSignup.employee_contribution_percent
                qryPension.employer_contribution_percent = qryPensionSignup.employer_contribution_percent
                qryPension.tax_saving = qryPensionSignup.tax_saving
                qryPension.saving_value 
                qryPension.list_fund = qryPensionSignup.list_fund           
                qryPension.fund_selection = qryPensionSignup.fund_selection
                qryPension.submitted = DateTime.getCurrentDateTime()
                qryPension.put()
                
            return PensionSignupResponse(message="Successfully %s" % (status))
        
        raise ErrorHelper.pension_not_found()
        
        
    
    def pension_signup_cancel_update(self, user_id, pension_signup_key, hashed):
        
        qryPensionSignup = PensionSignupModel.query(PensionSignupModel.key == ndb.Key('PensionSignupModel', pension_signup_key),
                                                    PensionSignupModel.user_id == user_id,
                                                    PensionSignupModel.token == hashed,
                                                    PensionSignupModel.status == self.get_status_type(1)).get()
        
        if qryPensionSignup:
            
            status = self.get_status_type(2)
            
            tokenVar = Token.generate_token()
            qryPensionSignup.token = tokenVar
            qryPensionSignup.status = status
            qryPensionSignup.submitted = DateTime.getCurrentDateTime()
            qryPensionSignup.put()
        
            return PensionSignupResponse(message="Successfully canceled")
        
        raise ErrorHelper.pension_signup_not_found()
        
    
    def pension_signup_withdraw_update(self, user_id, pension_signup_key, hashed):
        
        qryPensionSignup = PensionSignupModel.query(PensionSignupModel.key == ndb.Key('PensionSignupModel', pension_signup_key),
                                                    PensionSignupModel.user_id == user_id,
                                                    PensionSignupModel.status == self.get_status_type(3),
                                                    PensionSignupModel.token == hashed).get()
        print qryPensionSignup
    
        if qryPensionSignup:
            
            status = self.get_status_type(4)
            tokenVar = Token.generate_token()
            qryPensionSignup.token = tokenVar
            qryPensionSignup.status = status
            qryPensionSignup.submitted = DateTime.getCurrentDateTime()
            qryPensionSignup.put()
        
            return PensionSignupResponse(message="Successfully withdrawn")
        
        raise ErrorHelper.pension_signup_not_found()
        
        
    def pension_signup_list_get(self, user_id, client_id, pension_signup_status):
        
        pension_signup_list =  PensionSignupModel.query(PensionSignupModel.user == ndb.Key('UserModel', client_id),
                                                        PensionSignupModel.user_id == user_id,
                                                        PensionSignupModel.status.IN(pension_signup_status)).order(-PensionSignupModel.submitted).fetch()
        
        if pension_signup_list:
                
            return pension_signup_list
           
        raise ErrorHelper.pension_list_not_found()

        
        
    def pension_signup_list_auth_get(self, user_status, pension_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
    
        pension_signup_list =  PensionSignupModel.query(PensionSignupModel.user.IN(qryUser),
                                                        PensionSignupModel.status.IN(pension_signup_status)).fetch()
        
        if pension_signup_list:
            
            return pension_signup_list
       
        raise ErrorHelper.pension_list_not_found()
        
        
    def construct_pension_list(self, pensions_list):
        
        pensions_listArr = []
            
        ess_list = EssModel.get_ess(self.get_key_list(pensions_list))    
        
        for pensions_list in pensions_list:
            
            list_fundArr = []
            if pensions_list.list_fund:
                for fund in pensions_list.list_fund:
                    list_fundArr.append(ListFund(name=fund.name, value=fund.value))
            
            fund_selectionArr = []
            if pensions_list.fund_selection:
                for selection in pensions_list.fund_selection:
                    fund_selectionArr.append(FundSelection(name=selection.name, percent=selection.percent))
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if pensions_list.manager:
                
                manager_key = pensions_list.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if pensions_list.user:
                
                employee_key = pensions_list.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
            
            submitted = self.parseDateTimeFormatHyphen(pensions_list.submitted)
             
            pensions_list = PensionSignup(user_id=pensions_list.user_id,
                                          pension_signup_key = pensions_list.key.id(),
                                          employee_contribution=pensions_list.contribution,
                                          employer_contribution=pensions_list.employer_contribution,
                                          employee_contribution_percent=pensions_list.employee_contribution_percent,
                                          employer_contribution_percent=pensions_list.employer_contribution_percent,
                                          total_contribution=pensions_list.total_contribution,
                                          tax_saving=pensions_list.tax_saving,
                                          saving_value=pensions_list.saving_value,
                                          token=pensions_list.token,
                                          list_fund=list_fundArr,
                                          fund_selection=fund_selectionArr,
                                          status=pensions_list.status,
                                          manager=ManagerField(firstname=manager_firstname, 
                                                               lastname=manager_lastname),
                                          employee=EmployeeField(firstname=employee_firstname, 
                                                                 lastname=employee_lastname),
                                          submitted=submitted)
             
            pensions_listArr.append(pensions_list)
         
        return PensionSignupList(pensions_signup_list=pensions_listArr)
        
        


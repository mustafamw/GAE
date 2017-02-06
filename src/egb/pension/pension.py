from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.pension import TaxSavingType
from egb.generic.pension import StatusType
from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
from egb.user.user import UserModel
from egb.name_field.name_field import ManagerField, EmployeeField


class PensionTrs(messages.Message):
    employer_contribution = messages.FloatField(1, required=True)
    employer_contribution_percentage = messages.FloatField(2, required=True)


class ListFund(messages.Message):
    name = messages.StringField(1, required=True)
    value = messages.FloatField(2, required=True)
    

class FundSelection(messages.Message):
    name = messages.StringField(1, required=True)
    percent = messages.FloatField(2, required=True)


class Pension(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    provider_name = messages.StringField(2, required=False)
    product_type = messages.EnumField(ProductType, 3, required=False)
    product_variation = messages.EnumField(ProductVariation, 4, required=False)
    start_date = messages.StringField(5, required=False)
    end_date = messages.StringField(6, required=False)
    fund_value = messages.FloatField(7, required=False)
    valuation_date = messages.StringField(8, required=False)
    employee_contribution = messages.FloatField(9, required=False)
    employer_contribution = messages.FloatField(10, required=False)
    employee_contribution_percent = messages.FloatField(11, required=False)       
    employer_contribution_percent = messages.FloatField(12, required=True)
    min_employee_contribution_percent = messages.FloatField(13, required=True)       
    max_employee_contribution_percent = messages.FloatField(14, required=True)
    min_employer_contribution_percent = messages.FloatField(15, required=True)       
    max_employer_contribution_percent = messages.FloatField(16, required=True)
    tax_saving = messages.EnumField(TaxSavingType, 17, required=False)
    saving_value = messages.FloatField(18, required=True)
    wish_expression_link = messages.StringField(19, required=True)
    pension_key = messages.IntegerField(20, required=True)
    list_fund = messages.MessageField(ListFund, 21, repeated=True)
    fund_selection = messages.MessageField(FundSelection, 22, repeated=True)
    submitted = messages.StringField(23, required=True)
    

class PensionList(messages.Message):
    pension_list = messages.MessageField(Pension, 1, repeated=True)
    

class PensionSignup(messages.Message):
    user_id = messages.IntegerField(1, required=True)       
    contribution = messages.FloatField(2, required=False)
    employer_contribution = messages.FloatField(3, required=False)
    employee_contribution_percent = messages.FloatField(4, required=False)       
    employer_contribution_percent = messages.FloatField(5, required=True)
    tax_saving = messages.EnumField(TaxSavingType, 6)
    saving_value = messages.FloatField(7, required=True)
    list_fund = messages.StringField(8) 
    token = messages.StringField(9)
    list_fund = messages.MessageField(ListFund, 10, repeated=True)
    fund_selection = messages.MessageField(FundSelection, 11, repeated=True)
    pension_signup_key = messages.IntegerField(12, required=True)    
    status = messages.EnumField(StatusType, 13, required=True)
    manager = messages.MessageField(ManagerField, 14)
    employee = messages.MessageField(EmployeeField, 15)
    submitted = messages.StringField(16, required=True)
    total_contribution = messages.FloatField(17, required=False)
    
    
class PensionSignupList(messages.Message):
    pensions_signup_list = messages.MessageField(PensionSignup, 1, repeated=True)
    

class PensionSignupResponse(messages.Message):
    message = messages.StringField(1, required=True)
    

class ListFundModel(ndb.Model):
    name = ndb.StringProperty(required=True)
    value = ndb.FloatProperty(required=True)


class FundSelectionModel(ndb.Model):
    name = ndb.StringProperty(required=True)
    percent = ndb.FloatProperty(required=True)
                                 
    
class PensionModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)       
    start_date = ndb.DateProperty(required=False)
    end_date = ndb.DateProperty(required=False)     
    fund_value = ndb.FloatProperty(required=False)
    valuation_date = ndb.DateProperty(required=False)    
    employee_contribution = ndb.FloatProperty(required=False)
    employer_contribution = ndb.FloatProperty(required=True)
    employee_contribution_percent = ndb.FloatProperty(required=False)
    employer_contribution_percent = ndb.FloatProperty(required=False)
    min_employee_contribution_percent = ndb.FloatProperty(required=False)
    max_employee_contribution_percent = ndb.FloatProperty(required=False)
    min_employer_contribution_percent = ndb.FloatProperty(required=False)
    max_employer_contribution_percent = ndb.FloatProperty(required=False)
    tax_saving = msgprop.EnumProperty(TaxSavingType, indexed=False)
    saving_value = ndb.ComputedProperty(lambda self: self.get_tax_value())
    total_contribution = ndb.ComputedProperty(lambda self: self.get_total_contribution())
    wish_expression_link = ndb.StringProperty(required=True)
    list_fund = ndb.StructuredProperty(ListFundModel, repeated=True)
    fund_selection = ndb.StructuredProperty(FundSelectionModel, repeated=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)
    

    def get_tax_value(self):
        
        employee_contribution = self.employee_contribution

        if str(self.tax_saving) == 'SALARY_SACRIFICE':
            
            return employee_contribution * 0.138
        
        elif str(self.tax_saving) == 'NET_SAVING':
            
            return employee_contribution * 0.2
        
        else:
            
            return employee_contribution * 0.2
        
        

    def get_total_contribution(self):
        
        employee_contribution = self.employee_contribution
        employer_contribution = self.employer_contribution
        
        if str(self.tax_saving) == 'SALARY_SACRIFICE':
            
            return (employee_contribution * 0.138) + employee_contribution + employer_contribution
        
        elif str(self.tax_saving) == 'NET_SAVING':
            
            return employee_contribution + employer_contribution
        
        else:
            
            return employee_contribution + employer_contribution

            
    
    @classmethod
    def get_count(cls):
        return cls.query().count()
    
    @classmethod
    def get_submitted(cls):
        dateSubmitted = cls.query().order(-cls.submitted).get();
        if dateSubmitted:
            return dateSubmitted.submitted
        else:
            return False 
    
class PensionSignupModel(ndb.Model):
    pension = ndb.KeyProperty(kind=PensionModel, required=True)
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    contribution = ndb.FloatProperty(required=False, indexed=False)
    employer_contribution = ndb.FloatProperty(required=True, indexed=False)
    employee_contribution_percent = ndb.FloatProperty(required=False, indexed=False)
    employer_contribution_percent = ndb.FloatProperty(required=False, indexed=False)
    total_contribution = ndb.ComputedProperty(lambda self: self.get_total_contribution())
    tax_saving = msgprop.EnumProperty(TaxSavingType, indexed=False)
    saving_value = ndb.ComputedProperty(lambda self: self.get_tax_value())
    retirement_age = ndb.IntegerProperty(required=False, indexed=False)
    list_fund = ndb.StructuredProperty(ListFundModel, repeated=True, indexed=False)
    fund_selection = ndb.StructuredProperty(FundSelectionModel, repeated=True, indexed=False)
    token = ndb.StringProperty(required=True)
    status = msgprop.EnumProperty(StatusType, required=True)
    manager = ndb.KeyProperty(kind=UserModel, required=False, indexed=False)
    submitted = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    
    
    def get_tax_value(self):
        
        employee_contribution = self.contribution

        if str(self.tax_saving) == 'SALARY_SACRIFICE':
            
            return employee_contribution * 0.138
        
        elif str(self.tax_saving) == 'NET_SAVING':
            
            return employee_contribution * 0.2
        
        else:
            
            return employee_contribution * 0.2
        

    def get_total_contribution(self):
        
        employee_contribution = self.contribution
        employer_contribution = self.employer_contribution
        
        if str(self.tax_saving) == 'SALARY_SACRIFICE':
            
            return (employee_contribution * 0.138) + employee_contribution + employer_contribution
        
        elif str(self.tax_saving) == 'NET_SAVING':
            
            return employee_contribution + employer_contribution
        
        else:
            
            return employee_contribution + employer_contribution
    


    




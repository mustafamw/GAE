from google.appengine.ext import ndb

from protorpc import messages

from egb.user.user import UserModel

# from egb.core.generic.payment import Payment
# from egb.core.generic.deduction import Deduction
# from egb.core.generic.company import Department

class PayslipDates(messages.Message):
    date = messages.StringField(1, repeated=True)

   
class Payslip(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    employer_name = messages.StringField(2, required=False)
    employee_number = messages.IntegerField(3, required=False)
    department = messages.StringField(4, required=False)
    process_date = messages.StringField(5, required=False)
    tax_week = messages.IntegerField(6, required=False)    
    tax_code = messages.StringField(7, required=False)
    ni_number = messages.StringField(8, required=False)
    ni_code = messages.StringField(9, required=False)
    paye = messages.FloatField(10, required=False)
    payment = messages.StringField(11, required=False)
    deduction = messages.StringField(12, required=False)    
    ee_national_insurance = messages.FloatField(13, required=False)
    employee_pension = messages.FloatField(14, required=False)
    ssp = messages.FloatField(15, required=False)
    smp_spp = messages.FloatField(16, required=False)
    attachment_of_earnings = messages.FloatField(17, required=False)
    admin_fee = messages.FloatField(18, required=False)
    total_payment = messages.FloatField(19, required=False)
    total_deductions = messages.FloatField(20, required=False)
    gross_for_tax_td = messages.FloatField(21, required=False)    
    tax_paid_td = messages.FloatField(22, required=False)
    tax_credit_td = messages.FloatField(23, required=False)
    earnings_for_ni_td = messages.FloatField(24, required=False)
    ni_td = messages.FloatField(25, required=False)
    employer_pension = messages.FloatField(26, required=False)
    employer_pension_td = messages.FloatField(27, required=False)
    total_gross_tax_td = messages.FloatField(28, required=False)
    earning_for_ni = messages.FloatField(29, required=False)
    gross_for_tax = messages.FloatField(30, required=False)    
    net_pay = messages.FloatField(31, required=False)
    payment_method = messages.StringField(32, required=False)
    payment_period = messages.StringField(33, required=False)
    sac_pension = messages.FloatField(34, required=False)
    tax_credit = messages.FloatField(35, required=False)
    

class PayslipList(messages.Message):
    payslip_list = messages.MessageField(Payslip, 1, repeated=True)       

                                     
class PayslipModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    employer_name = ndb.StringProperty(required=True) 
    employee_number = ndb.IntegerProperty(required=True)
    department = ndb.StringProperty(required=False)
    process_date = ndb.DateProperty(required=True)
    year = ndb.IntegerProperty(required=True)
    tax_week = ndb.IntegerProperty(required=False)     
    tax_code = ndb.StringProperty(required=True)
    ni_number = ndb.StringProperty(required=True)
    ni_code = ndb.StringProperty(required=True)
    paye = ndb.FloatProperty(required=False, default=0.00)         
    payment = ndb.StringProperty(required=False)
    deduction = ndb.StringProperty(required=False)     
    ee_national_insurance = ndb.FloatProperty(required=False, default=0.00) 
    employee_pension = ndb.FloatProperty(required=False, default=0.00) 
    ssp = ndb.FloatProperty(required=False, default=0.00) 
    smp_spp = ndb.FloatProperty(required=False, default=0.00)
    attachment_of_earnings = ndb.FloatProperty(required=False, default=0.00) 
    admin_fee = ndb.FloatProperty(required=False, default=0.00) 
    total_payment = ndb.FloatProperty(required=False, default=0.00)
    total_deductions = ndb.FloatProperty(required=False, default=0.00) 
    gross_for_tax_td = ndb.FloatProperty(required=False, default=0.00)     
    tax_paid_td = ndb.FloatProperty(required=False, default=0.00) 
    tax_credit_td = ndb.FloatProperty(required=False, default=0.00)    
    earnings_for_ni_td = ndb.FloatProperty(required=False, default=0.00) 
    ni_td = ndb.FloatProperty(required=False, default=0.00) 
    employer_pension = ndb.FloatProperty(required=False, default=0.00) 
    employer_pension_td = ndb.FloatProperty(required=False, default=0.00)    
    total_gross_tax_td = ndb.FloatProperty(required=False, default=0.00) 
    earning_for_ni = ndb.FloatProperty(required=False, default=0.00)    
    gross_for_tax = ndb.FloatProperty(required=False, default=0.00) 
    net_pay = ndb.FloatProperty(required=False, default=0.00) 
    payment_method = ndb.StringProperty(required=False, default=0.00) 
    payment_period = ndb.StringProperty(required=False)
    sac_pension = ndb.FloatProperty(required=False, default=0.00)
    tax_credit = ndb.FloatProperty(required=False, default=0.00)
    submitted = ndb.DateTimeProperty(auto_now_add=True)

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


    
    
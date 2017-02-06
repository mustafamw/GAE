from protorpc import messages
from egb.payslip.payslips import Payslip, PayslipList, PayslipDates, PayslipModel
#from egb.roles.roles_helper import CheckRoles
from google.appengine.ext import ndb
from libs.parse.parse import Parse
from egb.utils.error import ErrorHelper
import endpoints

#ROLES_PERMISSION = ['administration','authenticated','leaver']
    
class PayslipHelper(Parse):
    
    PAYSLIP_LIST_DATES_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    PAYSLIP_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                    date=messages.StringField(2, variant=messages.Variant.STRING, required=True))
    
    def get_payslip_dates(self, client_id, user_id):
        
        qryPayslip = PayslipModel.query(PayslipModel.user == ndb.Key('UserModel', client_id)).order(-PayslipModel.process_date).fetch()
        
        if qryPayslip:
            
            return qryPayslip
        
        raise ErrorHelper.payslip_not_found()
    

    def construct_payslip_list_dates(self, payslips):
        
        payslipDateArr = []
        
        for payslips in payslips:
            
            process_date = self.parseDateFormatHyphen(payslips.process_date)

            payslipDateArr.append(process_date)
            
        return PayslipDates(date=payslipDateArr)
        
    
    def get_payslip(self, client_id, user_id, date):
        
        date = self.parseDate(date)
        
        payslips = PayslipModel.query(PayslipModel.user == ndb.Key('UserModel', client_id), 
                                      PayslipModel.user_id == user_id,
                                      PayslipModel.process_date == date).fetch()
                                      
        return payslips
    
    
    def construct_payslip(self, payslips):
        
        payslipsArr = []
        
        for payslip in payslips:
            
            process_date = self.parseDateFormatHyphen(payslip.process_date)
        
            payslip = Payslip(user_id=payslip.user_id,
                              employer_name=payslip.employer_name,
                              employee_number=payslip.employee_number,
                              department=payslip.department,
                              process_date=process_date,
                              tax_week=payslip.tax_week,
                              tax_code=payslip.tax_code,
                              ni_number=payslip.ni_number,
                              ni_code=payslip.ni_code,
                              paye=payslip.paye,
                              payment=payslip.payment,
                              deduction=payslip.deduction,
                              ee_national_insurance=payslip.ee_national_insurance,
                              employee_pension=payslip.employee_pension,
                              ssp=payslip.ssp,
                              smp_spp=payslip.smp_spp,
                              attachment_of_earnings=payslip.attachment_of_earnings,
                              admin_fee=payslip.admin_fee,
                              total_payment=payslip.total_payment,
                              total_deductions=payslip.total_deductions,
                              gross_for_tax_td=payslip.gross_for_tax_td,
                              tax_paid_td=payslip.tax_paid_td,
                              tax_credit_td=payslip.tax_credit_td,
                              earnings_for_ni_td=payslip.earnings_for_ni_td,
                              ni_td=payslip.ni_td,
                              employer_pension=payslip.employer_pension,
                              employer_pension_td=payslip.employer_pension_td,
                              total_gross_tax_td=payslip.total_gross_tax_td,
                              earning_for_ni=payslip.earning_for_ni,
                              gross_for_tax=payslip.gross_for_tax,
                              net_pay=payslip.net_pay,
                              payment_method=payslip.payment_method,
                              payment_period=payslip.payment_period,
                              sac_pension=payslip.sac_pension,
                              tax_credit=payslip.tax_credit)
            
            payslipsArr.append(payslip)
            
            
        return PayslipList(payslip_list = payslipsArr)
    
    
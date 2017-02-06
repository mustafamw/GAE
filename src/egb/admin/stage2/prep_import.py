#!/usr/bin/env python
import webapp2
import csv
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from prep_helper import PrepHelper
import logging
from egb.utils.helper import UtilsHelper
DEBUG = logging.getLogger().isEnabledFor(UtilsHelper.get_level())

csv_import = 'csv_import'

def validate_import(user_info):
    
    data_info = blobstore.BlobReader(user_info.key())
    reader = csv.reader(data_info, delimiter=',', dialect=csv.excel_tab)
    
    skip = True
    
    row_no = 1
    
    employee_id_list = []
     
    for row in reader:
         
        if skip is False:
            
            row_no += 1
            
            
            employee_id=row[0] 
            title=row[1] 
            first_name=row[2] 
            surname=row[3] 
            job_title=row[4] 
            date_of_birth=row[5] 
            ni_number=row[6] 
            email=row[7] 
            annual_holiday_allowance=row[8] 
            employee_date_joined=row[9] 
            date_of_leaving=row[10] 
            basic_salary=row[11] 
            bonus=row[12] 
            commission=row[13]     
            overtime=row[14]      
            fuel_allowance=row[15]     
            allowance_total=row[16]
            pension_date_joined=row[17]
            pension_provider=row[18]
            pension_scheme_type=row[19]
            pension_policy_no=row[20]
            employee_pension=row[21]
            employer_pension=row[22]
            sal_sac=row[23]
            fund_value=row[24]
            life_start=row[25]
            life_provider=row[26]
            life_scheme_type=row[27]
            life_salary_multiple=row[28]
            life_value=row[29]
            life_assured_amount=[30]
            pmi_start_date=row[31]
            pmi_provider_live=row[32]
            pmi_scheme_type=row[33]
            pmi_value=row[34]
            pmi_value_whole=row[35]
            ccv_value=row[36]
            ctw_value=row[37]
            company_car_value=row[38]
            car_allowance=row[39]
            
            if DEBUG:
                logging.info(row)
            
            PrepHelper.date_parse(employee_date_joined, row_no)
            PrepHelper.whitespace_replace(ni_number, row_no)
            PrepHelper.date_parse(date_of_birth, row_no)
            PrepHelper.email_parse(email, row_no)
            PrepHelper.start_date_parse(employee_date_joined, row_no)
            PrepHelper.end_date_parse(date_of_leaving, row_no)
            PrepHelper.payment_parse(basic_salary, row_no)
            PrepHelper.payment_parse(bonus, row_no)
            PrepHelper.payment_parse(commission, row_no)
            PrepHelper.payment_parse(overtime, row_no)
            PrepHelper.payment_parse(fuel_allowance, row_no)
            PrepHelper.payment_parse(allowance_total, row_no)
            
            #Pension
            PrepHelper.pension_date_joined_parse(pension_date_joined, row_no)
            PrepHelper.pension_provider_parse(pension_policy_no, row_no)
            PrepHelper.pension_scheme_type_parse(pension_policy_no, row_no)
            PrepHelper.pension_policy_number_parse(pension_policy_no, row_no)
            PrepHelper.pension_employee_pension_parse(employee_pension, row_no)
            PrepHelper.pension_employer_pension_parse(employer_pension, row_no)
            PrepHelper.pension_sal_sac_parse(employee_pension, employer_pension, row_no)
            PrepHelper.fund_value_parse(fund_value, row_no)
            
            #Life
            PrepHelper.life_start_date_parse(pmi_start_date,row_no)
            PrepHelper.life_provider_parse(life_salary_multiple,row_no)
            PrepHelper.life_scheme_type_parse(life_scheme_type, row_no)
            PrepHelper.life_salary_multiple_parse(life_salary_multiple, row_no)
            PrepHelper.life_value_parse(life_value, row_no)
            PrepHelper.life_assured_amount_parse(basic_salary, life_salary_multiple, row_no)
            
            #PMI
            PrepHelper.pmi_start_date_parse(pmi_start_date, row_no)
            PrepHelper.pmi_scheme_type_parse(pmi_scheme_type, row_no)
            PrepHelper.payment_parse(pmi_value, row_no)
            
            PrepHelper.payment_parse(pmi_value_whole, row_no)
            PrepHelper.payment_parse(ccv_value, row_no)
            PrepHelper.payment_parse(ctw_value, row_no)
            PrepHelper.payment_parse(company_car_value, row_no)
            PrepHelper.payment_parse(car_allowance, row_no)
            
            
        skip = False
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.redirect("/prep")  
            
    def post(self):

        validate_import_file = self.get_uploads(csv_import)
        
        if validate_import_file:
            print("in validate_import_file")
            
            file_info = validate_import_file[0]            
            validate_import(validate_import_file[0])            
            blobstore.delete(file_info.key()) 
        
        self.redirect("/prep")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        print "Print Stage 1"
        
        upload_url = blobstore.create_upload_url('/upload_prep')
        
        html_string = """
        <form action=""" + upload_url + """ method="POST" enctype="multipart/form-data">
        Select csv_import:
        <input type="file" name=""" + csv_import + """> <br>
        <input type="submit" name="submit" value="Submit">
        </form>    
        """ 
        
        self.response.write(html_string)
                
app = webapp2.WSGIApplication([
    ('/prep', MainHandler),
    ('/upload_prep', UploadHandler)
], debug=True)
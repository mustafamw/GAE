#!/usr/bin/env python
# new
import webapp2
import csv
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from validation_helper import validation_helper

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
            print '\n'
            print row 
            print '\n'
            
            #Employee Details
            validation_helper.employee_id_validation(employee_id, row_no, employee_id_list)
            employee_id_list.append(employee_id)
            validation_helper.title_validation(title, row_no)
            validation_helper.firstname_validation(first_name, row_no)
            validation_helper.surname_validation(surname, row_no)
            validation_helper.job_title_validation(job_title, row_no)
            validation_helper.dob_validation(date_of_birth, row_no)
            validation_helper.national_insurance_validation(ni_number, row_no)
            validation_helper.email_validation(email, row_no)
            
            #Employee Salary
            validation_helper.annual_holiday_allowance_validation(annual_holiday_allowance, row_no)
            validation_helper.employee_date_joined_validation(employee_date_joined, row_no)
            validation_helper.employee_date_of_leaving_validation(date_of_leaving, row_no)
            validation_helper.basic_salary_validation(basic_salary, row_no)
            validation_helper.bonus_validation(bonus, row_no)
            validation_helper.commision_validation(commission, row_no)
            validation_helper.overtime_validation(overtime, row_no)
            validation_helper.fuel_allowance_validation(fuel_allowance, row_no)
            validation_helper.allowance_total_validation(allowance_total, row_no)
            
            #Pension
            #Check
            validation_helper.pension_date_joined_validation(pension_date_joined, row_no)
            #Check
            validation_helper.pension_provider_validation(pension_provider, row_no)
            #Check
            validation_helper.pension_scheme_type_validation(pension_scheme_type, row_no)

            validation_helper.pension_policy_no_validation(pension_policy_no, row_no)
            validation_helper.employee_pension_validation(employee_pension, row_no)
            validation_helper.employer_pension_validation(employer_pension, row_no)
            
            #Life
            validation_helper.life_start_date_validation(life_start, row_no)
            validation_helper.life_salary_multiple_validation(life_salary_multiple, row_no)
            validation_helper.life_value_validation(life_value, row_no)
            
            #PMI
            validation_helper.pmi_start_date_validation(pmi_start_date, row_no)
            validation_helper.pmi_scheme_type_validation(pmi_scheme_type, row_no)
            validation_helper.pmi_value_validation(pmi_value, row_no)
            
            #Child Care Voucher
            validation_helper.ccv_value_validation(ccv_value, row_no)
            
            #Cycle To Work
            validation_helper.ctw_value_validation(ctw_value, row_no)
            
            #Company Car
            validation_helper.company_car_value_validation(company_car_value, row_no)
            
            #Car Allowance
            validation_helper.car_allowance_value_validation(car_allowance, row_no)
            
            
        skip = False
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.redirect("/validate")  
            
    def post(self):

        validate_import_file = self.get_uploads(csv_import)
        
        if validate_import_file:
            print("in validate_import_file")
            
            file_info = validate_import_file[0]            
            validate_import(validate_import_file[0])            
            blobstore.delete(file_info.key()) 
        
        self.redirect("/validate")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        print "Print Stage 1"
        
        upload_url = blobstore.create_upload_url('/upload_validate')
        
        html_string = """
        <form action=""" + upload_url + """ method="POST" enctype="multipart/form-data">
        Select csv_import:
        <input type="file" name=""" + csv_import + """> <br>
        <input type="submit" name="submit" value="Submit">
        </form>    
        """ 
        
        self.response.write(html_string)
                
app = webapp2.WSGIApplication([
    ('/validate', MainHandler),
    ('/upload_validate', UploadHandler)
], debug=True)
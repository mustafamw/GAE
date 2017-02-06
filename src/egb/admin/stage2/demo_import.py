#!/usr/bin/env python]#new
import webapp2
import csv
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from prep_helper import PrepHelper
import logging
from egb.utils.helper import UtilsHelper
DEBUG = logging.getLogger().isEnabledFor(UtilsHelper.get_level())

EMPLOYER_PREP = 'employer_prep'
EMPLOYEE_PREP = 'employee_prep'
PENSION_PREP = 'pension_prep'
PMI_PREP = 'pmi_prep'
LIFE_PREP = 'life_prep'
CCV_PREP = 'ccv_prep'

#Employer Import
def employer_import(user_info):
    
    data_info = blobstore.BlobReader(user_info.key())
    reader = csv.reader(data_info, delimiter=',', dialect=csv.excel_tab)
    
    skip = True
    
    row_no = 1
     
    for row in reader:
         
        if skip is False:
            
            row_no += 1
            
            name=row[0] 
            variation=row[1] 
            web_link=row[2] 
            handbook_link=row[3] 
            contact_link=row[4] 
            contact_email=row[5] 
            contact_phone=row[6] 
            email_ess=row[7] 
            email_holiday=row[8] 
            email_pension=row[9] 
            email_life=row[10] 
            email_cic=row[11] 
            email_gip=row[12] 
            email_cp=row[13]     
            email_dental=row[14]      
            email_ha=row[15]     
            email_hr=row[16]
            email_default=row[17]
            image_links=row[18]
            welcome_note=row[19]
            company_icon=row[20]
            company_slogan=row[21]
            bumf=row[22]
            window_life_start=row[23]
            window_life_end=row[24]
            window_cic_start=row[25]
            window_cic_end=row[26]
            window_pmi_start=row[27]
            window_pmi_end=row[28]
            window_ctw_start=row[29]
            window_ctw_end=row[30]
            window_wg_start=row[31]
            window_wg_end=row[32]
            
            if DEBUG:
                logging.info(row)
            
            PrepHelper.email_parse(contact_email, row_no)
            PrepHelper.whitespace_replace(contact_phone, row_no)
            PrepHelper.email_parse(email_ess, row_no)
            PrepHelper.email_parse(email_holiday, row_no)
            PrepHelper.email_parse(email_pension, row_no)
            PrepHelper.email_parse(email_life, row_no)
            PrepHelper.email_parse(email_cic, row_no)
            PrepHelper.email_parse(email_gip, row_no)
            PrepHelper.email_parse(email_cp, row_no)
            PrepHelper.email_parse(email_dental, row_no)
            PrepHelper.email_parse(email_ha, row_no)
            PrepHelper.email_parse(email_hr, row_no)
            PrepHelper.email_parse(email_default, row_no)
            PrepHelper.date_parse(window_life_start, row_no)
            PrepHelper.date_parse(window_life_end, row_no)
            PrepHelper.date_parse(window_cic_start, row_no)
            PrepHelper.date_parse(window_cic_end, row_no)
            PrepHelper.date_parse(window_pmi_start, row_no)
            PrepHelper.date_parse(window_pmi_end, row_no)
            PrepHelper.date_parse(window_ctw_start, row_no)
            PrepHelper.date_parse(window_ctw_end, row_no)
            PrepHelper.date_parse(window_wg_start, row_no)
            PrepHelper.date_parse(window_wg_end, row_no)

        skip = False


#Employee Import
def employee_import(user_info):
    
    data_info = blobstore.BlobReader(user_info.key())
    reader = csv.reader(data_info, delimiter=',', dialect=csv.excel_tab)
    
    skip = True
    
    row_no = 1
     
    for row in reader:
         
        if skip is False:
            
            row_no += 1
            
            user_ID=row[0]    
            employee_ID=row[1]      
            employer_variation=row[2]    
            job_title=row[3]    
            start_date=row[4]   
            end_date=row[5]    
            annual_salary=row[6]    
            hourly_rate=row[7]    
            currency=row[8]    
            bonus=row[9]    
            commission=row[10]    
            overtime=row[11]    
            weekly_hours=row[12]
            
            if DEBUG:
                logging.info(row)
                
            PrepHelper.start_date_parse(start_date, row_no)
            PrepHelper.end_date_parse(end_date, row_no)
            PrepHelper.payment_parse(annual_salary, row_no)
            PrepHelper.float_parse(hourly_rate, row_no)
            PrepHelper.payment_parse(bonus, row_no)
            PrepHelper.payment_parse(commission, row_no)
            PrepHelper.payment_parse(overtime, row_no)
            PrepHelper.float_parse(weekly_hours, row_no)
            
        skip = False
        
        
#Pension Import
def pension_import(user_info):

    data_info = blobstore.BlobReader(user_info.key())
    reader = csv.reader(data_info, delimiter=',', dialect=csv.excel_tab)
    
    skip = True
    
    row_no = 1
     
    for row in reader:
         
        if skip is False:
            
            row_no += 1
            
            employee_number=row[0]      
            ni_number=row[1]      
            provider_name=row[2]      
            policy_number=row[3]      
            start_date=row[4]      
            end_date=row[5]      
            employee_contribution=row[6]      
            employer_contribution=row[7]      
            employee_contribution_percent=row[8]      
            employer_contribution_percent=row[9]      
            salary_sacrifice=row[10]
            
            if DEBUG:
                logging.info(row)
                
            bool_salary_sacrifice = PrepHelper.convert_to_boolean(salary_sacrifice, row_no)
            PrepHelper.national_insurance_parse(ni_number, row_no)  
            PrepHelper.whitespace_replace(policy_number, row_no)
            PrepHelper.start_date_parse(start_date, row_no)
            PrepHelper.end_date_parse(end_date, row_no)
            PrepHelper.employee_contribution_payment_parse(employee_contribution, row_no)
            PrepHelper.employer_contribution_payment_parse(employer_contribution, row_no)
            PrepHelper.employee_contribution_parse(employee_contribution_percent, row_no)
            PrepHelper.employer_contribution_parse(employer_contribution_percent, row_no)
            PrepHelper.convert_to_boolean(salary_sacrifice, row_no)
    
            employee_contribution = PrepHelper.employee_contribution_payment_parse(employee_contribution, row_no)
            PrepHelper.employee_annual_contribution_parse(employee_contribution, 12)
            
            employer_contribution = PrepHelper.employer_contribution_payment_parse(employer_contribution, row_no)
            PrepHelper.employer_annual_contribution_parse(employer_contribution, 12)
     
        skip = False


#PMI Import
def pmi_import(user_info):

    data_info = blobstore.BlobReader(user_info.key())
    reader = csv.reader(data_info, delimiter=',', dialect=csv.excel_tab)
    
    skip = True
    
    row_no = 1
     
    for row in reader:
         
        if skip is False:
            
            row_no += 1
            
            employee_number=row[0]     
            ni_number=row[1]     
            provider_name=row[2]     
            flexible=row[3]     
            who=row[4]     
            cover_level=row[5]     
            where=row[6]     
            excess=row[7]     
            premium_core=row[8]
            
            if DEBUG:
                logging.info(row) 
            
            PrepHelper.national_insurance_parse(ni_number, row_no) 
            PrepHelper.convert_to_boolean(flexible, row_no)
            PrepHelper.payment_parse(excess, row_no)
            PrepHelper.payment_parse(premium_core, row_no)
            
        skip = False

#Life Import
def life_import(user_info):

    data_info = blobstore.BlobReader(user_info.key())
    reader = csv.reader(data_info, delimiter=',', dialect=csv.excel_tab)
    
    skip = True
    
    row_no = 1
     
    for row in reader:
         
        if skip is False:
            
            row_no += 1
            
            employee_number=row[0]     
            ni_number=row[1]     
            provider_name=row[2]     
            sum_assured=row[3]     
            core_multiple=row[4]     
            category_number=row[5]     
            flexible=row[6]     
            flex_multiple=row[7]     
            flex_max_multiple=row[8]     
            free_cover_limit=row[9]     
            has_flexed=row[10]     
            cap=row[11]     
            premium_core=row[12]     
            premium_flex=row[13]     
            gross=row[14]     
            net=row[15] 
            
            if DEBUG:
                logging.info(row)
            
            PrepHelper.national_insurance_parse(ni_number, row_no)
            PrepHelper.payment_parse(sum_assured, row_no)
            PrepHelper.float_parse(core_multiple, row_no) 
            PrepHelper.integer_parse(category_number, row_no)
            PrepHelper.convert_to_boolean(flexible, row_no)
            
        skip = False

#CCV Import
def ccv_import(user_info):

    data_info = blobstore.BlobReader(user_info.key())
    reader = csv.reader(data_info, delimiter=',', dialect=csv.excel_tab)
    
    skip = True
    
    row_no = 1
     
    for row in reader:
         
        if skip is False:
            
            row_no += 1
            
            employee_number=row[0]     
            ni_number=row[1]     
            employee_contribution=row[2]     
            protected_rights=row[3]     
            cut_off=row[4]
            
            if DEBUG:
                logging.info(row)
            
            PrepHelper.national_insurance_parse(ni_number, row_no)
            PrepHelper.payment_parse(employee_contribution, row_no)
            PrepHelper.convert_to_boolean(protected_rights, row_no)
            
        skip = False 
            
            
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.redirect("/demo-prep")  
            
    def post(self):

        employer_import_file = self.get_uploads(EMPLOYER_PREP)
        if employer_import_file:
            print("in employer_import_file")
            file_info = employer_import_file[0]            
            employer_import(employer_import_file[0])            
            blobstore.delete(file_info.key()) 

        employee_import_file = self.get_uploads(EMPLOYEE_PREP)
        if employee_import_file:
            print("in employee_import_file")
            file_info = employee_import_file[0]            
            employee_import(employee_import_file[0])            
            blobstore.delete(file_info.key())
        
        pension_import_file = self.get_uploads(PENSION_PREP)
        if pension_import_file:
            print("in pension_import_file")
            file_info = pension_import_file[0]            
            pension_import(pension_import_file[0])            
            blobstore.delete(file_info.key())
        
        pmi_import_file = self.get_uploads(PMI_PREP)
        if pmi_import_file:
            print("in pmi_import_file")
            file_info = pmi_import_file[0]            
            pmi_import(pmi_import_file[0])            
            blobstore.delete(file_info.key())
            
        life_import_file = self.get_uploads(LIFE_PREP)
        if life_import_file:
            print("in life_import_file")
            file_info = life_import_file[0]            
            life_import(life_import_file[0])            
            blobstore.delete(file_info.key())
        
        ccv_import_file = self.get_uploads(CCV_PREP)
        if ccv_import_file:
            print("in ccv_import_file")
            file_info = ccv_import_file[0]            
            ccv_import(ccv_import_file[0])            
            blobstore.delete(file_info.key())      
          
        
        self.redirect("/demo-prep")
        
class MainHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload_prep_demo')
        
        html_string = """
        <form action=""" + upload_url + """ method="POST" enctype="multipart/form-data">
        Select """+EMPLOYER_PREP+""":
        <input type="file" name=""" + EMPLOYER_PREP + """> <br>
        <input type="submit" name="submit" value="Submit">
        </form> 
        
        <form action=""" + upload_url + """ method="POST" enctype="multipart/form-data">
        Select """+EMPLOYEE_PREP+""":
        <input type="file" name=""" + EMPLOYEE_PREP + """> <br>
        <input type="submit" name="submit" value="Submit">
        </form>   
        
        <form action=""" + upload_url + """ method="POST" enctype="multipart/form-data">
        Select """+PENSION_PREP+""":
        <input type="file" name=""" + PENSION_PREP + """> <br>
        <input type="submit" name="submit" value="Submit">
        </form>    
        
        <form action=""" + upload_url + """ method="POST" enctype="multipart/form-data">
        Select """+PMI_PREP+""":
        <input type="file" name=""" + PMI_PREP + """> <br>
        <input type="submit" name="submit" value="Submit">
        </form>
        
        <form action=""" + upload_url + """ method="POST" enctype="multipart/form-data">
        Select """+LIFE_PREP+""":
        <input type="file" name=""" + LIFE_PREP + """> <br>
        <input type="submit" name="submit" value="Submit">
        </form>
        
        <form action=""" + upload_url + """ method="POST" enctype="multipart/form-data">
        Select """+CCV_PREP+""":
        <input type="file" name=""" + CCV_PREP + """> <br>
        <input type="submit" name="submit" value="Submit">
        </form>            
        """ 
        
        self.response.write(html_string)
                
app = webapp2.WSGIApplication([
    ('/demo-prep', MainHandler),
    ('/upload_prep_demo', UploadHandler)
], debug=True)
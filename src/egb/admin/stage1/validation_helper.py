#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import datetime
import numbers
import logging
import os
import time
from re import sub
from decimal import Decimal
from libs import dateutil

MIN_AGE = 18

from egb.utils.helper import UtilsHelper
DEBUG = logging.getLogger().isEnabledFor(UtilsHelper.get_level())

#http://einaregilsson.com/write-to-a-file-in-the-googleapp-engine-development-server/
if os.environ.get('SERVER_SOFTWARE','').startswith('Dev'):
    from google.appengine.tools.devappserver2.python.stubs import FakeFile
    FakeFile.ALLOWED_MODES = frozenset(['a','r', 'w', 'rb', 'U', 'rU'])

from libs.dateutil.parser import parse

#In the datastore aren't we storing '%d.%m.%Y' ?
DATE_FORMAT = '%d.%m.%Y'
CURRENCY_ENCODING = "latin-1"

EPOC_DATE = "01/01/1970"
RANDOM_DATE = "01.01.1111"

#TODO - Why are we using two different formats?
epoc_date2 = '01/01/1970'

#EMPTY STRING
EMPTY_STRING = '' 

#EMPTY FLOAT
EMPTY_FLOAT = 0.0

#Honorifics
HONORIFICS = ['mr', 'miss', 'ms', 'mrs', 'master', 'dr', 'madam', 'dame', 'lord', 'lady', 'prof', 'sir']

#Job Title 
JOB_TITLE = ['framework director', 'divisional director', 'group finance director',
'group commercial director', 'quantity surveyor', 'estimator', 'proposals co-ordiantor','working supervisor']

# Put any default values as variables
# So we can easily change them globally if needs be
# If these numbers are from the device, they will be strings
DEFAULT_ANDROID_ID = 0;
DEFAULT_IPHONE_ID = 0;

#Default Int anf Float
DEFAULT_NUMINT_VALUE = 0;
DEFAULT_NUMFLOAT_VALUE = 0.0;

#Email Regex
EMAIL_VALIDATION = r'[\w.-]+@[\w.-]+.\w+'

#NI_VALIDATION = r'^\s*[a-zA-Z]{2}(?:\s*\d\s*){6}[a-zA-Z]?\s*[a-zA-Z]{1}$'
NI_VALIDATION = r'^(?!BG)(?!GB)(?!NK)(?!KN)(?!TN)(?!NT)(?!ZZ)(?:[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z])(?:\s*\d\s*){6}([A-D]|\s)$'

# Email will always need to be unique
# We can't use a single string
CUSTOM_EMAIL = "?????????"

#Empty data field
EMPTY_FIELD = "Empty Field"

MAX_HOLIDAY = 40


JOINED_DATE_RANGE = -6

LOG_INFO = []
class validation_helper:
    
    @staticmethod
    def print_log(table):
        my_file = open("logs/%s-%s.txt" % (table,time.strftime("%d-%m-%Y")), "w")
        my_file.write("Table :%s \n" % (table))
        if LOG_INFO:
            for log in LOG_INFO:
                my_file.write("%s" % log)
        elif not LOG_INFO:
            my_file.write("Successfully Imported !!!")
        
        my_file.close()
        
    # Log Error
    @staticmethod
    def log_error(method, row_no):
        LOG_INFO.append("Row Number: %s --> %s \n" % (row_no, method))
        logging.info("Row Number: %s --> %s \n" % (row_no, method))
        
    
    # You could use this at the start of all methods
    # That need a basic string validation_helper
    @staticmethod
    def string_is_valid_example_only_use_the_next_one_down(value):
        
        if value:
            # Must have something in
            
            if isinstance(value, basestring):
                # Must be a string
            
                # Can use a string specific method now
                # to remove whitespace
                if value.strip():
                    # Must have something in
                    # A valid string
                    
                    return True
                    
                else:
                    # Must only have contained white space
                    
                    return False
                
            else:
                # is not a String!
                
                return False
                
        else:
            # is empty or null               
            
            return False
        
        
    @staticmethod
    def string_is_valid(value):
                
        if value and isinstance(value, basestring) and value.strip():       
            return True
            
        return False
    
    @staticmethod
    def number_is_valid(value):
        
        # think this cover int float and long
        if value and isinstance(value, (long, int, float)):
            return True
        
        return False
    
    # Date Validation  
    @staticmethod
    def date_validation(date):        
        # Date will always be String from CSV ?
        
        if validation_helper.string_is_valid(date):
            # There something in the String
            
            # Format could be d/m/yy
            # Format could be d/m/yyyy
            # Format could use separator - or / or . 
            
            # We need to get any string format into a date object
            # Look at this answer and library            
            # http://stackoverflow.com/a/25341965/1256219

            try: 
                parse(date)
                
                # Must be a date formatted string
                return True

            except ValueError:
                # not a date formatted string
                return False
        else:
            return False
    
    
    # Exclude Currency Value
    # http://stackoverflow.com/questions/8421922/how-do-i-convert-a-currency-string-to-a-floating-point-number-in-python
    @staticmethod
    def exlude_currency(value):
        if value and value != 'AE' :
            value = Decimal(sub(r'[^\d.]', '', value))
            return float(value)
        else:
            return False
    
    # Email Validation
    @staticmethod
    def email_validation(email, row_no):
        
        log_message_name = 'Email Validation: '
        
        if DEBUG:
            logging.info("email_validation" + str(row_no) + ' ~ '+ email)
             
        # If you try to do regex validation_helper on a null string 
        # in Java, it will crash.
        # I don't know about python?
        # Do other validation_helper first
        if validation_helper.string_is_valid(email):        
            match = re.search(EMAIL_VALIDATION, email.strip())
            
            if match:
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                # A log would need to written to the error file
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        
    
    # Employee ID Validation
    @staticmethod
    def employee_id_validation(value, row_no, employee_id_list):   
        
        log_message_name = 'Employee ID Validation: '
        
        if DEBUG:
            logging.info("employee_id_validation: " + str(row_no) + ' ~ '+ value) 
        if value:     
            if validation_helper.string_is_valid(value):
                if not value in employee_id_list:
                    validation_helper.log_error(''+log_message_name+'Success', row_no)
                else:
                    validation_helper.log_error(''+log_message_name+'Not Unique', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)

    
    # Title Validation
    @staticmethod
    def title_validation(value, row_no):
        
        log_message_name = 'Title Validation: '
        
        if DEBUG:
            logging.info("title_validation: " + str(row_no) + ' ~ '+ value)  
        if value:
            if validation_helper.string_is_valid(value):
                if value.lower() in HONORIFICS:
                    validation_helper.log_error(''+log_message_name+'Success', row_no)
                else:
                    validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
                
    
    # First Name Validation
    # TODO - check for foriegn characters
    @staticmethod
    def firstname_validation(value, row_no):
        
        log_message_name = 'First Name Validation: '
        
        if DEBUG:
            logging.info("firstname_validation: " + str(row_no) + ' ~ '+ value)
                  
        if value:
            if validation_helper.string_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    
    # Surname Validation
    @staticmethod
    def surname_validation(value, row_no): 
        
        log_message_name = 'Surname Validation: '
        
        if DEBUG:
            logging.info("surname_validation: " + str(row_no) + ' ~ '+ value)
          
        if value:     
            if validation_helper.string_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    
    # Job Title Validation
    @staticmethod
    def job_title_validation(value, row_no): 
        
        log_message_name = 'Job Title Validation: '
        
        if DEBUG:
            logging.info("job_title_validation: " + str(row_no) + ' ~ '+ value)
               
        if validation_helper.string_is_valid(value):
            if value.lower() in JOB_TITLE:
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    # Date of Birth Validation
    @staticmethod
    def dob_validation(dob, row_no):
        
        log_message_name = 'Date of birth Validation: '   
        
        if DEBUG:
            logging.info("dob_validation: " + str(row_no) + ' ~ '+ dob)    
        
        if dob:
            if validation_helper.date_validation(dob):
                
                now = datetime.datetime.now().now()

                #http://stackoverflow.com/questions/27800775/python-dateutil-parser-parse-parses-month-first-not-day
                date_parse = parse(dob, dayfirst=True)
  
            
                age = dateutil.relativedelta.relativedelta(now, date_parse).years
            
                if age >= MIN_AGE:
                    validation_helper.log_error(''+log_message_name+'Success', row_no)
                else:
                    validation_helper.log_error(''+log_message_name+'Too young!!', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
        
    # National Insurance Validation
    @staticmethod
    def national_insurance_validation(national_insurance, row_no):
        
        log_message_name = 'National Insurance Validation: '  
        
        if DEBUG:
            logging.info("national_insurance_validation: " + str(row_no) + ' ~ '+ national_insurance)   
        
        if national_insurance:
            if validation_helper.string_is_valid(national_insurance):
                
                
                match = re.search(NI_VALIDATION, national_insurance.replace(" ", ""), re.IGNORECASE)
                
                if match:
                    validation_helper.log_error(''+log_message_name+'Success', row_no)
                else:
                    # A log would need to written to the error file
                    validation_helper.log_error(''+log_message_name+'Not Valid Format', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
            
        
    # Annual Leave Validation
    @staticmethod
    def annual_holiday_allowance_validation(value, row_no):
        
        log_message_name = 'Annual Holiday Allowance Validation: '  
        
        if DEBUG:
            logging.info("annual_holiday_allowance_validation: " + str(row_no) + ' ~ '+ str(value))  
            
        if value:
            if validation_helper.number_is_valid(float(value)):
                if float(value) <= MAX_HOLIDAY:   
                    validation_helper.log_error(''+log_message_name+'Success', row_no)
                else:
                    validation_helper.log_error(''+log_message_name+'Too much holiday allowance', row_no) 
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
        
    # Employee Date Joined Validation
    @staticmethod
    def employee_date_joined_validation(date, row_no):
        
        log_message_name = 'Employee Date Joined Validation: ' 
        
        if DEBUG:
            logging.info("employee_date_joined_validation: " + str(row_no) + ' ~ '+ date)  
        
        if date:     
            if validation_helper.date_validation(date):
                    
                now = datetime.datetime.now().now()

                #http://stackoverflow.com/questions/27800775/python-dateutil-parser-parse-parses-month-first-not-day
                date_parse = parse(date, dayfirst=True)
  
                month = dateutil.relativedelta.relativedelta(now, date_parse).months
                
                year = dateutil.relativedelta.relativedelta(now, date_parse).years
                
                if year >=0 and month > JOINED_DATE_RANGE:
                    
                    validation_helper.log_error(''+log_message_name+'Success', row_no)
                    
                else:
                    
                    validation_helper.log_error(''+log_message_name+'Error future date', row_no)
                    
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    # Employee Date of Leaving Validation
    @staticmethod
    def employee_date_of_leaving_validation(date, row_no):
        
        log_message_name = 'Employee Date of leaving Validation: ' 
        
        if DEBUG:
            logging.info("employee_date_of_leaving_validation: " + str(row_no) + ' ~ '+ date)  
        
        if date:
            if validation_helper.date_validation(date):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    
    # Company Validation
    @staticmethod
    def company_validation(value, row_no):
        
        log_message_name = 'Company Validation: ' 
        
        if DEBUG:
            logging.info("company_validation: " + str(row_no) + ' ~ '+ value) 
             
        if value:  
            if validation_helper.string_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
            
        
    
    # Basic Salary Validation
    @staticmethod
    def basic_salary_validation(value, row_no):
        
        log_message_name = 'Basic Salary Validation: ' 
        
        if DEBUG:
            logging.info("basic_salary_validation: " + str(row_no) + ' ~ '+ str(value))  
        
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:  
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
        
    # Bonus Validation
    @staticmethod
    def bonus_validation(value, row_no):
        
        log_message_name = 'Bonus Validation: ' 
        
        if DEBUG:
            logging.info("bonus_validation: " + str(row_no) + ' ~ '+ value)  
        
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
        
    # Commission Validation
    @staticmethod
    def commision_validation(value, row_no):
        
        log_message_name = 'Commission Validation: '
        
        if DEBUG:
            logging.info("commission_validation: " + str(row_no) + ' ~ '+ value)  
            
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
        
    # Overtime Validation
    @staticmethod
    def overtime_validation(value, row_no):

        log_message_name = 'Overtime Validation: '
        
        if DEBUG:
            logging.info("overtime_validation: " + str(row_no) + ' ~ '+ value)  
            
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
        
        
    # Fuel Allowance Validation
    @staticmethod
    def fuel_allowance_validation(value, row_no):
        
        log_message_name = 'Fuel Allowance Validation: '
        
        if DEBUG:
            logging.info("fuel_allowance_validation: " + str(row_no) + ' ~ '+ value)  
            
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:  
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
                
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
        
    
    # Allowance Total Validation
    @staticmethod
    def allowance_total_validation(value, row_no):
        
        log_message_name = 'Allowance Total Validation: '

        if DEBUG:
            logging.info("allowance_total_validation: " + str(row_no) + ' ~ '+ value)  
            
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:   
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
                
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    # Pension Date Joined Validation
    @staticmethod
    def pension_date_joined_validation(value, row_no):
        
        log_message_name = 'Pension Date Joined Validation: '
        
        if DEBUG:
            logging.info("pension_date_joined_validation: " + str(row_no) + ' ~ '+ value)  
        if value:
            if validation_helper.date_validation(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
        
    # Pension Provider Joined Validation
    @staticmethod
    def pension_provider_validation(value, row_no):
        
        log_message_name = 'Pension Provider Validation: '
        
        if DEBUG:
            logging.info("pension_provider_validation: " + str(row_no) + ' ~ '+ value)  
        
        if value:   
            if validation_helper.string_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
            
    
    # Pension Scheme Type Validation
    @staticmethod
    def pension_scheme_type_validation(value, row_no):
        
        log_message_name = 'Pension Scheme Type Validation: '
        
        if DEBUG:
            logging.info("pension_scheme_type_validation: " + str(row_no) + ' ~ '+ value)  
        if value:       
            if validation_helper.string_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
        
    # Pension Policy Number Validation
    @staticmethod
    def pension_policy_no_validation(value, row_no):
        
        log_message_name = 'Pension Policy Number Validation: '
        
        if DEBUG:
            logging.info("pension_policy_no_validation: " + str(row_no) + ' ~ '+ value)  
            
        if value:        
            if validation_helper.string_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
            
    # Employee Pension Validation
    @staticmethod
    def employee_pension_validation(value, row_no):
        
        log_message_name = 'Employee Pension Validation: '
        
        if DEBUG:
            logging.info("employee_pension_validation: " + str(row_no) + ' ~ '+ str(value))  
            
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    # Employer Pension Validation
    @staticmethod
    def employer_pension_validation(value, row_no):
        
        log_message_name = 'Employer Pension Validation: '
            
        if DEBUG:
            logging.info("employer_pension_validation: " + str(row_no) + ' ~ '+ value)  
        
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:      
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    # Life Start Date Validation
    @staticmethod
    def life_start_date_validation(value, row_no):
        
        log_message_name = 'Life Start Date Validation: '
        
        if DEBUG:
            logging.info("life_start_date_validation: " + str(row_no) + ' ~ '+ value) 
             
        if value:        
            if validation_helper.date_validation(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
            
            
    # Life Start Date Validation
    @staticmethod
    def life_salary_multiple_validation(value, row_no):
        
        log_message_name = 'Life Salary Multiple Validation: '
        
        if DEBUG:
            logging.info("life_salary_multiple_validation: " + str(row_no) + ' ~ '+ value)  
        
        if value:        
            if value:
                if validation_helper.number_is_valid(int(value)):
                    validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    # Life Value Validation
    @staticmethod
    def life_value_validation(value, row_no):
        
        log_message_name = 'Life Value Validation: '
        
        if DEBUG:
            logging.info("life_value_validation: " + str(row_no) + ' ~ '+ value)  
            
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
            
            
    # PMI Start Date Validation
    @staticmethod
    def pmi_start_date_validation(value, row_no):
        
        log_message_name = 'PMI Start Date Validation: '
        
        if DEBUG:
            logging.info("pmi_start_date_validation: " + str(row_no) + ' ~ '+ value)  
        if value:        
            if validation_helper.date_validation(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    
    # PMI Start Date Validation
    @staticmethod
    def pmi_scheme_type_validation(value, row_no):
        
        log_message_name = 'PMI Scheme Type Validation: '
        
        if DEBUG:
            logging.info("pmi_scheme_type_validation: " + str(row_no) + ' ~ '+ value)  
        
        if value:        
            if validation_helper.string_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
            
    # PMI Value Validation
    @staticmethod
    def pmi_value_validation(value, row_no):
        
        log_message_name = 'PMI Value Validation: '
        
        if DEBUG:
            logging.info("pmi_value_validation: " + str(row_no) + ' ~ '+ value)  
        
        # Exclude currency
        value = validation_helper.exlude_currency(value)
    
        if value:       
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
            
    
    # CCV Value Validation
    @staticmethod
    def ccv_value_validation(value, row_no):

        log_message_name = 'Child Care Voucher Value Validation: '
        
        if DEBUG:
            logging.info("ccv_value_validation: " + str(row_no) + ' ~ '+ value)  
        
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)


    # C2W Value Validation
    @staticmethod
    def ctw_value_validation(value, row_no):
        
        log_message_name = 'Cycle To Work Value Validation: '

        if DEBUG:
            logging.info("ctw_value_validation: " + str(row_no) + ' ~ '+ value)  
        
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:  
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    
    # Company Car Value Validation
    @staticmethod
    def company_car_value_validation(value, row_no):
        
        log_message_name = 'Company Car Value Validation: '

        if DEBUG:
            logging.info("company_car_value_validation: " + str(row_no) + ' ~ '+ value)  
        
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:        
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    
    # Car Allowance Value Validation
    @staticmethod
    def car_allowance_value_validation(value, row_no):
        
        log_message_name = 'Car Allowance Value Validation: '
        
        if DEBUG:
            logging.info("car_allowance_value_validation: " + str(row_no) + ' ~ '+ value)  
        
        # Exclude currency
        value = validation_helper.exlude_currency(value)
        
        if value:
            if validation_helper.number_is_valid(value):
                validation_helper.log_error(''+log_message_name+'Success', row_no)
            else:
                validation_helper.log_error(''+log_message_name+'Not Valid', row_no)
        else:
            validation_helper.log_error(''+log_message_name+EMPTY_FIELD+'', row_no)
    
    
    
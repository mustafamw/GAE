#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# new update
import logging
from egb.utils.helper import UtilsHelper
from libs.dateutil.parser import parse
import datetime
from libs.dateutil.tz import relativedelta
from libs import dateutil
from re import sub
from decimal import Decimal

DS_DATE_FORMAT = '%d.%m.%Y'

DEBUG = logging.getLogger().isEnabledFor(UtilsHelper.get_level())

MIN_AGE = 18

EPOC_DATE = '01.01.1970'

AUTO_ENROLlMENT = 'AE'

EMPTY_FLOAT = 0.0

EMPTY_INT = 0

EMPTY_FIELD = ""

LIFE_PROVIDER = "Zurich"

BANDCE = "bandce"

class PrepHelper():
        
    # Exclude Currency Value
    # http://stackoverflow.com/questions/8421922/how-do-i-convert-a-currency-string-to-a-floating-point-number-in-python
    @staticmethod
    def exlude_currency(value):
        value = Decimal(sub(r'[^\d.]', '', value))
        return float(value)
        
    @staticmethod
    def convert_to_float(value):
        return float(value)
    
    
    @staticmethod
    def convert_to_int(value):
        return int(value)
    
    
    @staticmethod
    def convert_to_long(value):
        return long(value)
    
    @staticmethod
    def convert_date(date):
        
        #http://stackoverflow.com/questions/27800775/python-dateutil-parser-parse-parses-month-first-not-day
        date_parse = parse(date, dayfirst=True)
        
        google_date = date_parse.date()
        
#         my_date = google_date.strftime(DS_DATE_FORMAT)
#         
#         print 'asfsdfasd ->>' + str(my_date)
#         
#         ds_date = datetime.datetime.strptime(my_date, 
#                                                  DS_DATE_FORMAT).date()
#         
#         print 'asfsdfasd ->>' + str(ds_date)
                                                 
        

        return google_date
    
    @staticmethod
    def convert_to_boolean(value, row_no):
        if DEBUG:
            logging.info("Boolean parse: " + str(value))
        if value:
            if value.lower() == "yes" or value.lower() == "true":
                return True
            else:
                return False
        else:
            return False
    
    @staticmethod
    def holiday_allowance_parse(value, row_no):
        if DEBUG:
            logging.info("Holiday Allowance parse: " + str(value))
        
        if value:
            value = PrepHelper.convert_to_float(value)
            if DEBUG:
                logging.info("Holiday Allowance float: " + str(value))
            return value
        else:
            if DEBUG:
                logging.info("Holiday Allowance Empty float: " + str(EMPTY_FLOAT))
            return EMPTY_FLOAT
            
        
    #Parse Date
    @staticmethod
    def date_parse(date, row_no):
        
        if DEBUG:
            logging.info("Date parse: "+ str(date))
    
        if date:
            #http://stackoverflow.com/questions/27800775/python-dateutil-parser-parse-parses-month-first-not-day
            date = PrepHelper.convert_date(date)
            
            if DEBUG:
                logging.info("Original Date Parsed Row:" + str(row_no) + ' ~ '+ str(date))
                logging.info("Date Parsed Row:" + str(row_no) + ' ~ '+ str(date))
            return date
        else:
            date = PrepHelper.convert_date(EPOC_DATE)
            if DEBUG:
                logging.info("Empty Date Parsed Row:" + str(row_no) + ' ~ '+ str(date))
            return date
            
            
    #String to Lower Case  
    @staticmethod
    def str_to_lowercase(data):
        pass

    #String to Upper Case  
    @staticmethod
    def str_to_uppercase():
        pass
    
    
    @staticmethod
    def whitespace_replace(value, row_no):
        if DEBUG:
            logging.info("whitepspcae parse: " + str(value))
        # Replace all runs of whitespace with a non
        value_parse = value.replace(" ", "")
        return value_parse.upper()
    
    
    @staticmethod
    def email_parse(value, row_no):
        
        if DEBUG:
            logging.info("Email parse: " + str(value))
            
        if value:
            email = value.lower().strip()
            if DEBUG:
                logging.info("Email updated: " + str(email))
            return email
        else:
            if DEBUG:
                logging.info("Email Empty updated: " + str(EMPTY_FIELD))
            return EMPTY_FIELD
            
            
            
    @staticmethod
    def start_date_parse(date, row_no):
        if DEBUG:
            logging.info("Start Date parse: " + str(date))
        
        if date:
            start_date = PrepHelper.convert_date(date)
            if DEBUG:
                logging.info("Start Date updated: " + str(start_date))
            return start_date
        else:
            start_date = PrepHelper.convert_date(EPOC_DATE)
            if DEBUG:
                logging.info("Start Date Empty updated: " + str(start_date))
            return start_date
            
            
    @staticmethod
    def end_date_parse(date, row_no):
        if DEBUG:
            logging.info("End Date parse: " + str(date))
        
        if date:   
            end_date = PrepHelper.convert_date(date)
            if DEBUG:
                logging.info("End Date Updated: " + str(end_date))
            return end_date
        else:
            end_date = PrepHelper.convert_date(EPOC_DATE)
            if DEBUG:
                logging.info("End Date Empty updated: " + str(end_date))
            return end_date
        
            
    @staticmethod
    def payment_parse(value, row_no):
        if DEBUG:
            logging.info("payment parse: " + str(value))
        
        if value:
            value = PrepHelper.exlude_currency(value)
            if DEBUG:
                logging.info("Payment Parse updated: " + str(value))
            return value
        else:
            if DEBUG:
                logging.info("Payment Parse Empty updated: " + str(EMPTY_FLOAT))
            return EMPTY_FLOAT
        
        
    #TODO - looking into?
    @staticmethod
    def pension_date_joined_parse(date, row_no):
        if DEBUG:
            logging.info("Pension Date Joined parse: " + str(date))
        
        if date and date != "0":   
            date_joined = PrepHelper.convert_date(date)
            if DEBUG:
                logging.info("Pension Date  Joined parse update: " + str(date_joined))
            return date_joined
        else:
            date_joined = PrepHelper.convert_date(EPOC_DATE)
            if DEBUG:
                logging.info("Pension Date Empty updated: " + str(date_joined))
            return date_joined
        

    #TODO - looking into?
    @staticmethod
    def pension_provider_parse(value, row_no):
        if DEBUG:
            logging.info("Pension Provider parse: " + str(value))
        
        if value:
            if value == AUTO_ENROLlMENT:
                if DEBUG:
                    logging.info("Pension Provider parse update: " + str(value))
                return BANDCE
            else:
                if DEBUG:
                    logging.info("Pension Provider parse update: " + str(value))
                return 'SL'
        else:
            if DEBUG:
                    logging.info("Pension Provider TODO: " + str(value))
                    
    
    #TODO - looking into?
    @staticmethod
    def pension_scheme_type_parse(value, row_no):
        if DEBUG:
            logging.info("Pension Scheme Type parse: " + str(value))
        
        if value:
            if value == AUTO_ENROLlMENT:
                if DEBUG:
                    logging.info("Pension Scheme Type parse update: " + str(value))
                return AUTO_ENROLlMENT
            else:
                if DEBUG:
                    logging.info("Pension Scheme Type parse update: " + str("Core"))
                return 'Core'
        else:
            if DEBUG:
                    logging.info("Pension Scheme Type TODO: " + str(value))
        
        
    #TODO - looking into?
    @staticmethod
    def pension_policy_number_parse(value, row_no):
        if DEBUG:
            logging.info("Pension Policy Number parse: " + str(value))
        
        if value:
            value_parse = value.replace(" ", "").strip()
            if DEBUG:
                logging.info("Pension Policy Number parse update: " + str(value_parse))
            return value_parse
        else:
            if DEBUG:
                    logging.info("Pension Policy Number parse TODO: " + str(value))
                    
                    
    #TODO - looking into?
    @staticmethod
    def pension_employee_pension_parse(value, row_no):
        if DEBUG:
            logging.info("Pension Employee Contribution parse: " + str(value))
        
        if value:
            if value == AUTO_ENROLlMENT:
                if DEBUG:
                    logging.info("Pension Employee Contribution parse update: " + str(value))
                return value
            else:
                value = PrepHelper.payment_parse(value, row_no)
                if DEBUG:
                    logging.info("Pension Employee Contribution update: " + str(value))
        else:
            if DEBUG:
                    logging.info("Pension Employee Contribution TODO: " + str(value))
    
    
    
    #TODO - looking into?
    @staticmethod
    def pension_employer_pension_parse(value, row_no):
        if DEBUG:
            logging.info("Pension Employer Contribution parse: " + str(value))
        
        if value:
            if value == AUTO_ENROLlMENT:
                if DEBUG:
                    logging.info("Pension Employer Contribution parse update: " + str(value))
                return value
            else:
                value = PrepHelper.payment_parse(value, row_no)
                if DEBUG:
                    logging.info("Pension Employer Contribution update: " + str(value))
        else:
            if DEBUG:
                    logging.info("Pension Employer Contribution TODO: " + str(value))
    
    
    #TODO - looking into?
    @staticmethod
    def pension_sal_sac_parse(employee_pension, employer_pension, row_no):

        if DEBUG:
            logging.info("Salary Sacrifice parse: Employee: %s, Employer: %s " % (employee_pension, employer_pension))
        
        if employee_pension != AUTO_ENROLlMENT and employer_pension !=AUTO_ENROLlMENT:
            
            employee_pension = PrepHelper.payment_parse(employee_pension, row_no)
            employer_pension = PrepHelper.payment_parse(employer_pension, row_no)
            
            sal_sac = employee_pension + employer_pension
            
            if DEBUG:
                logging.info("Salary Sacrifice updated: " + str(sal_sac))
            return sal_sac
        else:
            if DEBUG:
                logging.info("Salary Sacrifice Empty updated: " + EMPTY_FIELD)
            
            return EMPTY_FIELD
    
    
    #TODO - looking into?
    @staticmethod
    def fund_value_parse(value, row_no):
        if DEBUG:
            logging.info("Pension Funding parse: " + str(value))
        
        if value:
            if value == AUTO_ENROLlMENT:
                if DEBUG:
                    logging.info("Pension Funding parse update: " + str(value))
                return value
            else:
                value = PrepHelper.payment_parse(value, row_no)
                if DEBUG:
                    logging.info("Pension Funding update: " + str(value))
        else:
            if DEBUG:
                    logging.info("Pension Employer Contribution TODO: " + str(value))
    
    
    #TODO - looking into?
    @staticmethod
    def life_start_date_parse(date, row_no):
        if DEBUG:
            logging.info("Life Start Date parse: " + str(date))
        
        if date and date != "n/a":   
            start_date = PrepHelper.convert_date(date)
            if DEBUG:
                logging.info("Life Start Date parse update: " + str(start_date))
            return start_date
        else:
            start_date = PrepHelper.convert_date(EPOC_DATE)
            if DEBUG:
                logging.info("Life Start Date Empty updated: " + str(start_date))
            return start_date
    
    
    #TODO - looking into?
    @staticmethod
    def life_provider_parse(value, row_no):
        if DEBUG:
            logging.info("Life Provider parse: " + str(value))
        
        if value:
            value = PrepHelper.convert_to_float(value)
            if value > 0:
                if DEBUG:
                    logging.info("Life Provider parse update: " + str(LIFE_PROVIDER))
                return LIFE_PROVIDER
            else:
                if DEBUG:
                    logging.info("Life Provider parse update: " + str(value))
                return BANDCE
        else:
            if DEBUG:
                    logging.info("Life Provider TODO: " + str(value))
                    
    #TODO - looking into?
    @staticmethod
    def life_scheme_type_parse(value, row_no):
        pass
#         if DEBUG:
#             logging.info("Life Scheme Type parse: " + str(value))
#         
#         if value:
#             if value == AUTO_ENROLlMENT:
#                 if DEBUG:
#                     logging.info("Life Scheme Type parse update: " + str(value))
#                 return AUTO_ENROLlMENT
#             else:
#                 if DEBUG:
#                     logging.info("Life Scheme Type parse update: " + str(value))
#                 return 'Core'
#         else:
#             if DEBUG:
#                     logging.info("Life Scheme Type TODO: " + str(value))


    #TODO - looking into?
    @staticmethod
    def life_salary_multiple_parse(value, row_no):
        if DEBUG:
            logging.info("Life Salary Multiple parse: " + str(value))
        
        if value:
            value = PrepHelper.convert_to_float(value)
            if DEBUG:
                logging.info("Life Salary Multiple parse update: " + str(value))
        else:
            if DEBUG:
                logging.info("Life Salary Multiple parse Empty updated: " + str(EMPTY_FIELD))
            return EMPTY_FIELD
        
    
    #TODO - looking into?
    @staticmethod
    def life_value_parse(value, row_no):
        if DEBUG:
            logging.info("Life value parse: " + str(value))
        
        if value:
            value = PrepHelper.payment_parse(value, row_no)
            if DEBUG:
                logging.info("Life value parse update: " + str(value))
            return value
        
        else:
            if DEBUG:
                logging.info("Life value parse Empty updated: " + str(EMPTY_FIELD))
    
    
    #TODO - looking into?
    @staticmethod
    def life_assured_amount_parse(basic_salary, life_salary_multiple, row_no):
        if DEBUG:
            logging.info("Life Assured Amount parse: Basic Salary: %s, Salary Multiple: %s " % (basic_salary, life_salary_multiple))
        
        if basic_salary and life_salary_multiple:
            
            basic_salary = PrepHelper.payment_parse(basic_salary, row_no)
            life_salary_multiple = PrepHelper.payment_parse(life_salary_multiple, row_no)
            
            life_assured_amount = basic_salary * life_salary_multiple
            
            if DEBUG:
                logging.info("Life Assured update: " + str(life_assured_amount))
            return life_assured_amount
        else:
            if DEBUG:
                logging.info("Life Assured Empty updated: " + str(EMPTY_FLOAT))
            return EMPTY_FLOAT
        
    
    #TODO - looking into?
    @staticmethod
    def pmi_start_date_parse(date, row_no):
        if DEBUG:
            logging.info("PMI Start Date parse: " + str(date))
        
        if date and date != "n/a":   
            start_date = PrepHelper.convert_date(date)
            if DEBUG:
                logging.info("PMI Start Date parse update: " + str(start_date))
            return start_date
        else:
            start_date = PrepHelper.convert_date(EPOC_DATE)
            if DEBUG:
                logging.info("PMI Start Date  Empty updated: " + str(start_date))
            return start_date
    
    #TODO - looking into?
    @staticmethod
    def pmi_scheme_type_parse(value, row_no):
        if DEBUG:
            logging.info("PMI Type parse: " + str(value))
        
        if value:
            value = value.lower()
            if DEBUG:
                logging.info("PMI Type parse update: " + str(value))
            return value
        else:
            if DEBUG:
                logging.info("PMI Type parse update: " + str(EMPTY_FIELD))
                
                
    @staticmethod
    def float_parse(value, row_no):
        if DEBUG:
            logging.info("Float parse: " + str(value))
        
        if value:
            value = PrepHelper.convert_to_float(value)
            if DEBUG:
                logging.info("Float parse update: " + str(value))
        else:
            if DEBUG:
                logging.info("Float parse update: " + str(value))
            return EMPTY_FLOAT
    
    
    @staticmethod
    def integer_parse(value, row_no):
        if DEBUG:
            logging.info("Integer parse: " + str(value))
        
        if value:
            value = PrepHelper.convert_to_int(value)
            if DEBUG:
                logging.info("Integer parse update: " + str(value))
        else:
            if DEBUG:
                logging.info("Integer parse update: " + str(value))
            return EMPTY_INT
    
    
    @staticmethod
    def national_insurance_parse(value, row_no):
        if DEBUG:
            logging.info("National insurance parse: " + str(value))
        
        if value:
            value = PrepHelper.whitespace_replace(value, row_no)
            if DEBUG:
                logging.info("National insurance update: " + str(value.upper()))
            return value
        else:
            if DEBUG:
                logging.info("National insurance Empty updated: " + str(EMPTY_FIELD))
            return EMPTY_FIELD
                
                
    @staticmethod
    def employee_contribution_payment_parse(value, row_no):
        if DEBUG:
            logging.info("Employee Contribution Payment parse: " + str(value))
        
        if value:
            value = PrepHelper.exlude_currency(value)
            if DEBUG:
                logging.info("Employee Contribution Payment update: " + str(value))
            return value
        else:
            if DEBUG:
                logging.info("Employee Contribution Payment Empty updated: " + str(EMPTY_FLOAT))
            return EMPTY_FLOAT
        
    
    @staticmethod
    def employer_contribution_payment_parse(value, row_no):
        if DEBUG:
            logging.info("Employer Contribution Payment parse: " + str(value))
        if value:
            value = PrepHelper.exlude_currency(value)
            if DEBUG:
                logging.info("Employer Contribution Payment Parse update: " + str(value))
            return value
        else:
            if DEBUG:
                logging.info("Employer Contribution Payment Empty updated: " + str(EMPTY_FLOAT))
            return EMPTY_FLOAT
        
        
    @staticmethod
    def employee_contribution_parse(value, row_no):
        if DEBUG:
            logging.info("Employee Contribution parse: " + str(value))
        if value:
            value = PrepHelper.convert_to_float(value)
            if DEBUG:
                logging.info("Employee Contribution parse:" + str(value))
            return value
        else:
            if DEBUG:
                logging.info("Employee Contribution Empty updated:" + str(EMPTY_FLOAT))
            return EMPTY_FLOAT
                             
    
    @staticmethod
    def employer_contribution_parse(value, row_no):
        if DEBUG:
            logging.info("Employer Contribution parse: " + str(value))
        if value:
            value = PrepHelper.convert_to_float(value)
            if DEBUG:
                logging.info("Employer Contribution parse:" + str(value))
            return value
        else:
            if DEBUG:
                logging.info("Employer Contribution Empty updated:" + str(EMPTY_FLOAT))
            return EMPTY_FLOAT
    
    
    @staticmethod
    def employee_annual_contribution_parse(value,months):
        if DEBUG:
            logging.info("Employee Contribution  parse: " + str(value))
        if value:
            value = PrepHelper.convert_to_float(value)
            months = PrepHelper.convert_to_float(months)
            value = value * months
            if DEBUG:
                logging.info("Employee Annual Contribution  parse: " + str(value))
            return value
        else:
            if DEBUG:
                logging.info("Employee Annual Contribution Empty updated: " + str(EMPTY_FLOAT))
            return EMPTY_FLOAT
    
    
    @staticmethod
    def employer_annual_contribution_parse(value,months):
        if DEBUG:
            logging.info("Employer Contribution  parse: " + str(value))
        if value:
            value = PrepHelper.convert_to_float(value)
            months = PrepHelper.convert_to_float(months)
            value = value * months
            if DEBUG:
                logging.info("Employer Annual Contribution  parse: " + str(value))
            return value
        else:
            if DEBUG:
                logging.info("Employer Annual Contribution Empty updated: " + str(EMPTY_FLOAT))
            return EMPTY_FLOAT
            
            
        
        
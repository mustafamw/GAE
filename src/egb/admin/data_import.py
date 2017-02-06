#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import csv
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader('jinja'))

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers 

from egb.generic.product import ProductTypeHelper

from egb.user.user import UserModel

from egb.employee.employee import EmployeeModel
from egb.generic.employee import EmployeeTypeHelper

from egb.employer.employer import EmployerModel
from egb.employer.employer_helper import EmployerHelper

from egb.provider.provider import ProviderModel

from egb.health_assessment.health_assessment import HealthAssessmentModel
from egb.generic.health_assessment import HealthAssessmentTypeHelper

from egb.dental.dental import DentalModel
from egb.generic.dental import DentalTypeHelper

from egb.pension.pension import PensionModel
from egb.pension.pension import ListFundModel
from egb.pension.pension import FundSelectionModel
from egb.generic.pension import PensionTypeHelper

from egb.life.life import LifeModel

from egb.gip.gip import GipModel
from egb.generic.gip import GipTypeHelper

from egb.cic.cic import CicModel

from egb.pmi.pmi import PMIModel
from egb.generic.pmi import PmiTypeHelper

from egb.cashplan.cashplan import CashplanModel
from egb.generic.cashplan import CashplanTypeHelper

from egb.ccv.ccv import CcvModel

from egb.car.car import CarSignupModel, CarModel
from egb.generic.car import CarTypeHelper

from egb.ctw.ctw import CtwModel, CtwSignupModel
from egb.generic.ctw import CtwTypeHelper

from egb.whitegood.whitegood import WhitegoodModel, WhitegoodSignupModel
from egb.generic.whitegood import WhitegoodTypeHelper

from egb.ess.ess import EssModel
from egb.generic.ess import EssTypeHelper

from egb.payslip.payslips import PayslipModel

from egb.holiday.holiday import HolidayModel
from egb.generic.holiday import HolidayTypeHelper

from egb.flood.flood_helper import Flood

from egb.login.login_helper import LoginHelper

from libs.tokenGenerate.token import Token

from libs.date_time.date_time import DateTime

from libs.parse.parse import Parse

from libs.secure.jwt_helper import JwtHelper

from google.appengine.ext import ndb


EMPLOYER_NAME = 'egb'

IMPORT_LIST = {}
IMPORT_LIST['employer_import'] = {'name':'employer_import'}
IMPORT_LIST['user_import'] = {'name':'user_import'}
IMPORT_LIST['employee_import'] = {'name':'employee_import'}
IMPORT_LIST['provider_import'] = {'name':'provider_import'}
IMPORT_LIST['pension_import'] = {'name':'pension_import'}
IMPORT_LIST['life_import'] = {'name':'life_import'}
IMPORT_LIST['cic_import'] = {'name':'cic_import'}
IMPORT_LIST['gip_import'] = {'name':'gip_import'}
IMPORT_LIST['pmi_import'] = {'name':'pmi_import'}
IMPORT_LIST['cp_import'] = {'name':'cp_import'}
IMPORT_LIST['ha_import'] = {'name':'ha_import'}
IMPORT_LIST['ccv_import'] = {'name':'ccv_import'}
IMPORT_LIST['car_signup_import'] = {'name':'car_signup_import'}
IMPORT_LIST['ctw_signup_import'] = {'name':'ctw_signup_import'}
IMPORT_LIST['ess_import'] = {'name':'ess_import'}
IMPORT_LIST['holiday_import'] = {'name':'holiday_import'}
IMPORT_LIST['payslips_import'] = {'name':'payslips_import'}
IMPORT_LIST['dental_import'] = {'name':'dental_import'}
IMPORT_LIST['white_good_signup_import'] = {'name':'white_good_signup_import'}
        
epoc_date = "01.01.1970"


class LoginErrorMessage:
    
    incorrect_login = "Incorrect Login" 
    account_blocked = "Account Blocked"
    logged_out = "Logged Out"
    locked_out = "You have been locked out for 5 minutes"

    def getMessage(self, error):
        if error == 1:
            return self.incorrect_login
        elif error == 2:
            return self.account_blocked
        elif error == 3:
            return self.logged_out
        elif error == 4:
            return self.locked_out
        else:
            return self.incorrect_login
        
        
class DataImportProcess(Parse, Token, EmployerHelper):
    
    def csv_reader(self, user_info):
        
        return csv.reader(user_info, delimiter=',', dialect=csv.excel_tab)
    
    
    def process_employer_import(self, user_info):
        
        user_info = blobstore.BlobReader(user_info.key())
        
        reader = self.csv_reader(user_info)
        
        skip = True
        
        for row in reader:
            
            if skip is False:
            
                name = self.stringToLower(row[0]) 
                variation = self.parseInteger(row[1]) 
                window_life_start = self.parseDate(row[2])
                window_life_end = self.parseDate(row[3])
                window_cic_start = self.parseDate(row[4]) 
                window_cic_end = self.parseDate(row[5])
                window_pmi_start = self.parseDate(row[6])
                window_pmi_end = self.parseDate(row[7]) 
                window_ctw_start = self.parseDate(row[8]) 
                window_ctw_end = self.parseDate(row[9]) 
                window_wg_start = self.parseDate(row[10])
                window_wg_end = self.parseDate(row[11])
                web_link = row[12] 
                handbook_link = row[13] 
                contact_link = row[14] 
                contact_email = self.stringToLower(row[15]) 
                contact_phone = row[16] 
                bumf = row[17] 
                email_ess = row[18] 
                email_holiday = row[19] 
                email_pension = row[20] 
                email_life = row[21] 
                email_cic = row[22]
                email_gip = row[23] 
                email_cp = row[24] 
                email_dental = row[25] 
                email_ha = row[26] 
                email_hr = row[27] 
                email_default = row[28] 
                image_links = row[29] 
                welcome_note = self.stringToLower(row[30]) 
                company_icon = row[31]
                company_slogan = self.stringToLower(row[32])
                
                variation = self.get_variation(variation)    
                
                qryEmployer = EmployerModel.query(EmployerModel.name==name).get()
                
                if qryEmployer:
                    
                    pass 
                
                else:
                    
                    entry = EmployerModel(name=name,
                                         variation=variation,
                                         window_life_start=window_life_start,
                                         window_life_end=window_life_end,
                                         window_cic_start=window_cic_start,
                                         window_cic_end=window_cic_end,
                                         window_pmi_start=window_pmi_start,
                                         window_pmi_end=window_pmi_end,
                                         window_ctw_start=window_ctw_start,
                                         window_ctw_end=window_ctw_end,
                                         window_wg_start=window_wg_start,
                                         window_wg_end=window_wg_end,
                                         web_link=web_link,
                                         handbook_link=handbook_link,
                                         contact_link=contact_link,
                                         contact_email=contact_email,
                                         contact_phone=contact_phone,
                                         bumf=bumf,
                                         email_ess=email_ess,
                                         email_holiday=email_holiday,
                                         email_pension=email_pension,
                                         email_life=email_life,
                                         email_cic=email_cic,
                                         email_gip=email_gip,
                                         email_cp=email_cp,
                                         email_dental=email_dental,
                                         email_ha=email_ha,
                                         email_hr=email_hr,
                                         email_default=email_default,
                                         image_links=image_links,
                                         welcome_note=welcome_note ,
                                         company_icon=company_icon,
                                         company_slogan=company_slogan)
                    entry.put()
                
            skip = False
            
            
    def process_user_import(self, user_info):
    
        user_info = blobstore.BlobReader(user_info.key())
        
        reader = self.csv_reader(user_info)
        
        skip = True
        
        for row in reader:
    
            if skip is False:
                
                user_id = self.parseInteger(row[0]) 
                employee_id = self.parseInteger(row[1]) 
                email = self.stringToLower(row[2]) 
                username = self.stringToLower(row[3]) 
                password = self.stringToLower(row[4]) 
                dob = self.parseDate(row[5]) 
                android_id = row[6] 
                android_gcm = row[7] 
                android_pin = self.parseInteger(row[8]) 
                iphone_id = row[9] 
                iphone_gcm = row[10] 
                iphone_pin = self.parseInteger(row[11]) 
                status = self.parseInteger(row[12])
                roles = self.stringToLower(row[13])
                hashed = self.generate_token()
                access_token = self.generate_token()
                
                if not android_pin:
                    android_pin = [0]
                
                if not iphone_pin:
                    iphone_pin = [0]
                
                rolesArr = roles.split(',')
                
                if not rolesArr:
                    
                    rolesArr = 'authenticated'
                
                qryUser = UserModel.query(UserModel.user_id == user_id, UserModel.employee_id == employee_id).get();
                
                if qryUser:
                    qryUser.created = DateTime.getCurrentDateTime()
                    qryUser.status = status
                    #qryUser.access_token = access_token
                    qryUser.put();
                    
                else:
                    
                    employer = EmployerModel.query(EmployerModel.name==EMPLOYER_NAME).get().key
                    
                    entry = UserModel(employer=employer,
                                      user_id=user_id,
                                      employee_id=employee_id,
                                      email=email,
                                      username=username,
                                      password=password,
                                      dob=dob,
                                      android_id=[android_id],
                                      android_gcm=[android_gcm],
                                      android_pin=[android_pin],
                                      iphone_id=[iphone_id],
                                      iphone_gcm=[iphone_gcm],
                                      iphone_pin=[iphone_pin],
                                      hash=hashed,
                                      access_token=access_token,
                                      status=status,
                                      roles=rolesArr)
                    entry.put()
                    
            skip = False
            
    def process_employee_import(self, user_info):
        
        user_info = blobstore.BlobReader(user_info.key())
        
        reader = self.csv_reader(user_info)
        
        skip = True
        
        for row in reader:
            
            if skip is False:
            
                user_id = self.parseInteger(row[0]) 
                employee_id = self.parseInteger(row[1]) 
                job_title = self.stringToLower(row[2]).split(',') 
                start_date = self.parseDate(row[3]) 
                end_date = self.parseDate(row[4]) 
                salary = self.parseFloat(row[5]) 
                hourly_rate = self.parseFloat(row[6]) 
                currency = row[7]
                bonus = self.parseFloat(row[8]) 
                commission = self.parseFloat(row[9]) 
                overtime = self.parseFloat(row[10]) 
                weekly_hours = self.parseFloat(row[11])
                gender = self.parseInteger(row[12])
                
                gender = EmployeeTypeHelper().get_geneder_type(gender) 
                
                qryEmployee = EmployeeModel.query(EmployeeModel.user_id==user_id).get()
                if qryEmployee:
                    
                    qryEmployee.gender = gender
                    qryEmployee.put()
                
                else:
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    entry = EmployeeModel(user=qryUser,
                                          user_id=user_id,
                                          gender=gender,
                                          employee_id=employee_id,
                                          job_title=job_title,
                                          start_date=start_date,
                                          end_date=end_date,
                                          salary=salary,
                                          hourly_rate=hourly_rate,
                                          currency=currency,
                                          bonus=bonus,
                                          commission=commission,
                                          overtime=overtime,
                                          weekly_hours=weekly_hours)
                    entry.put()
                
            skip = False
            
            
    def process_provider_import(self, user_info):
        
        user_info = blobstore.BlobReader(user_info.key())
        
        reader = self.csv_reader(user_info)
        
        skip = True
        
        for row in reader:
            
            if skip is False:
            
                provider_name = self.stringToLower(row[0]) 
                product_type = self.parseInteger(row[1]) 
                product_variation = self.parseInteger(row[2]) 
                web_link = row[3] 
                icon_link = row[4] 
                bumf = self.stringToLower(row[5])
                
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                
                qryProvider = ProviderModel.query(ProviderModel.provider_name==provider_name).get()
                
                if qryProvider:
                    
                    pass
                
                else:
        
                    entry = ProviderModel(provider_name=provider_name,
                                         product_type=product_type,
                                         product_variation=product_variation,
                                         web_link=web_link,
                                         icon_link=icon_link,
                                         bumf=bumf)
                    entry.put()
                
            skip = False
            
    def process_pension_import(self, user_info):
        
        user_info = blobstore.BlobReader(user_info.key())
        
        reader = self.csv_reader(user_info)
        
        skip = True
        
        for row in reader:
            
            if skip is False:
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                start_date = self.parseDate(row[4]) 
                end_date = self.parseDate(row[5]) 
                fund_value = self.parseFloat(row[6]) 
                valuation_date = self.parseDate(row[7]) 
                employee_contribution = self.parseFloat(row[8]) 
                employer_contribution = self.parseFloat(row[9]) 
                employee_contribution_percent = self.parseFloat(row[10]) 
                employer_contribution_percent = self.parseFloat(row[11]) 
                min_employee_contribution_percent = self.parseFloat(row[12])
                max_employee_contribution_percent = self.parseFloat(row[13])
                min_employer_contribution_percent = self.parseFloat(row[14])
                max_employer_contribution_percent = self.parseFloat(row[15])
                tax_saving = PensionTypeHelper().get_tax_saving_type(row[16])
                wish_expression_link = row[17]
                list_funds = row[18]
                fund_selections = row[19]
                
                list_fundsArr = []
                if list_funds:
                    for fund in list_funds.split(','):
                        fund = fund.split('|')
                        list_fundsArr.append(ListFundModel(name=fund[0], value=float(fund[1])))
                else:
                    list_fundsArr = []
                    
                list_fund_selectionsArr = []
                if fund_selections:
                    for selection in fund_selections.split(','):
                        selection = selection.split('|')
                        list_fund_selectionsArr.append(FundSelectionModel(name=selection[0], percent=float(selection[1])))
                else:
                    list_fund_selectionsArr = []
                    
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                
                if not end_date:
                    end_date = epoc_date
    
                qry = PensionModel.query(PensionModel.user_id==user_id).get()
                
                if qry:
                    
                    qry.provider_name = provider_name
                    qry.put()
                    
                else:
                    qry = UserModel.query(UserModel.user_id==user_id).get().key
                    entry = PensionModel(user=qry,
                                         user_id=user_id,
                                         provider_name=provider_name,
                                         product_type=product_type,
                                         product_variation=product_variation,
                                         start_date=start_date,
                                         end_date=end_date,
                                         fund_value=fund_value,
                                         valuation_date=valuation_date,
                                         employee_contribution=employee_contribution,
                                         employer_contribution=employer_contribution,
                                         employee_contribution_percent=employee_contribution_percent,
                                         employer_contribution_percent=employer_contribution_percent,
                                         min_employee_contribution_percent=min_employee_contribution_percent,
                                         max_employee_contribution_percent=max_employee_contribution_percent,
                                         min_employer_contribution_percent=min_employer_contribution_percent,
                                         max_employer_contribution_percent=max_employer_contribution_percent,
                                         tax_saving=tax_saving,
                                         wish_expression_link=wish_expression_link,
                                         list_fund=list_fundsArr,
                                         fund_selection=list_fund_selectionsArr)
                    entry.put()
                
            skip = False
            
    def process_life_import(self, user_info):
        
        user_info = blobstore.BlobReader(user_info.key())
        
        reader = self.csv_reader(user_info)
        
        skip = True
        
        for row in reader:
            
            if skip is False:
            
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                calculate = row[4] 
                sum_assured = self.parseFloat(row[5]) 
                core_multiple = self.parseFloat(row[6]) 
                flexible = row[7] 
                flex_multiple = self.parseFloat(row[8]) 
                flex_max_multiple = self.parseFloat(row[9]) 
                free_cover_limit = self.parseFloat(row[10]) 
                cap = self.parseFloat(row[11]) 
                premium_core = self.parseFloat(row[12]) 
                gross_cost = self.parseFloat(row[13]) 
                wish_expression_link = row[14]
                window_salary = self.parseFloat(row[15])
                             
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                
                qryLife = LifeModel.query(LifeModel.user_id==user_id).get()
                
                if qryLife:
                    
                    pass
                
                else:
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    
                    entry = LifeModel(user=qryUser,
                                      user_id=user_id,
                                      provider_name=provider_name,
                                      product_type=product_type,
                                      product_variation=product_variation,
                                      calculate=(calculate=="true"),
                                      sum_assured=sum_assured,
                                      core_multiple=core_multiple,
                                      flexible=(flexible=="true"),
                                      flex_multiple=flex_multiple,
                                      flex_max_multiple=flex_max_multiple,
                                      free_cover_limit=free_cover_limit,
                                      cap=cap,
                                      premium_core=premium_core,
                                      gross_cost=gross_cost,
                                      wish_expression_link=wish_expression_link,
                                      window_salary=window_salary)
                    entry.put()
                
            skip = False
            
    def process_cic_import(self, user_info):
        
        user_info = blobstore.BlobReader(user_info.key())
        
        reader = self.csv_reader(user_info)
        
        skip = True
        
        for row in reader:
            
            if skip is False:
            
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                calculate = row[4] 
                sum_assured = self.parseFloat(row[5]) 
                core_multiple = self.parseFloat(row[6]) 
                flexible = row[7] 
                flex_multiple = self.parseFloat(row[8]) 
                flex_max_multiple = self.parseFloat(row[9]) 
                free_cover_limit = self.parseFloat(row[10]) 
                cap = self.parseFloat(row[11])  
                premium_core = self.parseFloat(row[12]) 
                gross_cost = self.parseFloat(row[13])  
                window_salary = self.parseFloat(row[14]) 
        
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                
                qryCIC = CicModel.query(CicModel.user_id==user_id).get()
                
                if qryCIC:
                    
                    pass
                
                else:
                    
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    
                    entry = CicModel(user=qryUser,
                                     user_id=user_id,
                                     provider_name=provider_name,
                                     product_type=product_type,
                                     product_variation=product_variation,
                                     calculate=(calculate == 'true'),
                                     sum_assured=sum_assured,
                                     core_multiple=core_multiple,
                                     flexible=(flexible == 'true'),
                                     flex_multiple=flex_multiple,
                                     flex_max_multiple=flex_max_multiple,
                                     free_cover_limit=free_cover_limit,
                                     cap=cap,
                                     premium_core=premium_core,
                                     gross_cost=gross_cost,
                                     window_salary=window_salary)
                    entry.put()
                
            skip = False
            
    def process_gip_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
         
        for row in reader:
             
            if skip is False:
             
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                percentage = self.parseFloat(row[4])
                premium_percentage = self.parseFloat(row[5])  
                deferred_period = self.parseInteger(row[6]) 
                payment_term = self.parseInteger(row[7]) 
                flexible = self.stringToLower(row[8]) 
                free_cover_limit =  self.parseFloat(row[9]) 
                payment_period =  self.parseFloat(row[10]) 
                premium_core =  self.parseFloat(row[11]) 
                gross_cost =  self.parseFloat(row[12])
                window_salary = self.parseFloat(row[13]) 
                     
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                deferred_period = GipTypeHelper().get_deferred_type(0)
                payment_term = GipTypeHelper().get_payment_term_type(payment_term)
                
                qryGip = GipModel.query(GipModel.user_id==user_id).get()
        
                if qryGip:
                    pass
                else:
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    entry = GipModel(user=qryUser,
                                     user_id=user_id,
                                     provider_name=provider_name,
                                     product_type=product_type,
                                     product_variation=product_variation,
                                     percentage=percentage,
                                     premium_percentage=premium_percentage,
                                     deferred_period=deferred_period,
                                     payment_term=payment_term,
                                     flexible=(flexible == 'true'),
                                     free_cover_limit=free_cover_limit,
                                     payment_period=payment_period,
                                     premium_core=premium_core,
                                     gross_cost=gross_cost,
                                     window_salary=window_salary)
                    entry.put()
                 
            skip = False
             
    def process_pmi_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
         
        for row in reader:
             
            if skip is False:
                
                print row
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                flexible = self.stringToLower(row[4]) 
                who = self.parseInteger(row[5])
                premium_who = self.parseInteger(row[6])
                cover_level = self.parseInteger(row[7]) 
                premium_cover_level = self.parseInteger(row[8]) 
                where = self.parseInteger(row[9]) 
                excess = self.parseFloat(row[10])
                premium_core = self.parseFloat(row[11])  
                gross_cost = self.parseFloat(row[12]) 
                
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                
                who = PmiTypeHelper.get_who_type(who)
                premium_who = PmiTypeHelper.get_who_type(premium_who)
                
                where = PmiTypeHelper.get_cover_where(where)
                
                cover_level = PmiTypeHelper.get_cover_level(cover_level)
                premium_cover_level = PmiTypeHelper.get_cover_level(premium_cover_level)
    
    
                qryPmi = PMIModel.query(PMIModel.user_id==user_id).get()
                
                if qryPmi:
                    
                    pass
                
                else:
                    
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    
                    entry = PMIModel(user = qryUser,
                                     user_id=user_id,
                                     provider_name=provider_name,
                                     product_type=product_type,
                                     product_variation=product_variation,
                                     flexible=(flexible == "true"),
                                     who=who,
                                     premium_who=premium_who,
                                     cover_level=cover_level,
                                     premium_cover_level=premium_cover_level,
                                     where=where,
                                     excess=excess,
                                     premium_core=premium_core,
                                     gross_cost=gross_cost)
                    entry.put()
                 
            skip = False
             
    def process_cp_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
         
        for row in reader:
             
            if skip is False:
             
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                who = self.parseInteger(row[4]) 
                premium_who = self.parseInteger(row[5]) 
                cover_level = self.parseInteger(row[6])
                premium_cover_level = self.parseInteger(row[7])
                gross_cost = self.parseFloat(row[8]) 
                premium_core = self.parseFloat(row[9]) 
                
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
            
                who = CashplanTypeHelper.get_who_type(who)
                premium_who = CashplanTypeHelper.get_who_type(who)
                cover_level = CashplanTypeHelper.get_cover_level(cover_level)
                premium_cover_level = CashplanTypeHelper.get_cover_level(cover_level)
                
                qryCp = CashplanModel.query(CashplanModel.user_id==user_id).get()
                
                if qryCp:
                    
                    pass
                
                else:
                    
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    entry = CashplanModel(user=qryUser,
                                          user_id=user_id,
                                          provider_name=provider_name,
                                          product_type=product_type,
                                          product_variation=product_variation,
                                          who=who,
                                          premium_who=premium_who,
                                          cover_level=cover_level,
                                          premium_cover_level=premium_cover_level,
                                          premium_core=premium_core,
                                          gross_cost=gross_cost)
                    entry.put()
    
            skip = False
             
    def process_dental_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
         
        for row in reader:
             
            if skip is False:
             
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                flexible = self.stringToLower(row[4]) 
                who = self.parseInteger(row[5])
                premium_who = self.parseInteger(row[6])
                cover_level = self.parseInteger(row[7])
                premium_cover_level = self.parseInteger(row[8])
                premium_core = self.parseFloat(row[9]) 
                gross_cost = self.parseFloat(row[10]) 
                     
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                
                who = DentalTypeHelper.get_who_type(who)
                premium_who = DentalTypeHelper.get_who_type(premium_who)
                cover_level = DentalTypeHelper.get_cover_level(cover_level)
                premium_cover_level = DentalTypeHelper.get_cover_level(premium_cover_level)
                
                qryDental = DentalModel.query(DentalModel.user_id==user_id).get()
                
                if qryDental:
                    
                    pass
                
                else:
                    
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    
                    entry = DentalModel(user=qryUser,
                                        user_id=user_id,
                                        provider_name=provider_name,
                                        product_type=product_type,
                                        product_variation=product_variation,
                                        flexible=(flexible == "true"),
                                        who=who,
                                        premium_who=premium_who,
                                        cover_level=cover_level,
                                        premium_cover_level=premium_cover_level,
                                        premium_core=premium_core,
                                        gross_cost=gross_cost)
                    entry.put()
                 
            skip = False
             
    def process_ha_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
         
        for row in reader:
             
            if skip is False:
    
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                flexible = self.stringToLower(row[4]) 
                who = self.parseInteger(row[5]) 
                cover_level = self.parseInteger(row[6]) 
                premium_core = self.parseFloat(row[7]) 
                premium_flex = self.parseFloat(row[8]) 
                gross = self.parseFloat(row[9]) 
                net = self.parseFloat(row[10])
    
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                who = HealthAssessmentTypeHelper.get_who_type(who)
                cover_level = HealthAssessmentTypeHelper.get_cover_level(cover_level)
    
                
                qryHealthAssessment = HealthAssessmentModel.query(HealthAssessmentModel.user_id==user_id).get()
                
                if qryHealthAssessment:
                    
                    pass
                
                else:
                    
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    
                    entry = HealthAssessmentModel(user=qryUser,
                                                  user_id=user_id,
                                                  provider_name=provider_name,
                                                  product_type=product_type,
                                                  product_variation=product_variation,
                                                  flexible=(flexible == "true"),
                                                  who=who,
                                                  cover_level=cover_level,
                                                  premium_core=premium_core,
                                                  premium_flex=premium_flex,
                                                  gross=gross,
                                                  net=net)
                    entry.put()
                 
            skip = False
             
    def process_ccv_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
         
        for row in reader:
             
            if skip is False:
             
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                employee_contribution = self.parseFloat(row[4]) 
                protected_rights =  self.stringToLower(row[5]) 
                     
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                
                qryCcv = CcvModel.query(CcvModel.user_id==user_id).get()
                
                if qryCcv:
                    
                    pass
        
                else:
                    
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
    
                    entry = CcvModel(user=qryUser,
                                     user_id=user_id,
                                     provider_name=provider_name,
                                     product_type=product_type,
                                     product_variation=product_variation,
                                     contribution=employee_contribution,
                                     protected_rights=(protected_rights=="TRUE"))
                    entry.put()
                 
            skip = False
            
             
    def process_car_signup_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
        
        data_user_idArr = {}
                
        for row in reader:
             
            if skip is False:
             
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                gross_cost = self.parseFloat(row[4]) 
                submitted = self.parseDate(row[5])
                token = self.generate_token()
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                status = CarTypeHelper.get_status_type(3)
                data_user_idArr[user_id] = user_id
                qryCarSignup = CarSignupModel.query(CarSignupModel.user_id==user_id).get()
                
                if qryCarSignup:
                    
                    pass
                
                else:
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    entry = CarSignupModel(user=qryUser,
                                           user_id=user_id,
                                           provider_name=provider_name,
                                           product_type=product_type,
                                           product_variation=product_variation,
                                           gross_cost=gross_cost,
                                           status=status,
                                           token=token,
                                           submitted=submitted)
                    entry.put()
                

            skip = False
                    
                    
        qryCar = CarModel.query().fetch()
        
        for car in qryCar:
                        
            if not car.user_id in data_user_idArr:
        
                car.gross_cost = 0
                car.status = CarTypeHelper.get_status_type(5)
                car.put()

        qryCarSignup = CarSignupModel.query().fetch()
        
        for car_signup in qryCarSignup:
                        
            if not car_signup.user_id in data_user_idArr:
        
                car_signup.gross_cost = 0
                car_signup.status = CarTypeHelper.get_status_type(5)
                car_signup.put()

             
    def process_ctw_signup_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
        
        data_user_idArr = {} 
        
        for row in reader:
             
            if skip is False:
             
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                gross_cost = self.parseFloat(row[4]) 
                submitted = self.parseDate(row[5])
                token = self.generate_token()
                data_user_idArr[user_id] = user_id
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                status = CtwTypeHelper.get_status_type(3)
                    
                    
                qryCtwSignup = CtwSignupModel.query(CtwSignupModel.user_id==user_id).get()
                
                if qryCtwSignup:
                    
                    pass
                
                else:
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    entry = CtwSignupModel(user=qryUser,
                                           user_id=user_id,
                                           provider_name=provider_name,
                                           product_type=product_type,
                                           product_variation=product_variation,
                                           gross_cost=gross_cost,
                                           status=status,
                                           token=token,
                                           submitted=submitted)
                    entry.put()
                 
            skip = False
            
        qryCtw = CtwModel.query().fetch()
        
        for ctw in qryCtw:
                        
            if not ctw.user_id in data_user_idArr:
        
                ctw.gross_cost = 0
                ctw.status = CtwTypeHelper.get_status_type(5)
                ctw.put()
                

        qryCtwSignup = CtwSignupModel.query().fetch()
        
        for ctw_signup in qryCtwSignup:
                        
            if not ctw_signup.user_id in data_user_idArr:
        
                ctw_signup.gross_cost = 0
                ctw_signup.status = CtwTypeHelper.get_status_type(5)
                ctw_signup.put()


    def process_white_good_signup_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
        
        data_user_idArr = {} 
        
        for row in reader:
             
            if skip is False:
             
                user_id = self.parseInteger(row[0]) 
                provider_name = self.stringToLower(row[1]) 
                product_type = self.parseInteger(row[2]) 
                product_variation = self.parseInteger(row[3]) 
                gross_cost = self.parseFloat(row[4]) 
                submitted = self.parseDate(row[5])
                token = self.generate_token()
                data_user_idArr[user_id] = user_id
                product_type = ProductTypeHelper.get_product_type(product_type)
                product_variation = ProductTypeHelper.get_product_variation(product_variation)
                status = WhitegoodTypeHelper.get_status_type(3)
                    
                qryWhiteGoodsSignup = WhitegoodSignupModel.query(WhitegoodSignupModel.user_id==user_id).get()
                
                if qryWhiteGoodsSignup:
                    
                    pass
                
                else:
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    entry = WhitegoodSignupModel(user=qryUser,
                                                  user_id=user_id,
                                                  provider_name=provider_name,
                                                  product_type=product_type,
                                                  product_variation=product_variation,
                                                  gross_cost=gross_cost,
                                                  status=status,
                                                  token=token,
                                                  submitted=submitted)
                    entry.put()
                 
            skip = False
            
        qryWhiteGoods = WhitegoodModel.query().fetch()
        
        for white_goods in qryWhiteGoods:
                        
            if not white_goods.user_id in data_user_idArr:
        
                white_goods.gross_cost = 0
                white_goods.status = CtwTypeHelper.get_status_type(5)
                white_goods.put()
                

        qryWhiteGoodsSignup = WhitegoodSignupModel.query().fetch()
        
        for white_goods_signup in qryWhiteGoodsSignup:
                        
            if not white_goods_signup.user_id in data_user_idArr:
        
                white_goods_signup.gross_cost = 0
                white_goods_signup.status = CtwTypeHelper.get_status_type(5)
                white_goods_signup.put()

                
             
    def process_ess_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True

        for row in reader:
    
            if skip is False:
            
                user_id = self.parseInteger(row[0])
                title = self.parseInteger(row[1])  
                firstname = self.stringToLower(row[2]) 
                lastname = self.stringToLower(row[3])  
                maiden_name = self.stringToLower(row[4]) 
                address = self.stringToLower(row[5]) 
                city = self.stringToLower(row[6])  
                county = self.stringToLower(row[7]) 
                postcode = self.stringToLower(row[8]) 
                contact_no = row[9] 
                bank_holder_name = self.stringToLower(row[10]) 
                bank_name = self.stringToLower(row[11]) 
                account_no = self.parseInteger(row[12]) 
                sort_code = row[13]
                ni_no = row[14]
                
                title = EssTypeHelper().get_title_type(title)
                
                qryEss = EssModel.query(EssModel.user_id==user_id).get()
                
                if qryEss:
                    
                    pass
                
                else:
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    entry = EssModel(user=qryUser,
                                     user_id=user_id,
                                     title=title,
                                     firstname=firstname,
                                     lastname=lastname,
                                     maiden_name=maiden_name,
                                     address=address,
                                     city=city,
                                     county=county,
                                     postcode=postcode,
                                     contact_no=contact_no,
                                     bank_holder_name=bank_holder_name,
                                     bank_name=bank_name,
                                     account_no=account_no,
                                     sort_code=sort_code,
                                     ni_no=ni_no)
                    entry.put()
                 
            skip = False
             
    def process_holiday_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
         
        reader = self.csv_reader(user_info)
         
        skip = True
         
        for row in reader:
             
            if skip is False:
             
                user_id = self.parseInteger(row[0]) 
                team = self.stringToLower(row[1])
                days_off = self.stringToLower(row[2])
                allowance = self.parseFloat(row[3]) 
                allowance_type = self.parseInteger(row[4]) 
                year = self.parseInteger(row[5])
                
                if days_off:
                    days_off = days_off.split(',')
                else:
                    days_off = []
                
                allowance_type = HolidayTypeHelper.get_allowance_type(allowance_type)
                
                if not allowance:
                    allowance = 0.0
         
                qryHolidayDetails = HolidayModel.query(HolidayModel.user_id == user_id,
                                                             HolidayModel.year == year).get()
                if qryHolidayDetails:
                    
                    qryHolidayDetails.days_off = days_off
                    qryHolidayDetails.allowance = allowance
                    qryHolidayDetails.allowance_type = allowance_type
                    qryHolidayDetails.team = team
                    qryHolidayDetails.year = year
                    qryHolidayDetails.put()
    
                else:
                    qryUser = UserModel.query(UserModel.user_id==user_id).get().key
                    entry = HolidayModel(user=qryUser,
                                         user_id=user_id,
                                         team=team,
                                         days_off = days_off,
                                         allowance=allowance,
                                         allowance_type=allowance_type,
                                         year=year)
                    entry.put()
                 
            skip = False
    
             
    def process_payslips_import(self, user_info):
         
        user_info = blobstore.BlobReader(user_info.key())
        
        reader = self.csv_reader(user_info)
         
        skip = True
         
        for row in reader:
             
            if skip is False:
             
                user_id = self.parseInteger(row[0]) 
                employer_name = self.stringToLower(row[1]) 
                employee_number = self.parseInteger(row[2]) 
                department = self.stringToLower(row[3]) 
                process_date = self.parseDate(row[4]) 
                tax_week = self.parseInteger(row[5]) 
                tax_code = self.stringToLower(row[6]) 
                ni_number = self.stringToLower(row[7]) 
                ni_code = self.stringToLower(row[8]) 
                paye = self.parseFloat(row[9]) 
                payment = self.stringToLower(row[10]) 
                deduction = self.stringToLower(row[11]) 
                ee_national_insurance = self.parseFloat(row[12]) 
                employee_pension = self.parseFloat(row[13]) 
                tax_credit = self.parseFloat(row[14]) 
                ssp = self.parseFloat(row[15]) 
                smp_spp = self.parseFloat(row[16]) 
                attachment_of_earnings = self.parseFloat(row[17]) 
                admin_fee = self.parseFloat(row[18]) 
                total_payment = self.parseFloat(row[19]) 
                total_deductions = self.parseFloat(row[20]) 
                gross_for_tax_td = self.parseFloat(row[21]) 
                tax_paid_td = self.parseFloat(row[22]) 
                tax_credit_td = self.parseFloat(row[23]) 
                earnings_for_ni_td = self.parseFloat(row[24]) 
                ni_td = self.parseFloat(row[25]) 
                employer_pension = self.parseFloat(row[26]) 
                employer_pension_td = self.parseFloat(row[27])
                total_gross_tax_td = self.parseFloat(row[28]) 
                earning_for_ni = self.parseFloat(row[29]) 
                gross_for_tax = self.parseFloat(row[30]) 
                net_pay = self.parseFloat(row[31]) 
                payment_method = self.stringToLower(row[32]) 
                payment_period = self.stringToLower(row[33]) 
                sac_pension = self.parseFloat(row[34])
                year = DateTime.getDateYear(process_date)
    
                if not tax_credit:
                    tax_credit = 0
                    
                qryPayslip = PayslipModel.query(PayslipModel.tax_week == tax_week).get()
                
                if qryPayslip:
                    
                    pass
                
                else:
                    qryUser = UserModel.query(UserModel.user_id == user_id, UserModel.employee_id == employee_number).get().key
                    entry = PayslipModel(user=qryUser,
                                         user_id=user_id,
                                         employer_name=employer_name,
                                         employee_number=employee_number,
                                         department=department,
                                         process_date=process_date,
                                         year=year,
                                         tax_week=int(tax_week),
                                         tax_code=tax_code,
                                         ni_number=ni_number,
                                         ni_code=ni_code,
                                         paye=paye,
                                         payment=payment,
                                         deduction=deduction,
                                         ee_national_insurance=ee_national_insurance,
                                         employee_pension=employee_pension,
                                         tax_credit=tax_credit,
                                         ssp=ssp,
                                         smp_spp=smp_spp,
                                         attachment_of_earnings=attachment_of_earnings,
                                         admin_fee=admin_fee,
                                         total_payment=total_payment,
                                         total_deductions=total_deductions,
                                         gross_for_tax_td=gross_for_tax_td,
                                         tax_paid_td=tax_paid_td,
                                         tax_credit_td=tax_credit_td,
                                         earnings_for_ni_td=earnings_for_ni_td,
                                         ni_td=ni_td,
                                         employer_pension=employer_pension,
                                         employer_pension_td=employer_pension_td,
                                         total_gross_tax_td=total_gross_tax_td,
                                         earning_for_ni=earning_for_ni,
                                         gross_for_tax=gross_for_tax,
                                         net_pay=net_pay,
                                         payment_method=payment_method,
                                         payment_period=payment_period,
                                         sac_pension=sac_pension)
                    entry.put()
                 
            skip = False
        

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler, DataImportProcess):
    
    def get(self):
        
        self.redirect("/main")  
        
            
    def post(self):
    
        user_import_file = self.get_uploads(IMPORT_LIST['user_import']['name'])
        imported_file = ""
        
        if user_import_file:
            imported_file = IMPORT_LIST['user_import']['name'] 
            file_info = user_import_file[0]           
            self.process_user_import(user_import_file[0])            
            blobstore.delete(file_info.key())  # optional: delete file after import
            
        employee_import_file = self.get_uploads(IMPORT_LIST['employee_import']['name'])
        
        if employee_import_file:
            imported_file = IMPORT_LIST['employee_import']['name'] 
            file_info = employee_import_file[0]            
            self.process_employee_import(employee_import_file[0])            
            blobstore.delete(file_info.key()) 
        
        employer_import_file = self.get_uploads(IMPORT_LIST['employer_import']['name'])
        
        if employer_import_file:
            imported_file = IMPORT_LIST['employer_import']['name'] 
            file_info = employer_import_file[0]           
            self.process_employer_import(employer_import_file[0])            
            blobstore.delete(file_info.key())
            
        provider_import_file = self.get_uploads(IMPORT_LIST['provider_import']['name'])  
                
        if provider_import_file:
            imported_file = IMPORT_LIST['provider_import']['name']             
            file_info = provider_import_file[0]           
            self.process_provider_import(provider_import_file[0])            
            blobstore.delete(file_info.key()) 
                        
        pension_import_file = self.get_uploads(IMPORT_LIST['pension_import']['name']) 
        
        if pension_import_file:
            imported_file = IMPORT_LIST['pension_import']['name']   
            file_info = pension_import_file[0]            
            self.process_pension_import(pension_import_file[0])            
            blobstore.delete(file_info.key()) 
            
        life_import_file = self.get_uploads(IMPORT_LIST['life_import']['name'])  
        
        if life_import_file:
            imported_file = IMPORT_LIST['life_import']['name']   
            file_info = life_import_file[0]            
            self.process_life_import(life_import_file[0])            
            blobstore.delete(file_info.key()) 
        
        cic_import_file = self.get_uploads(IMPORT_LIST['cic_import']['name'])  
        
        if cic_import_file:
            imported_file = IMPORT_LIST['cic_import']['name']   
            file_info = cic_import_file[0]           
            self.process_cic_import(cic_import_file[0])            
            blobstore.delete(file_info.key())      
        
        gip_import_file = self.get_uploads(IMPORT_LIST['gip_import']['name'])  
        
        if gip_import_file:
            imported_file = IMPORT_LIST['gip_import']['name']   
            file_info = gip_import_file[0]           
            self.process_gip_import(gip_import_file[0])            
            blobstore.delete(file_info.key())
            
        pmi_import_file = self.get_uploads(IMPORT_LIST['pmi_import']['name'])  
        
        if pmi_import_file:
            imported_file = IMPORT_LIST['pmi_import']['name']   
            file_info = pmi_import_file[0]            
            self.process_pmi_import(pmi_import_file[0])            
            blobstore.delete(file_info.key())
            
        cp_import_file = self.get_uploads(IMPORT_LIST['cp_import']['name']) 
        
        if cp_import_file:
            imported_file = IMPORT_LIST['cp_import']['name']  
            file_info = cp_import_file[0]           
            self.process_cp_import(cp_import_file[0])            
            blobstore.delete(file_info.key())
            
        dental_import_file = self.get_uploads(IMPORT_LIST['dental_import']['name']) 
        
        if dental_import_file:
            imported_file = IMPORT_LIST['dental_import']['name']   
            file_info = dental_import_file[0]            
            self.process_dental_import(dental_import_file[0])            
            blobstore.delete(file_info.key())
            
        ha_import_file = self.get_uploads(IMPORT_LIST['ha_import']['name']) 
        
        if ha_import_file:
            imported_file = IMPORT_LIST['ha_import']['name']  
            file_info = ha_import_file[0]           
            self.process_ha_import(ha_import_file[0])            
            blobstore.delete(file_info.key())
            
        ccv_import_file = self.get_uploads(IMPORT_LIST['ccv_import']['name']) 
        
        if ccv_import_file:
            imported_file = IMPORT_LIST['ccv_import']['name']  
            file_info = ccv_import_file[0]            
            self.process_ccv_import(ccv_import_file[0])            
            blobstore.delete(file_info.key())
            
        car_signup_import = self.get_uploads(IMPORT_LIST['car_signup_import']['name']) 
        
        if car_signup_import:
            imported_file = IMPORT_LIST['car_signup_import']['name']  
            file_info = car_signup_import[0]           
            self.process_car_signup_import(car_signup_import[0])            
            blobstore.delete(file_info.key())

        white_good_signup_import = self.get_uploads(IMPORT_LIST['white_good_signup_import']['name']) 
        
        if white_good_signup_import:
            imported_file = IMPORT_LIST['white_good_signup_import']['name']  
            file_info = white_good_signup_import[0]           
            self.process_white_good_signup_import(white_good_signup_import[0])            
            blobstore.delete(file_info.key())   
            
        ctw_signup_import_file = self.get_uploads(IMPORT_LIST['ctw_signup_import']['name']) 
        
        if ctw_signup_import_file:
            imported_file = IMPORT_LIST['ctw_signup_import']['name']  
            file_info = ctw_signup_import_file[0]            
            self.process_ctw_signup_import(ctw_signup_import_file[0])            
            blobstore.delete(file_info.key())
            
        ess_import_file = self.get_uploads(IMPORT_LIST['ess_import']['name']) 
        
        if ess_import_file:
            imported_file = IMPORT_LIST['ess_import']['name']  
            file_info = ess_import_file[0]            
            self.process_ess_import(ess_import_file[0])            
            blobstore.delete(file_info.key())
            
        holiday_import_file = self.get_uploads(IMPORT_LIST['holiday_import']['name']) 
        
        if holiday_import_file:
            imported_file = IMPORT_LIST['holiday_import']['name']  
            file_info = holiday_import_file[0]           
            self.process_holiday_import(holiday_import_file[0])            
            blobstore.delete(file_info.key())
            

        payslips_import_file = self.get_uploads(IMPORT_LIST['payslips_import']['name'])  
        
        if payslips_import_file:
            imported_file = IMPORT_LIST['payslips_import']['name'] 
            file_info = payslips_import_file[0]           
            self.process_payslips_import(payslips_import_file[0])            
            blobstore.delete(file_info.key())
            
         
        self.redirect("/main?imported_file=%s" % (imported_file))
        

class NewImportHandler(webapp2.RequestHandler):
    
    def get(self):
        
        imported_file = self.request.get("imported_file")

        upload_url = blobstore.create_upload_url('/upload')
    
        userDetails = {'firstname':'New',
                       'lastname':'New'}
        #count    
        IMPORT_LIST['employer_import']['count'] = EmployerModel.get_count()
        IMPORT_LIST['user_import']['count'] = UserModel.get_count()
        IMPORT_LIST['employee_import']['count'] = EmployeeModel.get_count()
        IMPORT_LIST['provider_import']['count'] = ProviderModel.get_count()
        IMPORT_LIST['pension_import']['count'] = PensionModel.get_count()
        IMPORT_LIST['life_import']['count'] = LifeModel.get_count()
        IMPORT_LIST['cic_import']['count'] = CicModel.get_count()
        IMPORT_LIST['gip_import']['count'] = GipModel.get_count()
        IMPORT_LIST['pmi_import']['count'] = PMIModel.get_count()
        IMPORT_LIST['cp_import']['count'] = CashplanModel.get_count()
        IMPORT_LIST['ha_import']['count'] = HealthAssessmentModel.get_count()
        IMPORT_LIST['ccv_import']['count'] = CcvModel.get_count()
        IMPORT_LIST['car_signup_import']['count'] = CarSignupModel.get_count()
        IMPORT_LIST['ctw_signup_import']['count'] = CtwSignupModel.get_count()
        IMPORT_LIST['ess_import']['count'] = EssModel.get_count()
        IMPORT_LIST['holiday_import']['count'] = HolidayModel.get_count()
        IMPORT_LIST['payslips_import']['count'] = PayslipModel.get_count()
        IMPORT_LIST['dental_import']['count'] = DentalModel.get_count()
        IMPORT_LIST['white_good_signup_import']['count'] = WhitegoodSignupModel.get_count()
        
        #submitted    
        IMPORT_LIST['employer_import']['submitted'] = EmployerModel.get_submitted()
        IMPORT_LIST['user_import']['submitted'] = UserModel.get_submitted()
        IMPORT_LIST['employee_import']['submitted'] = EmployeeModel.get_submitted()
        IMPORT_LIST['provider_import']['submitted'] = ProviderModel.get_submitted()
        IMPORT_LIST['pension_import']['submitted'] = PensionModel.get_submitted()
        IMPORT_LIST['life_import']['submitted'] = LifeModel.get_submitted()
        IMPORT_LIST['cic_import']['submitted'] = CicModel.get_submitted()
        IMPORT_LIST['gip_import']['submitted'] = GipModel.get_submitted()
        IMPORT_LIST['pmi_import']['submitted'] = PMIModel.get_submitted()
        IMPORT_LIST['cp_import']['submitted'] = CashplanModel.get_submitted()
        IMPORT_LIST['ha_import']['submitted'] = HealthAssessmentModel.get_submitted()
        IMPORT_LIST['ccv_import']['submitted'] = CcvModel.get_submitted()
        IMPORT_LIST['car_signup_import']['submitted'] = CarSignupModel.get_submitted()
        IMPORT_LIST['ctw_signup_import']['submitted'] = CtwSignupModel.get_submitted()
        IMPORT_LIST['ess_import']['submitted'] = EssModel.get_submitted()
        IMPORT_LIST['holiday_import']['submitted'] = HolidayModel.get_submitted()
        IMPORT_LIST['payslips_import']['submitted'] = PayslipModel.get_submitted()
        IMPORT_LIST['dental_import']['submitted'] = DentalModel.get_submitted()
        IMPORT_LIST['white_good_signup_import']['submitted'] = WhitegoodSignupModel.get_submitted()
                        
        import_value = {'upload_url':upload_url,
                        'user_detail':userDetails,
                        'import_list':IMPORT_LIST,
                        'imported_file':imported_file}
            
        template = JINJA_ENVIRONMENT.get_template('import.html')
            
        self.response.write(template.render(import_value))


    
class ImportHandler(webapp2.RequestHandler, JwtHelper):
    
    def get(self):
        
        imported_file = self.request.get("imported_file")
        
        token = self.request.cookies.get("token")
        
        userDetails = {"firstname":"Coming",
                        "lastname":"Soon"}
        
        upload_url = blobstore.create_upload_url('/upload')
        
        if token:
        
            ip_address = self.request.host
            
            payload = self.decode_jwt_admin_import(token, ip_address)
    
            if payload:
                
                client_id = payload['client_id']
                user_id = payload['user_id']

                qryEss = EssModel.query(EssModel.user==ndb.Key('UserModel', client_id), EssModel.user_id==user_id).get()
            
                if qryEss:
                    userDetails = {"firstname":qryEss.firstname,
                                   "lastname":qryEss.lastname}
                    
            #count    
            IMPORT_LIST['employer_import']['count'] = EmployerModel.get_count()
            IMPORT_LIST['user_import']['count'] = UserModel.get_count()
            IMPORT_LIST['employee_import']['count'] = EmployeeModel.get_count()
            IMPORT_LIST['provider_import']['count'] = ProviderModel.get_count()
            IMPORT_LIST['pension_import']['count'] = PensionModel.get_count()
            IMPORT_LIST['life_import']['count'] = LifeModel.get_count()
            IMPORT_LIST['cic_import']['count'] = CicModel.get_count()
            IMPORT_LIST['gip_import']['count'] = GipModel.get_count()
            IMPORT_LIST['pmi_import']['count'] = PMIModel.get_count()
            IMPORT_LIST['cp_import']['count'] = CashplanModel.get_count()
            IMPORT_LIST['ha_import']['count'] = HealthAssessmentModel.get_count()
            IMPORT_LIST['ccv_import']['count'] = CcvModel.get_count()
            IMPORT_LIST['car_signup_import']['count'] = CarSignupModel.get_count()
            IMPORT_LIST['ctw_signup_import']['count'] = CtwSignupModel.get_count()
            IMPORT_LIST['ess_import']['count'] = EssModel.get_count()
            IMPORT_LIST['holiday_import']['count'] = HolidayModel.get_count()
            IMPORT_LIST['payslips_import']['count'] = PayslipModel.get_count()
            IMPORT_LIST['dental_import']['count'] = DentalModel.get_count()
            IMPORT_LIST['white_good_signup_import']['count'] = WhitegoodSignupModel.get_count()
            
            #submitted    
            IMPORT_LIST['employer_import']['submitted'] = EmployerModel.get_submitted()
            IMPORT_LIST['user_import']['submitted'] = UserModel.get_submitted()
            IMPORT_LIST['employee_import']['submitted'] = EmployeeModel.get_submitted()
            IMPORT_LIST['provider_import']['submitted'] = ProviderModel.get_submitted()
            IMPORT_LIST['pension_import']['submitted'] = PensionModel.get_submitted()
            IMPORT_LIST['life_import']['submitted'] = LifeModel.get_submitted()
            IMPORT_LIST['cic_import']['submitted'] = CicModel.get_submitted()
            IMPORT_LIST['gip_import']['submitted'] = GipModel.get_submitted()
            IMPORT_LIST['pmi_import']['submitted'] = PMIModel.get_submitted()
            IMPORT_LIST['cp_import']['submitted'] = CashplanModel.get_submitted()
            IMPORT_LIST['ha_import']['submitted'] = HealthAssessmentModel.get_submitted()
            IMPORT_LIST['ccv_import']['submitted'] = CcvModel.get_submitted()
            IMPORT_LIST['car_signup_import']['submitted'] = CarSignupModel.get_submitted()
            IMPORT_LIST['ctw_signup_import']['submitted'] = CtwSignupModel.get_submitted()
            IMPORT_LIST['ess_import']['submitted'] = EssModel.get_submitted()
            IMPORT_LIST['holiday_import']['submitted'] = HolidayModel.get_submitted()
            IMPORT_LIST['payslips_import']['submitted'] = PayslipModel.get_submitted()
            IMPORT_LIST['dental_import']['submitted'] = DentalModel.get_submitted()
            IMPORT_LIST['white_good_signup_import']['submitted'] = WhitegoodSignupModel.get_submitted()
            
            import_value = {'upload_url':upload_url,
                            'user_detail':userDetails,
                            'import_list':IMPORT_LIST,
                            'imported_file':imported_file}
            
            template = JINJA_ENVIRONMENT.get_template('import.html')
            
            self.response.write(template.render(import_value))
            
        else:
            self.response.delete_cookie('token')
            self.redirect("/login?error=3")

class LoginHandler(webapp2.RequestHandler, LoginErrorMessage, LoginHelper):
    
    def get(self):
        
        qryUser = UserModel.query().count()
        
        if qryUser == 0:
            self.redirect('/new')

        token = self.request.cookies.get("token")
        error = self.request.get('error')
        
        message_value = {'message':''}
        
        if token:
            self.redirect("/main")
        
        elif error:
            error = int(error)
            error_message = self.getMessage(error)
            message_value = {'message':error_message}
            

        template = JINJA_ENVIRONMENT.get_template('login.html')
        
        self.response.write(template.render(message_value))
        
        
    def post(self):
                
        username = self.request.get("username")
        password = self.request.get("password")
        
        ip_address = self.request.host

        
        qryUser = UserModel.query(UserModel.username==username, 
                                  UserModel.password==password,
                                  UserModel.roles.IN(['administration'])).get()

        if qryUser:
            
            if qryUser.status == 0:
                self.redirect('/login?error=2')
    
            flood = Flood.checkFlood(username, ip_address)
            if flood:
                self.redirect('/login?error=4')
            
            qryUser.logged_in = DateTime.getCurrentDateTime()
            qryUser.put()
            
            token = self.encode_desktop(qryUser, ip_address)
            
            # Saves a cookie in the client.
            self.response.set_cookie('token', token.token)
            
            self.redirect('/main')
        
        else:
            flood = Flood.createFlood(username, ip_address)
            if flood:
                self.redirect('/login?error=4')
            else:
                self.redirect('/login?error=1')
            
class LogoutHandler(webapp2.RequestHandler):
    
    def get(self):
        # Deletes a cookie previously set in the client.
        self.response.delete_cookie('token')
        self.redirect("/login")

                
app = webapp2.WSGIApplication([
    ('/', LoginHandler),
    ('/login', LoginHandler),
    ('/new', NewImportHandler),
    ('/main', ImportHandler),
    ('/upload', UploadHandler),
    ('/logout', LogoutHandler)
], debug=True)


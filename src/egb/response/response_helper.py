"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 12 Jan 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from egb.user.user import UserModel
from egb.employer.employer import EmployerModel
from egb.employee.employee import EmployeeModel
from egb.pmi.pmi import PMIModel
from egb.life.life import LifeModel
from egb.ctw.ctw import CtwModel
from egb.cic.cic import CicModel
from egb.provider.provider import ProviderModel
from egb.pension.pension import PensionModel
from egb.ccv.ccv import CcvModel
from egb.gip.gip import GipModel
from egb.car.car import CarModel
from egb.dental.dental import DentalModel
from egb.ess.ess import EssModel
from egb.health_assessment.health_assessment import HealthAssessmentModel

from egb.utils.error import ErrorHelper

from egb.response.response import EmployerResponse
from egb.response.response import LifeResponse
from egb.response.response import Response
from egb.response.response import PmiResponse
from egb.response.response import CtwResponse
from egb.response.response import CicResponse
from egb.response.response import PensionResponse
from egb.response.response import CcvResponse
from egb.response.response import GipResponse
from egb.response.response import CarResponse
from egb.response.response import DentalResponse
from egb.response.response import HaResponse
from egb.response.response import EmployeeResponse
from egb.response.response import EssResponse
from egb.response.response import ProductResponse
from egb.response.response import SelfServiceResponse
from egb.response.response import CompanyResponse


from protorpc import messages
from datetime import datetime
from google.appengine.ext import ndb

import endpoints


EPOC_DATE = "01.01.1970" 
EMPTY_LIST = ['','','',False]
EMPTY_LIST_ESS = ['','','']
EMPTY_LIST_EMPLOYEE = ['','','','']
  
        
class ResponseHelper:
    
    RESPONSE_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    # added the static decorator to avoid the requirement of an instance
    def get_providers(self, provider_name, product_type, product_variation):
        
        # this is a variable and a list
        # should be lower case and pluralised
        providers = ProviderModel.query(ProviderModel.product_variation == product_variation, 
                                        ProviderModel.product_type == product_type,
                                        ProviderModel.provider_name == provider_name).get()
        if providers:
            return providers
        else:
            raise ErrorHelper.provider_not_found()
    
    # added the static decorator to avoid the requirement of an instance
    def has_left(self, client_id, user_id):
        # changing variable name to employees
        # removed ndb.and
        employees = EmployeeModel.query(EmployeeModel.user == ndb.Key('UserModel',client_id) , EmployeeModel.user_id == user_id).get()
        
        if employees:
            
            # More simplistic approach to converting datetime object to String
            employee_end = employees.end_date.strftime('%d.%m.%Y')
            
            # Use an or statement and a constant for the date
            # First check if it's empty for performance
            if employee_end or employee_end == EPOC_DATE:
                # If these conditions are true, the employer has not left
                return False

            # We could assume that if there is an end date other than the above
            # then the employer has left, as it could only be a valid end date

            return True
    
    # new helper method
    def check_window(self, window_start, window_end):     
        # You were converting dates to strings previously
        # You were using the < > operators which shouldn't work on Strings?
        today = datetime.now()
        todaysformat = today.strftime("%Y-%m-%d")
        window_start = datetime.strptime(str(window_start), "%Y-%m-%d").strftime("%Y-%m-%d")
        window_end = datetime.strptime(str(window_end), "%Y-%m-%d").strftime("%Y-%m-%d")
        if window_start <= todaysformat <= window_end:
            return True
        else:
            return False
        
    #Return empty response
    def empty_response(self, name_response):
        empty_response = name_response(provider_name='',
                                     icon_link='',
                                     web_link='',
                                     window=False)
        return empty_response
        
    
    # added the static decorator to avoid the requirement of an instance
    # renamed to avoid confusion
    def create_response(self, client_id, user_id):
        # renamed for readability
        response_object = {}
        
        # changed variable to lower case and plural for list
        # removed ndb and

        qryUser = UserModel.query(UserModel.key == ndb.Key('UserModel' , client_id) , UserModel.user_id==user_id).get().employer                                   
        employers = EmployerModel.query(ancestor=qryUser).get()
        employer_name = employers.name
                                       
        employer = EmployerModel.query(EmployerModel.name == employer_name).get()
        
        # rather than indenting all further code check for an error
        # I believe this will terminate here
        if not employer:
            raise ErrorHelper.employer_not_found()
        
        # Creating a dictionary is a good idea to store the values until you create the response
        # In python arrays can contain anything
        # So we'll construct the classes and append as we go           
        employer_response = EmployerResponse(image_links=employer.image_links,
                             welcome_note=employer.welcome_note,
                             company_icon=employer.company_icon,
                             company_slogan=employer.company_slogan)
        
        response_object['employer_response'] = employer_response
        
        #
        # Handle life
        #
        
        
        # renamed variable
        # removed ndb.and
        life = LifeModel.query(LifeModel.user == ndb.Key('UserModel' , client_id) , LifeModel.user_id == user_id).get()
        
        if life:
            # here we know the user has a life policy
            # We don't need to check any policy start or end dates?
            # Unless it's a pension?                 
            provider = self.get_providers(life.provider_name, 
                                                    life.product_type, 
                                                    life.product_variation)
            
            # We need to check if its availability is subject to a window
            # We need more fields to potentially promote the product
            # That data is held on the employer table         
            window_open = self.check_window(employer.window_life_start, 
                                                      employer.window_life_end)


            life_response = LifeResponse(provider_name=provider.provider_name,
                             icon_link=provider.icon_link,
                             web_link=provider.web_link,
                             window=window_open)
            
            response_object['life_response'] = life_response
        else:
            # Rather than appending an empty LifeResponse class
            # append False which we can check below           

            response_object['life_response'] = self.empty_response(LifeResponse)
            
            
        #Changed PMI
        pmi = PMIModel.query(PMIModel.user == ndb.Key('UserModel' , client_id) , PMIModel.user_id == user_id).get()
        
        if pmi:
            provider = self.get_providers(pmi.provider_name, 
                                                            pmi.product_type, 
                                                            pmi.product_variation)
 
            window_open = self.check_window(employer.window_pmi_start, 
                                                      employer.window_pmi_end)

            pmi_response = PmiResponse(provider_name=provider.provider_name,
                            icon_link=provider.icon_link,
                            web_link=provider.web_link,
                            window=window_open)
            
            response_object['pmi_response'] = pmi_response
            
        else:
            
            response_object['pmi_response'] = self.empty_response(PmiResponse)
        
        
        #Changed CTW
        ctw = CtwModel.query(CtwModel.user == ndb.Key('UserModel' , client_id) , CtwModel.user_id == user_id).get()
        
        if ctw:
            
            provider = self.get_providers(ctw.provider_name, ctw.product_type, ctw.product_variation)
            
            window_open = self.check_window(employer.window_pmi_start, employer.window_pmi_end)
            
            ctw_response = CtwResponse(provider_name=provider.provider_name,
                            icon_link=provider.icon_link,
                            web_link=provider.web_link,
                            window=window_open)
            
            response_object['ctw_response'] = ctw_response
            
        else:

            response_object['ctw_response'] = self.empty_response(CtwResponse)
        
        
        #Changed CIC
        cic = CicModel.query(CicModel.user == ndb.Key('UserModel' , client_id) , CicModel.user_id == user_id).get()
        
        if cic:
            
            provider = self.get_providers(cic.provider_name, cic.product_type, cic.product_variation)
            
            window_open = self.check_window(employer.window_cic_start, employer.window_cic_end)
            
            cic_response = CicResponse(provider_name=provider.provider_name,
                            icon_link=provider.icon_link,
                            web_link=provider.web_link,
                            window=window_open)

            response_object['cic_response'] = cic_response
        else:
            
            response_object['cic_response'] = self.empty_response(CicResponse)
        
        
        #Changed Pension
        pension = PensionModel.query(PensionModel.user == ndb.Key('UserModel' , client_id) , PensionModel.user_id == user_id).get()
        
        if pension:
    
            provider = self.get_providers(pension.provider_name, pension.product_type, pension.product_variation)
            
            pension_response = PensionResponse(provider_name=provider.provider_name,
                                icon_link=provider.icon_link,
                                web_link=provider.web_link,
                                window=True)

            response_object['pension_response'] = pension_response
        else:

            response_object['pension_response'] = self.empty_response(PensionResponse)
        
        
        #Changed CCV
        ccv = CcvModel.query(CcvModel.user == ndb.Key('UserModel' , client_id) , CcvModel.user_id == user_id).get()
        
        if ccv:

            provider = self.get_providers(ccv.provider_name, ccv.product_type, ccv.product_variation)
            
            ccv_response = CcvResponse(provider_name=provider.provider_name,
                            icon_link=provider.icon_link,
                            web_link=provider.web_link,
                            window=True)

            response_object['ccv_response'] = ccv_response
        else:

            response_object['ccv_response'] = self.empty_response(CcvResponse)
        
        
        #Changed GIP
        gip = GipModel.query(GipModel.user == ndb.Key('UserModel' , client_id) , GipModel.user_id == user_id).get()
        
        if gip:
            
            provider = self.get_providers(gip.provider_name, gip.product_type, gip.product_variation)
            
            gip_response = GipResponse(provider_name=provider.provider_name,
                            icon_link=provider.icon_link,
                            web_link=provider.web_link,
                            window=True)
            
            response_object['gip_response'] = gip_response
            
        else:

            response_object['gip_response'] = self.empty_response(GipResponse)
        
        
        #Changed Car
        car = CarModel.query(CarModel.user == ndb.Key('UserModel' , client_id) , CarModel.user_id == user_id).get()
        
        if car:

            provider = self.get_providers(car.provider_name, 
                                                            car.product_type, 
                                                            car.product_variation)
            
            #window_open = self.check_window(car.start_date, car.end_date)
            
            
            car_response = CarResponse(provider_name=provider.provider_name,
                            icon_link=provider.icon_link,
                            web_link=provider.web_link,
                            window=False)
            

            response_object['car_response'] = car_response
        else:

            response_object['car_response'] = self.empty_response(CarResponse)
            
        
        #Changed Dental
        dental = DentalModel.query(DentalModel.user == ndb.Key('UserModel' , client_id) , DentalModel.user_id == user_id).get()
        
        if dental:

            provider = self.get_providers(dental.provider_name, 
                                                            dental.product_type, 
                                                            dental.product_variation)
            
            dental_response = DentalResponse(provider_name=provider.provider_name,
                              icon_link=provider.icon_link,
                              web_link=provider.web_link,
                              window=True)

            response_object['dental_response'] = dental_response
        else:

            response_object['dental_response'] = self.empty_response(DentalResponse)
        
        
        #Changed Health Assessment
        health_assessment = HealthAssessmentModel.query(HealthAssessmentModel.user == ndb.Key('UserModel' , client_id) , 
                                                        HealthAssessmentModel.user_id == user_id).get()
        
        if health_assessment:
            
            provider = self.get_providers(health_assessment.provider_name, 
                                                            health_assessment.product_type,
                                                            health_assessment.product_variation)
    
            health_assessment = HaResponse(provider_name=provider.provider_name,
                                 icon_link=provider.icon_link,
                                 web_link=provider.web_link,
                                 window=True)
            
            response_object['health_assessment'] = health_assessment
            
        else:
        
            response_object['health_assessment'] = self.empty_response(HaResponse)
        
        
        #Changed Employee    
        employee = EmployeeModel.query(EmployeeModel.user == ndb.Key('UserModel' , client_id) , EmployeeModel.user_id == user_id).get()
        
        if employee:

            start_date = datetime.strptime(str(employee.start_date), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.strptime(str(employee.end_date), "%Y-%m-%d").strftime("%Y-%m-%d")
            employee_response = EmployeeResponse(job_title=employee.job_title,
                                 start_date=start_date,
                                 end_date=end_date,
                                 annual_salary=employee.salary)
    
            response_object['employee_response'] = employee_response
            
        else:
            response_object['employee_response'] = EMPTY_LIST_EMPLOYEE
        
        
        #Changed ESS    
        ess = EssModel.query(EssModel.user == ndb.Key('UserModel' , client_id) , EssModel.user_id == user_id).get()
        if ess:
            
            ess_respone = EssResponse(firstname=ess.firstname,
                                      lastname=ess.lastname,
                                      contact_no=ess.contact_no)
            
            response_object['ess_response'] = ess_respone
        else:
            response_object['ess_response'] = EMPTY_LIST_ESS


        #Return Response Array
        return response_object
    
    def construct_response(self, responses):
        
        life_response = responses['life_response']
        pmi_response = responses['pmi_response']
        ctw_response = responses['ctw_response']
        cic_response = responses['cic_response']
        pension_response = responses['pension_response']
        ccv_response = responses['ccv_response']
        gip_response = responses['gip_response']
        car_response = responses['car_response']
        dental_response = responses['dental_response']
        ha_response = responses['health_assessment']
        employer_response = responses['employer_response']
        employee_response = responses['employee_response']
        ees_response = responses['ess_response']
        
        response_list =  Response(benefits_details=ProductResponse(life_details=life_response,
                                                                 pmi_details=pmi_response,
                                                                 ctw_details=ctw_response,
                                                                 cic_details=cic_response,
                                                                 pension_details=pension_response,
                                                                 ccv_details=ccv_response,
                                                                 gip_details=gip_response,
                                                                 car_details=car_response,
                                                                 dental_details=dental_response,
                                                                 health_assess_details=ha_response), 
                                  ess_details=SelfServiceResponse(ess_details=ees_response),
                                  company_details=CompanyResponse(employer_details=employer_response,
                                                                  employee_details=employee_response))
        return response_list



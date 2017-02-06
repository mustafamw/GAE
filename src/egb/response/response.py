"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 12 Jan 2016

@Mustafa Mohamed: mo.mustafa3@gmail.com
"""
from protorpc import messages

class CarResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)
    
class CcvResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)
    
class PensionResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)

class CtwResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)
    
class LifeResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)
    
class PmiResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)

class CicResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)

class GipResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)

class DentalResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)

# Let's call heath assessment HA from now on
class HaResponse(messages.Message):
    provider_name = messages.StringField(1, required=False)
    icon_link = messages.StringField(2, required=False)
    web_link = messages.StringField(3, required=False)
    window = messages.BooleanField(4, required=False)

class EmployeeResponse(messages.Message):
    job_title = messages.StringField(1, repeated=True)
    start_date = messages.StringField(2, required=False)
    end_date = messages.StringField(3, required=False)
    annual_salary = messages.FloatField(4, required=False)

# This is an acronym
class EssResponse(messages.Message):
    firstname = messages.StringField(1, required=False)
    lastname = messages.StringField(2, required=False)
    contact_no = messages.StringField(3, required=False)
    
class EmployerResponse(messages.Message):
    image_links = messages.StringField(1, required=False)
    welcome_note = messages.StringField(2, required=False)
    company_icon = messages.StringField(3, required=False)
    company_slogan = messages.StringField(4, required=False)

class ProductResponse(messages.Message):
    life_details = messages.MessageField(LifeResponse, 1, required=False)
    pmi_details = messages.MessageField(PmiResponse, 2, required=False)
    ctw_details = messages.MessageField(CtwResponse, 3, required=False)
    cic_details = messages.MessageField(CicResponse, 4, required=False)
    pension_details = messages.MessageField(PensionResponse, 5, required=False)
    ccv_details = messages.MessageField(CcvResponse, 6, required=False)
    gip_details = messages.MessageField(GipResponse, 7, required=False)
    car_details = messages.MessageField(CarResponse, 8, required=False)
    dental_details = messages.MessageField(DentalResponse, 9, required=False)
    health_assess_details = messages.MessageField(HaResponse, 10, required=False)
    
class SelfServiceResponse(messages.Message):
    ess_details = messages.MessageField(EssResponse, 1, required=False)

class CompanyResponse(messages.Message):
    employee_details = messages.MessageField(EmployeeResponse, 1, repeated=False)
    employer_details = messages.MessageField(EmployerResponse, 3, repeated=False)
     
class Response(messages.Message):
    # renamed variable
    benefits_details = messages.MessageField(ProductResponse, 1, repeated=False)
    ess_details = messages.MessageField(SelfServiceResponse, 2, repeated=False)
    company_details = messages.MessageField(CompanyResponse, 3, repeated=False)

    
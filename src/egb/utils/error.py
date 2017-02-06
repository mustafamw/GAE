NOT_AUTHORISED = 'Incorrect Login'
NOT_AUTHORISED_JWT = 'You are not authorised to view this information'
ACCOUNT_BLOCKED = 'Your account is not active'
ACCOUNT_LOCKED = 'Your account is locked for 5min'
INVALID_TOKEN = 'Invalid token'

NOT_FOUND_EMPLOYER = 'No such employer exists'
NOT_FOUND_EMPLOYEE = 'No such employee exists'
NOT_FOUND_PROVIDER = 'No such provider exists'
NOT_FOUND_PENSION = 'No such pension exists'
NOT_FOUND_PENSION_SIGNUP = 'No such pension signup exists'
NOT_FOUND_PENSION_LIST = 'No such pension list exists'
FOUND_PENSION_SIGNUP = "Pension Signup currently pending"
NOT_FOUND_LIFE = 'No such life exists'
NOT_FOUND_LIFE_SIGNUP = 'No such life signup exists'
NOT_FOUND_LIFE_LIST = 'No such life list exists'
NOT_FOUND_GIP = 'No such gip exists'
NOT_FOUND_GIP_SIGNUP = 'No such gip signup exists'
NOT_FOUND_CIC = 'No such cic exists'
NOT_FOUND_CIC_SIGNUP = 'No such cic signup exists'
NOT_FOUND_CIC_SIGNUP_LIST = 'No such cic signup list exists'
NOT_FOUND_CP = 'No such cashplan exists'
NOT_FOUND_CP_SIGNUP = 'No such cashplan signup exists'
NOT_FOUND_CP_LIST = 'No such cashplan list exists'
NOT_FOUND_CCV = 'No such ccv exists'
NOT_FOUND_CCV_SIGNUP = 'No such ccv signup exists'
NOT_FOUND_PMI = 'No such pmi exists'
NOT_FOUND_PMI_LIST = 'No such pmi list exists'
NOT_FOUND_DENTAL = 'No such dental exists'
NOT_FOUND_DENTAL = 'No such dental signup exists'
NOT_FOUND_HEALTH_ASSESSMENT = 'No such health assessment exists'
NOT_FOUND_CAR = 'No such car exists'
NOT_FOUND_CAR_SIGNUP = 'No such car signup exists'
NOT_FOUND_CTW = 'No such ctw exists'
NOT_FOUND_CTW_SIGNUP = 'No such ctw signup exists'
NOT_FOUND_WHITE_GOODS = 'No such white goods exists'
NOT_FOUND_WHITE_GOODS_SIGNUP = 'No such white goods signup exists'
NOT_FOUND_ESS = 'No such ess exists'
NOT_FOUND_ESS_UPDATED = 'No such ess updated exists'
NOT_FOUND_TRS = 'No such trs exists'
NOT_FOUND_PAYSLIP = 'No such payslip exists'
NOT_FOUND_PAYSLIP_DATES = 'No such payslip list of dates exists'
NOT_FOUND_HOLIDAY = 'No such holiday exists'
NOT_FOUND_HOLIDAY_BOOK = 'No such holiday book exists'
NOT_FOUND_HOLIDAY_BOOK_LIST = 'No such holiday book list exists'
NOT_FOUND_RESPONSE = 'No such response exists'
NOT_FOUND_USER = 'No such user exists'
NOT_FOUND_EMAIL = 'No such email exists'
NOT_FOUND_MAQUERADE = 'No such masquerade exists'
NOT_FOUND_NOTIFICATION = 'No such notification found'
NOT_FOUND_REWARD_POINT = 'No such reward point found'
REWARD_POINTS_NOT_INSERTED = "Rewards point not inserted"
DATA_ALREADY_EXISTS = "Data already exists"
NOT_FOUND_BENEFICIARY = "Beneficiary not found"
PASSWORD_INCORRECT = "1"

import endpoints

# https://cloud.google.com/appengine/docs/python/endpoints/exceptions
class ErrorHelper():
    
    @staticmethod
    def data_already_exists():
        return endpoints.BadRequestException(DATA_ALREADY_EXISTS)
    
    @staticmethod
    def beneficiary_not_found():
        return endpoints.NotFoundException(NOT_FOUND_BENEFICIARY)
    
    @staticmethod
    def reward_point_not_inserted():  
        return endpoints.UnauthorizedException(REWARD_POINTS_NOT_INSERTED)
    
    @staticmethod
    def reward_point_not_found():  
        return endpoints.NotFoundException(NOT_FOUND_REWARD_POINT)
    
    @staticmethod
    def unuthorised():  
        return endpoints.UnauthorizedException(NOT_AUTHORISED)
    
    @staticmethod
    def invalid_token():  
        return endpoints.UnauthorizedException(INVALID_TOKEN)
    
    @staticmethod
    def token_unuthorised():  
        return endpoints.UnauthorizedException(NOT_AUTHORISED_JWT)
    
    @staticmethod
    def account_locked():  
        return endpoints.UnauthorizedException(ACCOUNT_LOCKED)
    
    @staticmethod
    def reset_unauthorised():
        return endpoints.BadRequestException(INVALID_TOKEN)
    
    @staticmethod
    def account_blocked():  
        return endpoints.UnauthorizedException(ACCOUNT_BLOCKED)
    
    @staticmethod
    def notification_not_found():
        return endpoints.NotFoundException(NOT_FOUND_NOTIFICATION)
    
    @staticmethod
    def user_not_found():
        return endpoints.NotFoundException(NOT_FOUND_USER)
    
    @staticmethod
    def email_not_found():
        return endpoints.NotFoundException(NOT_FOUND_EMAIL)
    
    @staticmethod
    def maquerade_not_found():
        return endpoints.NotFoundException(NOT_FOUND_MAQUERADE)
    
    @staticmethod
    def ccv_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CCV)
    
    @staticmethod
    def ccv_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CCV_SIGNUP)
    
    @staticmethod
    def not_authorised():  
        return endpoints.NotFoundException(NOT_AUTHORISED)
    
    @staticmethod
    def employee_not_found():
        return endpoints.NotFoundException(NOT_FOUND_EMPLOYEE)
    
    @staticmethod
    def employer_not_found():
        return endpoints.NotFoundException(NOT_FOUND_EMPLOYER)
    
    @staticmethod
    def provider_not_found():
        return endpoints.NotFoundException(NOT_FOUND_PROVIDER)
    
    @staticmethod
    def pension_not_found():
        return endpoints.NotFoundException(NOT_FOUND_PENSION)
    
    @staticmethod
    def pension_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_PENSION_SIGNUP)
    
    @staticmethod
    def pension_signup_pending():
        return endpoints.BadRequestException(FOUND_PENSION_SIGNUP)
    
    @staticmethod
    def pension_list_not_found():
        return endpoints.NotFoundException(NOT_FOUND_PENSION_LIST)
    
    @staticmethod
    def life_not_found():
        return endpoints.NotFoundException(NOT_FOUND_LIFE)
    
    @staticmethod
    def life_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_LIFE_SIGNUP)

    @staticmethod
    def life_list_not_found():
        return endpoints.NotFoundException(NOT_FOUND_LIFE_LIST)
    
    @staticmethod
    def cic_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CIC)
    
    @staticmethod
    def cic_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CIC_SIGNUP)
    
    
    @staticmethod
    def cic_signup_list_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CIC_SIGNUP_LIST)
    
    @staticmethod
    def gip_not_found():
        return endpoints.NotFoundException(NOT_FOUND_GIP)
    
    @staticmethod
    def gip_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_GIP_SIGNUP)
    
    @staticmethod
    def cp_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CP)
    
    @staticmethod
    def cp_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CP_SIGNUP)
    
    @staticmethod
    def cp_list_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CP_LIST)
    
    @staticmethod
    def pmi_not_found():
        return endpoints.NotFoundException(NOT_FOUND_PMI)
    
    @staticmethod
    def pmi_list_not_found():
        return endpoints.NotFoundException(NOT_FOUND_PMI_LIST)
    
    @staticmethod
    def dental_not_found():
        return endpoints.NotFoundException(NOT_FOUND_DENTAL)
    
    @staticmethod
    def dental_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_DENTAL)
    
    @staticmethod
    def ha_not_found():
        return endpoints.NotFoundException(NOT_FOUND_HEALTH_ASSESSMENT)
        
    @staticmethod
    def car_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CAR)

    @staticmethod
    def car_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CAR_SIGNUP)
    
    @staticmethod
    def white_goods_not_found():
        return endpoints.NotFoundException(NOT_FOUND_WHITE_GOODS)

    @staticmethod
    def whitegood_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_WHITE_GOODS_SIGNUP)
    
    @staticmethod
    def ctw_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CTW)

    @staticmethod
    def ctw_signup_not_found():
        return endpoints.NotFoundException(NOT_FOUND_CTW_SIGNUP)
    
    @staticmethod
    def ess_not_found():
        return endpoints.NotFoundException(NOT_FOUND_ESS)
    

    @staticmethod
    def ess_updated_not_found():
        return endpoints.NotFoundException(NOT_FOUND_ESS_UPDATED)
    
    @staticmethod
    def trs_not_found():
        return endpoints.NotFoundException(NOT_FOUND_TRS)
    
    @staticmethod
    def payslip_not_found():
        return endpoints.NotFoundException(NOT_FOUND_PAYSLIP)
    
    @staticmethod
    def payslip_dates_not_found():
        return endpoints.NotFoundException(NOT_FOUND_PAYSLIP_DATES)

    @staticmethod
    def holiday_not_found():
        return endpoints.NotFoundException(NOT_FOUND_HOLIDAY)
    
    @staticmethod
    def holiday_book_not_found():
        return endpoints.NotFoundException(NOT_FOUND_HOLIDAY_BOOK)     

    @staticmethod
    def holiday_book_list_not_found():
        return endpoints.NotFoundException(NOT_FOUND_HOLIDAY_BOOK_LIST)     
    
    @staticmethod
    def response_not_found():
        return endpoints.NotFoundException(NOT_FOUND_RESPONSE)
    
    @staticmethod
    def not_authorised_jwt():  
        return endpoints.NotFoundException(NOT_AUTHORISED_JWT)
    

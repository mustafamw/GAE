'''
Copyright (C) 2016 EG Benefits. All rights reserved.
 
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 23 Nov 2016

@author: mustafa.mohamed@ernestgrant.com
'''
from egb.user.user import UserList
from egb.user.user import UserModel
from egb.user.user_helper import UserHelper

from egb.employee.employee import EmployeeList
from egb.employee.employee_helper import EmployeeTypeHelper

from egb.employer.employer import EmployerList
from egb.employer.employer_helper import EmployerHelper

from egb.provider.provider import ProviderList
from egb.provider.provider_helper import ProviderHelper

from egb.pension.pension import PensionList
from egb.pension.pension import PensionSignupResponse
from egb.pension.pension import PensionSignupList
from egb.pension.pension_helper import PensionHelper

from egb.life.life import LifeList, LifeSignupResponse, LifeSignupList
from egb.life.life_helper import LifeHelper

from egb.cic.cic import CicList, CicSignupResponse, CicSignupList
from egb.cic.cic_helper import CicHelper

from egb.cashplan.cashplan import CashplanList, CashplanSignupResponse, CashplanSignupList
from egb.cashplan.cashplan_helper import CashplanHelper

from egb.pmi.pmi import PMIList, PMISignupResponse, PMISignupList
from egb.pmi.pmi_helper import PmiHelper

from egb.dental.dental import DentalList, DentalSignupList, DentalSignupResponse
from egb.dental.dental_helper import DentalHelper

from egb.health_assessment.health_assessment import HealthAssessmentList
from egb.health_assessment.health_assessment_helper import HealthAssessHelper

from egb.ccv.ccv import CcvSignupResponse, CcvList, CcvSignupList
from egb.ccv.ccv_helper import CCVHelper

from egb.car.car import CarList, CarSignupList, CarSignupResponse
from egb.car.car_helper import CarHelper

from egb.ctw.ctw import CtwList, CtwSignupList, CtwSignupResponse
from egb.ctw.ctw_helper import CtwHelper

from egb.whitegood.whitegood import WhiteGoodList, WhitegoodSignupList, WhiteGoodSignupResponse
from egb.whitegood.whitegood_helper import WhitegoodHelper

from egb.ess.ess import EssList, EssResponse, EssUpdatedList
from egb.ess.ess_helper import EssHelper

from egb.total_reward.total_reward import TotalReward
from egb.total_reward.total_reward_helper import TotalRewardHelper

from egb.payslip.payslips import PayslipList, PayslipDates
from egb.payslip.payslips_helper import PayslipHelper

from egb.holiday.holiday import HolidayDetailList
from egb.holiday.holiday import HolidayDetailResponse
from egb.holiday.holiday import HolidayBookResponse
from egb.holiday.holiday import HolidayBookList

from egb.holiday.holiday_helper import HolidayHelper

from egb.gip.gip import GipList, GipSignupList, GipSignupResponse
from egb.gip.gip_helper import GipHelper

from egb.response.response import Response
from egb.response.response_helper import ResponseHelper

from egb.login.login_helper import LoginHelper
from egb.login.login import LoginDesktopResponse
from egb.login.login import LoginMobileResponse

from egb.refresh_token.refresh_token_helper import REFRESH_TOKEN_CONTAINER

from egb.logout.logout import LogoutResponse
from egb.logout.logout import LOGOUT_CONTAINER
from egb.logout.logout_helper import LogoutHelper

from egb.password_recovery.password_recovery import ResetPasswordResponse
from egb.password_recovery.password_recovery import ChangePasswordResponse
from egb.password_recovery.password_helper import PasswordReset

from egb.masquerade.masquerade import Masquerade
from egb.masquerade.masquerade import MasqueradeResponse
from egb.masquerade.masquerade_helper import MaqueradeHelper

from egb.notification.notification import NotificationResponse
from egb.notification.notification import NotificationList 
from egb.notification.notification_helper import NotificationHelper

from egb.reward_point.reward_point import RewardPointResponse
from egb.reward_point.reward_point import RewardPointList
from egb.reward_point.reward_point_helper import RewardPointHelper

from egb.beneficiary.beneficiary import Beneficiary
from egb.beneficiary.beneficiary_helper import BeneficiaryHelper

from egb.wage_check.wage_check import WageCheckList
from egb.wage_check.wage_check_helper import WageListHelper

from egb.flood.flood_helper import Flood

from egb.utils.error import ErrorHelper

from libs.secure.jwt_helper import JwtHelper
from libs.tokenGenerate.token import Token

from google.appengine.ext import ndb
from protorpc import remote
from libs.date_time.date_time import DateTime
import endpoints
      

egb_api = endpoints.api(name='platform', version='v1', description='Debug Platform API')

@egb_api.api_class(resource_name='Login')
class LoginDesktopApi(remote.Service, LoginHelper):
    @endpoints.method(LoginHelper.LOGIN_CONTAINER, 
                      LoginDesktopResponse,
                      name='desktop',
                      path='login/desktop',
                      http_method='POST') 
    
    def login(self, request):
        
        username = request.username
        password = request.password
        
        ip_address =  self.request_state.headers['host']
        
        qryUser = self.login_check(username, password)
        
        if qryUser:
            if qryUser.status == 0:
                raise ErrorHelper.account_blocked()
        
            Flood.checkFlood(username, ip_address)
            
            qryUser.logged_in = DateTime.getCurrentDateTime()
            qryUser.put()
                
            return self.encode_desktop(qryUser, ip_address)
        
        else:
        
            flood = Flood.createFlood(username, ip_address)
            if flood:
                raise ErrorHelper.account_locked()
            else:
                raise ErrorHelper.unuthorised()


@egb_api.api_class(resource_name='Login')
class LoginMobileApi(remote.Service, LoginHelper):
    @endpoints.method(LoginHelper.LOGIN_CONTAINER, LoginMobileResponse,
                      name='mobile',
                      path='login/mobile',
                      http_method='POST') 
    
    def login(self, request):
        
        username = request.username
        password = request.password
        
        ip_address =  self.request_state.headers['host']

        qryUser = self.login_check(username, password)

        if qryUser:
    
            if qryUser.status == 0:
                raise ErrorHelper.account_blocked()
            
            Flood.checkFlood(username, ip_address)
            
            encodeJwt = self.encode_mobile(qryUser, ip_address)
            
            return encodeJwt
        
        else:
        
            flood = Flood.createFlood(username, ip_address)
            if flood:
                raise ErrorHelper.account_locked()
            else:
                raise ErrorHelper.unuthorised()
        
        

@egb_api.api_class(resource_name='Refresh')
class RefreshTokenAPI(remote.Service, LoginHelper):
    @endpoints.method(REFRESH_TOKEN_CONTAINER, LoginDesktopResponse,
                      name='token',
                      path='login/refresh',
                      http_method='POST') 
    
    def refresh_token(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
                                        
        client_id = payload['client_id']
        user_id = payload['user_id']
        
        qryUser = UserModel.query(UserModel.key==ndb.Key('UserModel', client_id), 
                                  UserModel.user_id==user_id).get()

        if qryUser:
            
            if qryUser.status == 0:
                raise ErrorHelper.account_blocked()
            
            qryUser.logged_in = DateTime.getCurrentDateTime()
            qryUser.put()
            
            encodeJwt = self.encode_desktop(qryUser, ip_address)
            
            return encodeJwt
        
        
@egb_api.api_class(resource_name='Logout')
class LogoutApi(remote.Service):
    @endpoints.method(LOGOUT_CONTAINER, LogoutResponse,
                      name='logout',
                      path='user/logout',
                      http_method='GET')
    
    def logout(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
        exp = payload['exp'] 
        
        LogoutHelper.logout(client_id, user_id, token, exp)
        
        return LogoutResponse(message="Logged out")
    
        
@egb_api.api_class(resource_name='Password')
class ChangePasswordApi(remote.Service, UserHelper, PasswordReset):
    @endpoints.method(PasswordReset.CHANGE_PASSWORD_CONTAINER, 
                      ChangePasswordResponse,
                      name='change',
                      path='password/change',
                      http_method='POST')
    
    def change_password(self, request):

        tokenvar = request.token
        password = request.password
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(tokenvar, ip_address)
            
        client_id  = payload['client_id']    
        user_id  = payload['user_id']     
        
        users = self.get_user(client_id, user_id)[0]     
        
        users.password = password 
        users.hash = Token.generate_token()     
        users.put()  
        
        return ChangePasswordResponse(message="password changed")


@egb_api.api_class(resource_name='Password')
class ResetPasswordApi(remote.Service, PasswordReset):
    @endpoints.method(PasswordReset.RESET_CONTAINER, 
                      ResetPasswordResponse,
                      name='reset',
                      path='password/reset',
                      http_method='POST')
    
    def reset_password(self, request):
        
        email = request.email
        
        qryUser = UserModel.query(UserModel.email == email).get()
        
        if qryUser:
            
            client_id = qryUser.key.id()
            user_id = qryUser.user_id
            hashed = qryUser.hash
            token = str(client_id)+'-'+str(user_id)+'-'+str(hashed)

            return self.reset_password_encode(token)
        
        raise ErrorHelper.email_not_found() 
        
        
@egb_api.api_class(resource_name='Password')
class ResetPasswordChangeApi(remote.Service, PasswordReset):
    @endpoints.method(PasswordReset.RESET_PASSWORD_CONTAINER, 
                      ResetPasswordResponse,
                      name='reset.update',
                      path='password/reset/update',
                      http_method='POST')
    
    def reset_password(self, request):
        
        tokenVar = request.token
        password = request.password
        
        payload = JwtHelper().decode_reset_jwt(tokenVar)
        
        if payload: 
            payload.password = password
            payload.hash = Token.generate_token()
            payload.access_token = Token.generate_token()
            payload.put()
            return ResetPasswordResponse(message="Password Changed")
        else:
            raise ErrorHelper.reset_unauthorised()
        


@egb_api.api_class(resource_name='Notification')
class NotificationApi(remote.Service, NotificationHelper):
    @endpoints.method(NotificationHelper.NOTIFICATION_CONTAINER, 
                      NotificationResponse,
                      name='registrationId',
                      path='notification/registrationId',
                      http_method='POST')
    
    def registration_id(self, request):
        
        token = request.token
        
        registration_id = request.registration_id
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id = payload['client_id']
        user_id = payload['user_id']
            
        return self.insert_registration_id(client_id, user_id, registration_id)
            

@egb_api.api_class(resource_name='Notification')
class NotificationListApi(remote.Service, NotificationHelper):
    @endpoints.method(NotificationHelper.NOTIFICATION_LIST_CONTAINER, 
                      NotificationList,
                      name='registrationId.list',
                      path='notification/registrationId/list',
                      http_method='GET')
    
    def registration_id_list(self, request):
        
        token = request.token
        
        user_id = request.user_id
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        JwtHelper().decode_notification_auth_jwt(token, ip_address)
        
        qryNotificationList = self.get_registration_id(user_id)
        
        if qryNotificationList:
            
            notification = self.construct_registration_id(qryNotificationList)
            
            return notification
        
        else:
            
            raise ErrorHelper.notification_not_found()
            
        

@egb_api.api_class(resource_name='Masquerade')
class MasqueradeTokenApi(remote.Service, MaqueradeHelper):
    @endpoints.method(MaqueradeHelper.MASQUERADE_CONTAINER, 
                      Masquerade,
                      name='token',
                      path='masquerade/token',
                      http_method='GET') 
    
    def masquerade_token(self, request):
        
        token = request.token
        user_id_as = request.user_id_as
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_masquerade_auth_jwt(token, ip_address)
        
        if payload:
            
            maquerade = self.get_maquerade_list(user_id_as)
            
            if maquerade:
                
                maquerade = self.construct_masquerade_token(maquerade, ip_address)

                return maquerade

            else:
                
                raise ErrorHelper.maquerade_not_found()
            
        else:
            
            raise ErrorHelper.token_unuthorised()
        

@egb_api.api_class(resource_name='Masquerade')
class MasqueradeUserApi(remote.Service, MaqueradeHelper):
    @endpoints.method(MaqueradeHelper.MASQUERADE_CONTAINER, 
                      MasqueradeResponse,
                      name='user',
                      path='masquerade/user',
                      http_method='POST') 
    
    def masquerade_user(self, request):
        
        token = request.token
        
        user_id_as = request.user_id_as
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_masquerade_auth_jwt(token, ip_address)
        
        if payload:
            
            client_id = payload['client_id']
            user_id = payload['user_id']
            masquerade = self.construct_masquerade(client_id, user_id, user_id_as)
            
            if masquerade:
                
                return MasqueradeResponse(message="Successfully masquerade")
            
        else:
            
            raise ErrorHelper.token_unuthorised()
            
      
        
@egb_api.api_class(resource_name='user')
class UserApi(remote.Service, UserHelper): 
    @endpoints.method(UserHelper.USER_CONTAINER, 
                      UserList,
                      name='get',
                      path='user/get',
                      http_method='GET')
    
    def users(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id']    
        user_id  = payload['user_id']     
            
        users = self.get_user(client_id, user_id)     
            
        return self.construct_user(users)           
    
        
@egb_api.api_class(resource_name='pension')
class PensionApi(remote.Service, PensionHelper): 
        
    @endpoints.method(PensionHelper.PENSION_CONTAINER, 
                      PensionList,
                      name='get',
                      path='pension/get',
                      http_method='GET')
    
    def pension(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id']    
        user_id  = payload['user_id']   
            
        pensions = self.get_pension(client_id, user_id)
        
        return self.construct_pension(pensions)      
                
        
    
@egb_api.api_class(resource_name='pension')
class PensionSignupApi(remote.Service, PensionHelper): 
        
    @endpoints.method(PensionHelper.PENSION_SIGNUP_CONTAINER, 
                      PensionSignupResponse,
                      name='signup',
                      path='pension/signup',
                      http_method='POST')
    
    def pension_signup(self, request):
        
        token = request.token
        employee_contribution = request.contribution
        employee_contribution_percent = request.employee_contribution_percent
        employer_contribution = request.employer_contribution
        employer_contribution_percent = request.employer_contribution_percent
        tax_saving = request.tax_saving
        retirement_age = request.retirement_age
        list_fund = request.list_fund
        fund_selection = request.fund_selection
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)

        client_id  = payload['client_id']    
        user_id  = payload['user_id']
        
        return self.pension_signup_insert(user_id, client_id, employee_contribution, employee_contribution_percent, employer_contribution, employer_contribution_percent, tax_saving, retirement_age, list_fund, fund_selection)
        

        

@egb_api.api_class(resource_name='pension')
class PensionSignupListApi(remote.Service, PensionHelper): 
        
    @endpoints.method(PensionHelper.PENSION_SIGNUP_LIST_CONTAINER, 
                      PensionSignupList,
                      name='signup.list',
                      path='pension/signup/list',
                      http_method='GET')
    def pension_signup_list(self, request):
        
        token = request.token
        pension_signup_status = request.pension_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id']
        user_id  = payload['user_id']       
        
        pension_signup_list_get = self.pension_signup_list_get(user_id, client_id, pension_signup_status)
        
        return self.construct_pension_list(pension_signup_list_get)

        

@egb_api.api_class(resource_name='pension')
class PensionSignupListAuthApi(remote.Service, PensionHelper): 
  
    @endpoints.method(PensionHelper.PENSION_SIGNUP_LIST_AUTH_CONTAINER, 
                      PensionSignupList,
                      name='signup.list.auth',
                      path='pension/signup/list/auth',
                      http_method='GET')
    
    def pension_signup_list_auth(self, request):
        
        token = request.token
        user_status = request.user_status
        pension_signup_status = request.pension_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        JwtHelper().decode_jwt_admin(token, ip_address)
            
        pension_signup_list_auth = self.pension_signup_list_auth_get(user_status, pension_signup_status)
                
        return self.construct_pension_list(pension_signup_list_auth)
        

@egb_api.api_class(resource_name='pension')
class PensionSignupAmendApi(remote.Service, PensionHelper): 
        
    @endpoints.method(PensionHelper.PENSION_SIGNUP_AMEND_CONTAINER, 
                      PensionSignupResponse,
                      name='signup.amend',
                      path='pension/signup/amend',
                      http_method='POST')
    
    def pension_signup_amend(self, request):
        
        token = request.token
        employee_contribution = request.contribution
        employee_contribution_percent = request.employee_contribution_percent
        employer_contribution = request.employer_contribution
        employer_contribution_percent = request.employer_contribution_percent
        tax_saving = request.tax_saving
        fund_selection = request.fund_selection

        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']  
        user_id  = payload['user_id']       
            
        return self.pension_signup_amend_update(client_id, user_id, employee_contribution, employee_contribution_percent, employer_contribution, employer_contribution_percent, tax_saving, fund_selection)


@egb_api.api_class(resource_name='pension')
class PensionSignupApprovalApi(remote.Service, PensionHelper): 
        
    @endpoints.method(PensionHelper.PENSION_SIGNUP_APPROVAL_CONTAINER, 
                      PensionSignupResponse,
                      name='signup.approval',
                      path='pension/signup/approval',
                      http_method='POST')
    
    def pension_signup_approval(self, request):
        
        token = request.token
        pension_signup_key = request.pension_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)

        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
            
        return self.pension_signup_approval_update(client_id, user_id, pension_signup_key, hashed, status)
                

@egb_api.api_class(resource_name='pension')
class PensionSignupCancelApi(remote.Service, PensionHelper): 
        
    @endpoints.method(PensionHelper.PENSION_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      PensionSignupResponse,
                      name='signup.cancel',
                      path='pension/signup/cancel',
                      http_method='POST')
    
    def pension_signup_cancel(self, request):
        
        token = request.token
        pension_signup_key = request.pension_signup_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
          
        user_id  = payload['user_id']       
        
        return self.pension_signup_cancel_update(user_id, pension_signup_key, hashed)
        

@egb_api.api_class(resource_name='pension')
class PensionSignupWithdrawApi(remote.Service, PensionHelper): 
        
    @endpoints.method(PensionHelper.PENSION_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      PensionSignupResponse,
                      name='signup.withdraw',
                      path='pension/signup/withdraw',
                      http_method='POST')
    
    def get_pension_signup_withdraw_api(self, request):
        
        token = request.token
        pension_signup_key = request.pension_signup_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
        
        if payload:

            client_id  = payload['client_id']    
            user_id  = payload['user_id']       
            
            pension_signup_withdraw = self.pension_signup_withdraw_update(user_id, pension_signup_key, hashed)
                
            return pension_signup_withdraw
            
        else:
            
            raise ErrorHelper.token_unuthorised()
                
                
            
@egb_api.api_class(resource_name='employee')
class EmployeeApi(remote.Service, EmployeeTypeHelper):
        
    @endpoints.method(EmployeeTypeHelper.EMPLOYEE_CONTAINER, 
                      EmployeeList,
                      name='get',
                      path='employee/get',
                      http_method='GET')
    
    def employee(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']   
        
        employees = self.get_employee(client_id, user_id)
             
        return self.construct_employee(employees)  
                

@egb_api.api_class(resource_name='employer')
class EmployerApi(remote.Service, EmployerHelper): 
        
    @endpoints.method(EmployerHelper.EMPLOYER_CONTAINER, 
                      EmployerList,
                      name='get',
                      path='employer/get',
                      http_method='GET')
    
    def employer(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id']  
        user_id  = payload['user_id']     
    
        employers = self.get_employer(client_id, user_id)
                                  
        return self.construct_employer(employers)        
    

@egb_api.api_class(resource_name='provider')
class ProviderApi(remote.Service, ProviderHelper): 
    @endpoints.method(ProviderHelper.PROVIDER_CONTAINER, 
                      ProviderList,
                      name='get',
                      path='provider/get',
                      http_method='GET')
    
    def provider(self, request):

        providers = self.get_provider(request.provider_name, request.product_type, request.product_variation)          
            
        return self.construct_provider(providers)        
    
    
@egb_api.api_class(resource_name='life')
class LifeApi(remote.Service, LifeHelper): 
        
    @endpoints.method(LifeHelper.LIFE_CONTAINER, 
                      LifeList,
                      name='get',
                      path='life/get',
                      http_method='GET')
    
    def life_cover(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id']     
                    
        lifes = self.get_life(client_id)
        
        return self.construct_life(lifes)        
        

@egb_api.api_class(resource_name='life')
class LifeSignupApi(remote.Service, LifeHelper): 
        
    @endpoints.method(LifeHelper.LIFE_SIGNUP_CONTAINER, 
                      LifeSignupResponse,
                      name='signup',
                      path='life/signup',
                      http_method='POST')
    
    def life_signup(self, request):
        
        token = request.token
        multiple = request.multiple
        gross_cost = request.gross_cost
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']  
        user_id  = payload['user_id']   
            
        return self.life_signup_insert(user_id, client_id, multiple, gross_cost)



@egb_api.api_class(resource_name='life')
class LifeSignupAmendApi(remote.Service, LifeHelper): 
    
    @endpoints.method(LifeHelper.LIFE_SIGNUP_AMEND_CONTAINER, 
                      LifeSignupResponse,
                      name='signup.amend',
                      path='life/signup/amend',
                      http_method='POST')
    
    def life_signup_amend(self, request):
        
        token = request.token
        life_signup_key = request.life_signup_key
        selected_multiple = request.selected_multiple
        gross_cost = request.gross_cost
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']   
                
        return self.life_signup_amend_update(user_id, life_signup_key, selected_multiple, gross_cost, hashed)             
        

@egb_api.api_class(resource_name='life')
class LifeSignupApprovalApi(remote.Service, LifeHelper): 
    
    @endpoints.method(LifeHelper.LIFE_SIGNUP_APPROVAL_CONTAINER, 
                      LifeSignupResponse,
                      name='signup.approval',
                      path='life/signup/approval',
                      http_method='POST')
    
    def life_signup_approval(self, request):
        
        token = request.token
        life_signup_key = request.life_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
            
        return self.life_signup_approval_update(client_id, user_id, life_signup_key, hashed, status)
            
        

@egb_api.api_class(resource_name='life')
class LifeSignupListApi(remote.Service, LifeHelper): 
        
    @endpoints.method(LifeHelper.LIFE_SIGNUP_LIST_CONTAINER, 
                      LifeSignupList,
                      name='signup.list',
                      path='life/signup/list',
                      http_method='GET')
    def life_signup_list(self, request):
        
        token = request.token
        life_signup_status = request.life_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']  
        user_id  = payload['user_id']   
                
        life_signup_list = self.life_signup_list_get(user_id, client_id, life_signup_status)             
                
        return self.construct_life_signup_list(life_signup_list)

        

@egb_api.api_class(resource_name='life')
class LifeSignupListAuthApi(remote.Service, LifeHelper): 
        
    @endpoints.method(LifeHelper.LIFE_SIGNUP_LIST_AUTH_CONTAINER, 
                      LifeSignupList,
                      name='signup.list.auth',
                      path='life/signup/list/auth',
                      http_method='GET')
    
    def life_signup_list_auth(self, request):
        
        token = request.token
        user_status = request.user_status
        life_signup_status = request.life_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        JwtHelper().decode_jwt_admin(token, ip_address)
           
        life_signup_list_auth = self.life_signup_list_auth_get(user_status, life_signup_status)             
            
        return self.construct_life_signup_list(life_signup_list_auth)
                

@egb_api.api_class(resource_name='life')
class LifeSignupCancelApi(remote.Service, LifeHelper): 
        
    @endpoints.method(LifeHelper.LIFE_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      LifeSignupResponse,
                      name='signup.cancel',
                      path='life/signup/cancel',
                      http_method='POST')
    
    def life_signup_cancel(self, request):
        
        token = request.token
        life_signup_key = request.life_signup_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)

        user_id  = payload['user_id']   

        return self.life_signup_cancel_update(user_id, life_signup_key, hashed)
        

@egb_api.api_class(resource_name='life')
class LifeSignupWithdrawApi(remote.Service, LifeHelper): 
        
    @endpoints.method(LifeHelper.LIFE_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      LifeSignupResponse,
                      name='signup.withdraw',
                      path='life/signup/withdraw',
                      http_method='POST')
    
    def life_signup_withdraw(self, request):
        
        token = request.token
        life_signup_key = request.life_signup_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        user_id  = payload['user_id']   
                                      
        return self.life_signup_withdraw_update(user_id, life_signup_key, hashed)             
        
    
@egb_api.api_class(resource_name='cic')
class CicApi(remote.Service, CicHelper): 
         
    @endpoints.method(CicHelper.CIC_CONTAINER, 
                      CicList,
                      name='get',
                      path='cic/get',
                      http_method='GET')
    
    def cic(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)

        client_id  = payload['client_id']  
        user_id  = payload['user_id']      
            
        cics = self.get_cic(client_id, user_id)
                                       
        return self.construct_cic(cics)
    

@egb_api.api_class(resource_name='cic')
class CicSignupApi(remote.Service, CicHelper): 
        
    @endpoints.method(CicHelper.CIC_SIGNUP_CONTAINER, 
                      CicSignupResponse,
                      name='signup',
                      path='cic/signup',
                      http_method='POST')
    
    def cic_signup(self, request):
        
        token = request.token
        window_salary = request.window_salary
        gross_cost = request.gross_cost
        multiple = request.multiple
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']  
        user_id  = payload['user_id']   
            
        return self.cic_signup_insert(user_id, client_id, window_salary, multiple, gross_cost)



@egb_api.api_class(resource_name='cic')
class CicSignupAmendApi(remote.Service, CicHelper): 
    
    @endpoints.method(CicHelper.CIC_SIGNUP_AMEND_CONTAINER, 
                      CicSignupResponse,
                      name='signup.amend',
                      path='cic/signup/amend',
                      http_method='POST')
    
    def cic_signup_amend(self, request):
        
        token = request.token
        cic_signup_key = request.cic_signup_key
        unit = request.unit
        gross_cost = request.gross_cost
        cover_cost = request.cover_cost
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']   
                
        return self.cic_signup_amend_update(user_id, cic_signup_key, unit, gross_cost, cover_cost, hashed)             
        

@egb_api.api_class(resource_name='cic')
class CicSignupApprovalApi(remote.Service, CicHelper): 
    
    @endpoints.method(CicHelper.CIC_SIGNUP_APPROVAL_CONTAINER, 
                      CicSignupResponse,
                      name='signup.approval',
                      path='cic/signup/approval',
                      http_method='POST')
    
    def cic_signup_approval(self, request):
        
        token = request.token
        cic_signup_key = request.cic_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
            
        return self.cic_signup_approval_update(client_id, user_id, cic_signup_key, hashed, status)
            
        

@egb_api.api_class(resource_name='cic')
class CicSignupListApi(remote.Service, CicHelper): 
        
    @endpoints.method(CicHelper.CIC_SIGNUP_LIST_CONTAINER, 
                      CicSignupList,
                      name='signup.list',
                      path='cic/signup/list',
                      http_method='GET')
    def cic_signup_list(self, request):
        
        token = request.token
        cic_signup_status = request.cic_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']  
        user_id  = payload['user_id']   
                
        cic_signup_list = self.cic_signup_list_get(user_id, client_id, cic_signup_status)           
         
        return self.construct_cic_signup_list(cic_signup_list)

        

@egb_api.api_class(resource_name='cic')
class CicSignupListAuthApi(remote.Service, CicHelper): 
        
    @endpoints.method(CicHelper.CIC_SIGNUP_LIST_AUTH_CONTAINER, 
                      CicSignupList,
                      name='signup.list.auth',
                      path='cic/signup/list/auth',
                      http_method='GET')
    
    def cic_signup_list_auth(self, request):
        
        token = request.token
        user_status = request.user_status
        cic_signup_status = request.cic_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        JwtHelper().decode_jwt_admin(token, ip_address)
           
        cic_signup_list_auth = self.cic_signup_list_auth_get(user_status, cic_signup_status)             
            
        return self.construct_cic_signup_list(cic_signup_list_auth)
                

@egb_api.api_class(resource_name='cic')
class CicSignupCancelApi(remote.Service, CicHelper): 
        
    @endpoints.method(CicHelper.CIC_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      CicSignupResponse,
                      name='signup.cancel',
                      path='cic/cancel',
                      http_method='POST')
    
    def cic_signup_cancel(self, request):
        
        token = request.token
        cic_signup_key = request.cic_signup_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)

        user_id  = payload['user_id']   

        return self.cic_signup_cancel_update(user_id, cic_signup_key, hashed)
        

@egb_api.api_class(resource_name='cic')
class CicSignupWithdrawApi(remote.Service, CicHelper): 
        
    @endpoints.method(CicHelper.CIC_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      CicSignupResponse,
                      name='signup.withdraw',
                      path='cic/signup/withdraw',
                      http_method='POST')
    
    def cic_signup_withdraw(self, request):
        
        token = request.token
        cic_signup_key = request.cic_signup_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        user_id  = payload['user_id']   
                                      
        return self.cic_signup_withdraw_update(user_id, cic_signup_key, hashed)              
    
               
@egb_api.api_class(resource_name='gip')
class GipApi(remote.Service, GipHelper): 
         
    @endpoints.method(GipHelper.GIP_CONTAINER, 
                      GipList,
                      name='get',
                      path='gip/get',
                      http_method='GET')
    
    def gip(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']      

        gips = self.get_gip(client_id, user_id)
                                       
        return self.construct_gip(gips)
    
    

@egb_api.api_class(resource_name='gip')
class GipSignupApi(remote.Service, GipHelper): 
        
    @endpoints.method(GipHelper.GIP_SIGNUP_CONTAINER, 
                      GipSignupResponse,
                      name='signup',
                      path='gip/signup',
                      http_method='POST')
    
    def gip_signup(self, request):
        
        token = request.token
        percentage = request.percentage
        deferred_period = request.deferred_period
        payment_term = request.payment_term
        gross_cost = request.gross_cost
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']  
        user_id  = payload['user_id']   
            
        return self.gip_signup_insert(user_id, client_id, percentage, deferred_period, payment_term, gross_cost)



@egb_api.api_class(resource_name='gip')
class GipSignupAmendApi(remote.Service, GipHelper): 
    
    @endpoints.method(GipHelper.GIP_SIGNUP_AMEND_CONTAINER, 
                      GipSignupResponse,
                      name='signup.amend',
                      path='gip/signup/amend',
                      http_method='POST')
    
    def gip_signup_amend(self, request):
        
        token = request.token
        gip_signup_key = request.gip_signup_key
        earnings = request.earnings
        deferred = request.deferred
        payment_term = request.payment_term
        gross_cost = request.gross_cost
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']   
                
        return self.gip_signup_amend_update(user_id, gip_signup_key, earnings, deferred, payment_term, gross_cost, hashed)             
        

@egb_api.api_class(resource_name='gip')
class GipSignupApprovalApi(remote.Service, GipHelper): 
    
    @endpoints.method(GipHelper.GIP_SIGNUP_APPROVAL_CONTAINER, 
                      GipSignupResponse,
                      name='signup.approval',
                      path='gip/signup/approval',
                      http_method='POST')
    
    def gip_signup_approval(self, request):
        
        token = request.token
        gip_signup_key = request.gip_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
            
        return self.gip_signup_approval_update(client_id, user_id, gip_signup_key, hashed, status)
            
        

@egb_api.api_class(resource_name='gip')
class GipSignupListApi(remote.Service, GipHelper): 
        
    @endpoints.method(GipHelper.GIP_SIGNUP_LIST_CONTAINER, 
                      GipSignupList,
                      name='signup.list',
                      path='gip/signup/list',
                      http_method='GET')
    def gip_signup_list(self, request):
        
        token = request.token
        gip_signup_status = request.gip_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']  
        user_id  = payload['user_id']   
                
        gip_signup_list = self.gip_signup_list_get(client_id, user_id, gip_signup_status)             
                
        return self.construct_gip_signup_list(gip_signup_list)

        

@egb_api.api_class(resource_name='gip')
class GipSignupListAuthApi(remote.Service, GipHelper): 
        
    @endpoints.method(GipHelper.GIP_SIGNUP_LIST_AUTH_CONTAINER, 
                      GipSignupList,
                      name='signup.list.auth',
                      path='gip/signup/list/auth',
                      http_method='GET')
    
    def gip_signup_list_auth(self, request):
        
        token = request.token
        user_status = request.user_status
        gip_signup_status = request.gip_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        JwtHelper().decode_jwt_admin(token, ip_address)
           
        gip_signup_list_auth = self.gip_signup_list_auth_get(user_status, gip_signup_status)             
            
        return self.construct_gip_signup_list(gip_signup_list_auth)
                

@egb_api.api_class(resource_name='gip')
class GIPSignupCancelApi(remote.Service, GipHelper): 
        
    @endpoints.method(GipHelper.GIP_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      GipSignupResponse,
                      name='signup.cancel',
                      path='gip/signup/cancel',
                      http_method='POST')
    
    def gip_signup_cancel(self, request):
        
        token = request.token
        gip_signup_key = request.gip_signup_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)

        user_id  = payload['user_id']   

        return self.gip_signup_cancel_update(user_id, gip_signup_key, hashed)
        

@egb_api.api_class(resource_name='gip')
class GipSignupWithdrawApi(remote.Service, GipHelper): 
        
    @endpoints.method(GipHelper.GIP_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      GipSignupResponse,
                      name='signup.withdraw',
                      path='gip/signup/withdraw',
                      http_method='POST')
    
    def gip_signup_withdraw(self, request):
        
        token = request.token
        gip_signup_key = request.gip_signup_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        user_id  = payload['user_id']   
                                      
        return self.gip_signup_withdraw_update(user_id, gip_signup_key, hashed)               

        
     
@egb_api.api_class(resource_name='pmi')
class PmiApi(remote.Service, PmiHelper): 
         
    @endpoints.method(PmiHelper.PMI_CONTAINER, 
                      PMIList,
                      name='get',
                      path='pmi/get',
                      http_method='GET')
    
    def pmi(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']     
                     
        pmis = self.get_pmi(client_id, user_id)

        return self.construct_pmi(pmis)
        

@egb_api.api_class(resource_name='pmi')
class PmiSignupApi(remote.Service, PmiHelper): 
         
    @endpoints.method(PmiHelper.PMI_SIGNUP_CONTAINER, 
                      PMISignupResponse,
                      name='signup',
                      path='pmi/signup',
                      http_method='POST')
    
    def pmi_signup(self, request):
        
        token = request.token
        excess = request.excess
        who = request.who
        gross_cost = request.gross_cost
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)

        client_id  = payload['client_id'] 
        user_id  = payload['user_id']         
                 
        return self.pmi_signup_insert(user_id, client_id, who, excess, gross_cost)     


@egb_api.api_class(resource_name='pmi')
class PmiSignupApprovalApi(remote.Service, PmiHelper): 
        
    @endpoints.method(PmiHelper.PMI_SIGNUP_APPROVAL_CONTAINER, 
                      PMISignupResponse,
                      name='signup.approval',
                      path='pmi/signup/approval',
                      http_method='POST')
    
    def pmi_signup_approval(self, request):
        
        token = request.token
        pmi_signup_key = request.pmi_signup_key
        hashed = request.hashed
        status = request.status

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
            
        return self.pmi_signup_approval_update(client_id, user_id, pmi_signup_key, hashed, status)
        

@egb_api.api_class(resource_name='pmi')
class PmiSignupAmendApi(remote.Service, PmiHelper): 
    
    @endpoints.method(PmiHelper.PMI_SIGNUP_AMEND_CONTAINER, 
                      PMISignupResponse,
                      name='signup.amend',
                      path='pmi/signup/amend',
                      http_method='POST')
    
    def pmi_signup_amend(self, request):
        
        token = request.token
        pmi_signup_key = request.pmi_signup_key
        who = request.who
        cover_level = request.cover_level
        gross_cost = request.gross_cost
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']   
                
        return self.pmi_signup_amend_update(user_id, pmi_signup_key, who, cover_level, gross_cost, hashed)
    

@egb_api.api_class(resource_name='pmi')
class PmiSignupCancelApi(remote.Service, PmiHelper): 
         
    @endpoints.method(PmiHelper.PMI_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      PMISignupResponse,
                      name='signup.cancel',
                      path='pmi/signup/cancel',
                      http_method='POST')
    
    def pmi_signup_cancel(self, request):
        
        token = request.token
        pmi_signup_key = request.pmi_signup_key
        hashed = request.hashed

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']
            
        return self.pmi_signup_cancel_update(user_id, pmi_signup_key, hashed)

        

@egb_api.api_class(resource_name='pmi')
class PmiSignupWithdrawApi(remote.Service, PmiHelper): 
         
    @endpoints.method(PmiHelper.PMI_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      PMISignupResponse,
                      name='signup.withdraw',
                      path='pmi/signup/withdraw',
                      http_method='POST')
    
    def pmi_signup_withdraw(self, request):
        
        token = request.token
        pmi_signup_key = request.pmi_signup_key
        hashed = request.hashed

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']
            
        return self.pmi_signup_withdraw_update(user_id, pmi_signup_key, hashed)
    
        
@egb_api.api_class(resource_name='pmi')
class PmiSignupListApi(remote.Service, PmiHelper): 
         
    @endpoints.method(PmiHelper.PMI_SIGNUP_LIST_CONTAINER, 
                      PMISignupList,
                      name='signup.list',
                      path='pmi/signup/list',
                      http_method='GET')
    
    def pmi_signup_list(self, request):
        
        token = request.token
        pmi_signup_status = request.pmi_signup_status

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
        
        if payload:
            
            client_id  = payload['client_id'] 
            user_id  = payload['user_id']

            pmi_signup_list = self.pmi_signup_list_get(user_id, client_id, pmi_signup_status)
            
            return self.construct_pmi_signup_list(pmi_signup_list)
        

@egb_api.api_class(resource_name='pmi')
class PmiSignupListAuthApi(remote.Service, PmiHelper): 
         
    @endpoints.method(PmiHelper.PMI_SIGNUP_LIST_AUTH_CONTAINER, 
                      PMISignupList,
                      name='signup.list.auth',
                      path='pmi/signup/list/auth',
                      http_method='GET')
    
    def pmi_signup_list_auth(self, request):
        
        token = request.token
        user_status = request.user_status
        pmi_signup_status = request.pmi_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        JwtHelper().decode_jwt_admin(token, ip_address)

        pmi_signup_list_auth = self.pmi_signup_list_auth_get(user_status, pmi_signup_status)
        
        return self.construct_pmi_signup_list(pmi_signup_list_auth)

      
@egb_api.api_class(resource_name='cashplan')
class CashplanApi(remote.Service, CashplanHelper): 
         
    @endpoints.method(CashplanHelper.CASHPLAN_CONTAINER, 
                      CashplanList,
                      name='get',
                      path='cashplan/get',
                      http_method='GET')
    
    def cashplan(self, request):

        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        if payload:
            
            client_id  = payload['client_id'] 
            user_id  = payload['user_id'] 
                     
            cps = self.get_cashplan(client_id, user_id)
                                       
            return self.construct_cash_plan(cps)
        

@egb_api.api_class(resource_name='cashplan')
class CashplanSignupApi(remote.Service, CashplanHelper): 
         
    @endpoints.method(CashplanHelper.CASHPLAN_SIGNUP_CONTAINER, 
                      CashplanSignupResponse,
                      name='signup',
                      path='cashplan/signup',
                      http_method='POST')
    
    def cashplan_signup(self, request):
        
        token = request.token
        who = request.who
        cover_level = request.cover_level
        gross_cost = request.gross_cost
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']
                                       
        return self.cashplan_signup_insert(user_id, client_id, who, cover_level, gross_cost)
        


@egb_api.api_class(resource_name='cashplan')
class CashplanSignupApprovalApi(remote.Service, CashplanHelper): 
        
    @endpoints.method(CashplanHelper.CASHPLAN_SIGNUP_APPROVAL_CONTAINER, 
                      CashplanSignupResponse,
                      name='signup.approval',
                      path='cashplan/signup/approval',
                      http_method='POST')
    
    def cashplan_signup_approval(self, request):
        
        token = request.token
        cashplan_signup_key = request.cashplan_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
        
        return self.cashplan_signup_approval_update(client_id, user_id, cashplan_signup_key, hashed, status)
            
            

@egb_api.api_class(resource_name='cashplan')
class CashplanSignupAmendApi(remote.Service, CashplanHelper): 
    
    @endpoints.method(CashplanHelper.CASHPLAN_SIGNUP_AMEND_CONTAINER, 
                      CashplanSignupResponse,
                      name='signup.amend',
                      path='cashplan/signup/amend',
                      http_method='POST')
    
    def cashplan_signup_amend(self, request):
        
        token = request.token
        cashplan_signup_key = request.cashplan_signup_key
        who = request.who
        cover_level = request.cover_level
        gross_cost = request.gross_cost
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']   
            
        return self.cashplan_signup_amend_update(user_id, cashplan_signup_key, who, cover_level, gross_cost, hashed)
        

@egb_api.api_class(resource_name='cashplan')
class CashplanSignupCancelApi(remote.Service, CashplanHelper): 
         
    @endpoints.method(CashplanHelper.CASHPLAN_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      CashplanSignupResponse,
                      name='signup.cancel',
                      path='cashplan/signup/cancel',
                      http_method='POST')
    
    def cashplan_signup_cancel(self, request):
        
        token = request.token
        cashplan_signup_key = request.cashplan_signup_key
        hashed = request.hashed

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']
        
        return self.cashplan_signup_cancel_update(user_id, cashplan_signup_key, hashed)
    

@egb_api.api_class(resource_name='cashplan')
class CashplanSignupWithdrawApi(remote.Service, CashplanHelper): 
         
    @endpoints.method(CashplanHelper.CASHPLAN_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      CashplanSignupResponse,
                      name='signup.withdraw',
                      path='cashplan/signup/withdraw',
                      http_method='POST')
    
    def cashplan_signup_withdraw(self, request):
        
        token = request.token
        cashplan_signup_key = request.cashplan_signup_key
        hashed = request.hashed

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']
        
        return self.cashplan_signup_withdraw_update(user_id, cashplan_signup_key, hashed)    
    
        
@egb_api.api_class(resource_name='cashplan')
class CashplanSignupListApi(remote.Service, CashplanHelper): 
         
    @endpoints.method(CashplanHelper.CASHPLAN_SIGNUP_LIST_CONTAINER, 
                      CashplanSignupList,
                      name='signup.list',
                      path='cashplan/signup/list',
                      http_method='GET')
    
    def cashplan_signup_list(self, request):
        
        token = request.token
        cashplan_signup_status = request.cashplan_signup_status

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']

        cashplan_signup_list = self.cashplan_signup_list_get(user_id, client_id, cashplan_signup_status)
            
        return self.construct_cashplan_signup_list(cashplan_signup_list)


@egb_api.api_class(resource_name='cashplan')
class CashplanSignupListAuthApi(remote.Service, CashplanHelper): 
         
    @endpoints.method(CashplanHelper.CASHPLAN_SIGNUP_LIST_AUTH_CONTAINER, 
                      CashplanSignupList,
                      name='signup.list.auth',
                      path='cashplan/signup/list/auth',
                      http_method='GET')
    
    def cashplan_signup_list_auth(self, request):
        
        token = request.token
        user_status = request.user_status
        cashplan_signup_status = request.cashplan_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        JwtHelper().decode_jwt_admin(token, ip_address)
        
        cashplan_signup_list_auth = self.cashplan_signup_list_auth_get(user_status, cashplan_signup_status)

        return self.construct_cashplan_signup_list(cashplan_signup_list_auth)


@egb_api.api_class(resource_name='dental')
class DentalApi(remote.Service, DentalHelper): 
         
    @endpoints.method(DentalHelper.DENTAL_CONTAINER, 
                      DentalList,
                      name='get',
                      path='dental/get',
                      http_method='GET')
    
    def dental(self, request):
         
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']     
                 
        dentals = self.get_dental(client_id, user_id)
                                       
        return self.construct_dental(dentals)
    

@egb_api.api_class(resource_name='dental')
class DentalSignupApi(remote.Service, DentalHelper): 
         
    @endpoints.method(DentalHelper.DENTAL_SIGNUP_CONTAINER, 
                      DentalSignupResponse,
                      name='signup',
                      path='dental/signup',
                      http_method='POST')
    
    def dental_signup(self, request):
         
        token = request.token
        who = request.who
        cover_level = request.cover_level
        gross_cost = request.gross_cost
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']     
                 
        return self.dental_signup_insert(client_id, user_id, who, cover_level, gross_cost)
    
@egb_api.api_class(resource_name='dental')
class DentalSignupApprovalApi(remote.Service, DentalHelper): 
        
    @endpoints.method(DentalHelper.DENTAL_SIGNUP_APPROVAL_CONTAINER, 
                      DentalSignupResponse,
                      name='signup.approval',
                      path='dental/signup/approval',
                      http_method='POST')
    
    def dental_signup_approval(self, request):
        
        token = request.token
        dental_signup_key = request.dental_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
        
        return self.dental_signup_approval_update(client_id, user_id, dental_signup_key, hashed, status)
    

@egb_api.api_class(resource_name='dental')
class DentalSignupAmendApi(remote.Service, DentalHelper): 
    
    @endpoints.method(DentalHelper.DENTAL_SIGNUP_AMEND_CONTAINER, 
                      DentalSignupResponse,
                      name='signup.amend',
                      path='dental/signup/amend',
                      http_method='POST')
    
    def dental_signup_amend(self, request):
        
        token = request.token
        dental_signup_key = request.dental_signup_key
        who = request.who
        cover_level = request.cover_level
        gross_cost = request.gross_cost
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']   
            
        return self.dental_signup_amend_update(user_id, dental_signup_key, who, cover_level, gross_cost, hashed)
    


@egb_api.api_class(resource_name='dental')
class DentalSignupCancelApi(remote.Service, DentalHelper): 
         
    @endpoints.method(DentalHelper.DENTAL_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      DentalSignupResponse,
                      name='signup.cancel',
                      path='dental/signup/cancel',
                      http_method='POST')
    
    def dental_signup_cancel(self, request):
        
        token = request.token
        dental_signup_key = request.dental_signup_key
        hashed = request.hashed

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']
        
        return self.dental_signup_cancel_update(user_id, dental_signup_key, hashed)
    

@egb_api.api_class(resource_name='dental')
class DentalSignupWithdrawApi(remote.Service, DentalHelper): 
         
    @endpoints.method(DentalHelper.DENTAL_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      DentalSignupResponse,
                      name='signup.withdraw',
                      path='dental/signup/withdraw',
                      http_method='POST')
    
    def dental_signup_withdraw(self, request):
        
        token = request.token
        dental_signup_key = request.dental_signup_key
        hashed = request.hashed

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']
        
        return self.dental_signup_withdraw_update(user_id, dental_signup_key, hashed)


@egb_api.api_class(resource_name='dental')
class DentalSignupListApi(remote.Service, DentalHelper): 
         
    @endpoints.method(DentalHelper.DENTAL_SIGNUP_LIST_CONTAINER, 
                      DentalSignupList,
                      name='signup.list',
                      path='dental/signup/list',
                      http_method='GET')
    
    def dental_signup_list(self, request):
        
        token = request.token
        dental_signup_status = request.dental_signup_status

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']

        dental_signup_list = self.dental_signup_list_get(user_id, client_id, dental_signup_status)
            
        return self.construct_dental_signup_list(dental_signup_list)
    

@egb_api.api_class(resource_name='dental')
class DentalSignupListAuthApi(remote.Service, DentalHelper): 
         
    @endpoints.method(DentalHelper.DENTAL_SIGNUP_LIST_AUTH_CONTAINER, 
                      DentalSignupList,
                      name='signup.list.auth',
                      path='dental/signup/list/auth',
                      http_method='GET')
    
    def dental_signup_list_auth(self, request):
        
        token = request.token
        user_status = request.user_status
        dental_signup_status = request.dental_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        JwtHelper().decode_jwt_admin(token, ip_address)
        
        dental_signup_list_auth = self.dental_signup_list_auth_get(user_status, dental_signup_status)

        return self.construct_dental_signup_list(dental_signup_list_auth)   
                                       
        
     
@egb_api.api_class(resource_name='health_assessment')
class HealthAssessmentApi(remote.Service, HealthAssessHelper): 
         
    @endpoints.method(HealthAssessHelper.HEALTHASSESS_CONTAINER, 
                      HealthAssessmentList,
                      name='get',
                      path='health_assessment/get',
                      http_method='GET')
    
    def health_assessment(self, request):

        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']     
                     
        health_assessments = self.get_health_assessment(client_id, user_id)
                                       
        return self.construct_health_assessment(health_assessments)       
    
               
@egb_api.api_class(resource_name='ccv')
class CcvApi(remote.Service, CCVHelper): 
         
    @endpoints.method(CCVHelper.CCV_CONTAINER, 
                      CcvList,
                      name='get',
                      path='ccv/get',
                      http_method='GET')
    
    def ccv(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)

        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
                     
        ccvs = self.get_ccv(client_id, user_id)
                                       
        return self.construct_ccv(ccvs)
    

@egb_api.api_class(resource_name='ccv')
class CcvSignupApi(remote.Service, CCVHelper): 
         
    @endpoints.method(CCVHelper.CCV_CONTAINER_SIGNUP, 
                      CcvSignupResponse,
                      name='signup',
                      path='ccv/signup',
                      http_method='POST')
    
    def ccv_signup(self, request):
        
        token = request.token
        contribution = request.contribution
        comment = request.comment
        """
        firstname = request.firstname
        lastname = request.lastname
        dob = request.dob
        address = request.address
        city = request.city
        postcode = request.postcode
        contact_no = request.contact_no
        """
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)

        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
                                       
        return self.ccv_signup_insert(client_id, user_id, contribution, comment) 
    

@egb_api.api_class(resource_name='ccv')
class CcvSignupApprovalApi(remote.Service, CCVHelper): 
         
    @endpoints.method(CCVHelper.CCV_CONTAINER_SIGNUP_APPROVAL_CONTAINER, 
                      CcvSignupResponse,
                      name='signup.approval',
                      path='ccv/signup/approval',
                      http_method='POST')
    
    def ccv_signup_approval(self, request):
        
        token = request.token
        ccv_signup_key = request.ccv_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
        
        return self.ccv_signup_approval_update(client_id, user_id, ccv_signup_key, hashed, status)
    

@egb_api.api_class(resource_name='ccv')
class CcvSignupCancelApi(remote.Service, CCVHelper): 
         
    @endpoints.method(CCVHelper.CCV_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      CcvSignupResponse,
                      name='signup.cancel',
                      path='ccv/signup/cancel',
                      http_method='POST')
    
    def ccv_signup_cancel(self, request):
        
        token = request.token
        ccv_signup_key = request.ccv_signup_key
        hashed = request.hashed

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']
        
        return self.ccv_signup_cancel_update(user_id, ccv_signup_key, hashed)
    

@egb_api.api_class(resource_name='ccv')
class CcvSignupWithdrawApi(remote.Service, CCVHelper): 
         
    @endpoints.method(CCVHelper.CCV_SIGNUP_CANCEL_WITHDRAW_CONTAINER, 
                      CcvSignupResponse,
                      name='signup.withdraw',
                      path='ccv/signup/withdraw',
                      http_method='POST')
    
    def ccv_signup_withdraw(self, request):
        
        token = request.token
        ccv_signup_key = request.ccv_signup_key
        hashed = request.hashed

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id']
        
        return self.ccv_signup_withdraw_update(user_id, ccv_signup_key, hashed)   
    

@egb_api.api_class(resource_name='ccv')
class CcvSignupListApi(remote.Service, CCVHelper): 
         
    @endpoints.method(CCVHelper.CCV_SIGNUP_LIST_CONTAINER, 
                      CcvSignupList,
                      name='signup.list',
                      path='ccv/signup/list',
                      http_method='GET')
    
    def ccv_signup_list(self, request):
        
        token = request.token
        ccv_signup_status = request.ccv_signup_status

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']

        ccv_signup_list = self.ccv_signup_list_get(user_id, client_id, ccv_signup_status)
            
        return self.construct_ccv_signup_list(ccv_signup_list)


@egb_api.api_class(resource_name='ccv')
class CcvSignupListAuthApi(remote.Service, CCVHelper): 
         
    @endpoints.method(CCVHelper.CCV_SIGNUP_LIST_AUTH_CONTAINER, 
                      CcvSignupList,
                      name='signup.list.auth',
                      path='ccv/signup/list/auth',
                      http_method='GET')
    
    def ccv_signup_list_auth(self, request):
        
        token = request.token
        user_status = request.user_status
        ccv_signup_status = request.ccv_signup_status

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']

        ccv_signup_list = self.ccv_signup_list_auth_get(user_status, ccv_signup_status)
            
        return self.construct_ccv_signup_list(ccv_signup_list)    


@egb_api.api_class(resource_name='car')
class CarApi(remote.Service, CarHelper): 
         
    @endpoints.method(CarHelper.CAR_CONTAINER, 
                      CarList,
                      name='get',
                      path='car/get',
                      http_method='GET')
    
    def car(self, request):

        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']
            
        cars = self.get_car(client_id, user_id)
                                           
        return self.construct_car(cars)


@egb_api.api_class(resource_name='car')
class CarSignupListApi(remote.Service, CarHelper): 
         
    @endpoints.method(CarHelper.CAR_SIGNUP_LIST_CONTAINER, 
                      CarSignupList,
                      name='signup.list',
                      path='car/signup/list',
                      http_method='GET')
    
    def car_signup_list(self, request):

        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']
            
        car_signup_list = self.car_signup_list_get(client_id, user_id)
                                           
        return self.construct_car_signup_list(car_signup_list)


@egb_api.api_class(resource_name='car')
class CarSignupAuthListApi(remote.Service, CarHelper): 
         
    @endpoints.method(CarHelper.CAR_SIGNUP_LIST_AUTH_CONTAINER, 
                      CarSignupList,
                      name='signup.list.auth',
                      path='car/signup/list/auth',
                      http_method='GET')
    
    def car_signup_list_auth(self, request):

        token = request.token
        user_status = request.user_status
        car_signup_status = request.car_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        car_signup_list_auth = self.car_signup_list_auth_get(user_status, car_signup_status)
                                           
        return self.construct_car_signup_list(car_signup_list_auth)
    

@egb_api.api_class(resource_name='car')
class CarSignupApprovalApi(remote.Service, CarHelper): 
         
    @endpoints.method(CarHelper.CAR_SIGNUP_APPROVAL_CONTAINER, 
                      CarSignupResponse,
                      name='signup.approval',
                      path='car/signup/approval',
                      http_method='POST')
    
    def car_signup_approval(self, request):
        
        token = request.token
        car_signup_key = request.car_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
        
        return self.car_signup_approval_update(client_id, user_id, car_signup_key, hashed, status)     
    
    
@egb_api.api_class(resource_name='whitegood')
class WhiteGoodApi(remote.Service, WhitegoodHelper): 
         
    @endpoints.method(WhitegoodHelper.WHITEGOOD_CONTAINER, 
                      WhiteGoodList,
                      name='get',
                      path='whitegood/get',
                      http_method='GET')
    
    def white_good(self, request):

        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']
            
        whitegood_list = self.get_whitegood(client_id, user_id)
                                           
        return self.construct_whitegood(whitegood_list)


@egb_api.api_class(resource_name='whitegood')
class WhiteGoodSignupListApi(remote.Service, WhitegoodHelper): 
         
    @endpoints.method(WhitegoodHelper.WHITEGOOD_SIGNUP_LIST_CONTAINER, 
                      WhitegoodSignupList,
                      name='signup.list',
                      path='whitegood/signup/list',
                      http_method='GET')
    
    def whitegood_signup_list(self, request):

        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']
            
        whitegood_signup_list = self.whitegood_signup_list_get(client_id, user_id)
                                           
        return self.construct_whitegood_signup_list(whitegood_signup_list)


@egb_api.api_class(resource_name='whitegood')
class WhiteGoodSignupAuthListApi(remote.Service, WhitegoodHelper): 
         
    @endpoints.method(WhitegoodHelper.WHITEGOOD_SIGNUP_LIST_AUTH_CONTAINER, 
                      WhitegoodSignupList,
                      name='signup.list.auth',
                      path='whitegood/signup/list/auth',
                      http_method='GET')
    
    def white_good_signup_list_auth(self, request):

        token = request.token
        user_status = request.user_status
        whitegood_signup_status = request.whitegood_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        whitegood_signup_list_auth = self.whitegood_signup_list_auth_get(user_status, whitegood_signup_status)
                                           
        return self.construct_whitegood_signup_list(whitegood_signup_list_auth)
    

@egb_api.api_class(resource_name='whitegood')
class WhiteGoodSignupApprovalApi(remote.Service, WhitegoodHelper): 
         
    @endpoints.method(WhitegoodHelper.WHITEGOOD_SIGNUP_APPROVAL_CONTAINER, 
                      WhiteGoodSignupResponse,
                      name='signup.approval',
                      path='whitegood/signup/approval',
                      http_method='POST')
    
    def white_good_signup_approval(self, request):
        
        token = request.token
        white_good_signup_key = request.whitegood_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
        
        return self.white_good_signup_approval_update(client_id, user_id, white_good_signup_key, hashed, status)        


@egb_api.api_class(resource_name='ctw')
class CtwApi(remote.Service, CtwHelper): 
         
    @endpoints.method(CtwHelper.CTW_CONTAINER, 
                      CtwList,
                      name='get',
                      path='ctw/get',
                      http_method='GET')
    
    def ctw(self, request):

        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']
            
        ctws = self.get_ctw(client_id, user_id)
                                           
        return self.construct_ctw(ctws)


@egb_api.api_class(resource_name='ctw')
class CtwSignupListApi(remote.Service, CtwHelper): 
         
    @endpoints.method(CtwHelper.CTW_SIGNUP_LIST_CONTAINER, 
                      CtwSignupList,
                      name='signup.list',
                      path='ctw/signup/list',
                      http_method='GET')
    
    def ctw_signup_list(self, request):

        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']
            
        ctw_signup_list = self.ctw_signup_list_get(client_id, user_id)
                                           
        return self.construct_ctw_signup_list(ctw_signup_list)


@egb_api.api_class(resource_name='ctw')
class CtwSignupAuthListApi(remote.Service, CtwHelper): 
         
    @endpoints.method(CtwHelper.CTW_SIGNUP_LIST_AUTH_CONTAINER, 
                      CtwSignupList,
                      name='signup.list.auth',
                      path='ctw/signup/list/auth',
                      http_method='GET')
    
    def ctw_signup_list_auth(self, request):

        token = request.token
        user_status = request.user_status
        ctw_signup_status = request.ctw_signup_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        ctw_signup_list_auth = self.ctw_signup_list_auth_get(user_status, ctw_signup_status)
                                           
        return self.construct_ctw_signup_list(ctw_signup_list_auth)
    

@egb_api.api_class(resource_name='ctw')
class CtwSignupApprovalApi(remote.Service, CtwHelper): 
         
    @endpoints.method(CtwHelper.CTW_SIGNUP_APPROVAL_CONTAINER, 
                      CtwSignupResponse,
                      name='signup.approval',
                      path='ctw/signup/approval',
                      http_method='POST')
    
    def ctw_signup_approval(self, request):
        
        token = request.token
        ctw_signup_key = request.ctw_signup_key
        hashed = request.hashed
        status = request.status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt_admin(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']       
        
        return self.ctw_signup_approval_update(client_id, user_id, ctw_signup_key, hashed, status)     
           
     
@egb_api.api_class(resource_name='ess')
class EssApi(remote.Service, EssHelper): 
    @endpoints.method(EssHelper.ESS_CONTAINER, 
                      EssList,
                      name='get',
                      path='ess/get',
                      http_method='GET')
    def ess(self, request):
         
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)

        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
                     
        esss = self.get_ess(client_id, user_id)
                                       
        return self.construct_ess(esss)
    

@egb_api.api_class(resource_name='ess')
class EssAmendApi(remote.Service, EssHelper): 
    @endpoints.method(EssHelper.ESS_AMEND_CONTAINER, 
                      EssResponse,
                      name='amend',
                      path='ess/amend',
                      http_method='POST')
    def ess_ammend(self, request):

        token = request.token
        ni_no = request.ni_no
        title = request.title
        firstname = request.firstname
        lastname = request.lastname
        contact_no = request.contact_no
        email = request.email
        address = request.address
        city = request.city
        county = request.county
        postcode = request.postcode
        bank_name = request.bank_name
        bank_holder_name = request.bank_holder_name
        account_no = request.account_no
        sort_code = request.sort_code
        
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)

        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
                     
        return self.ess_ammend_update(client_id, user_id, ni_no, title, firstname, lastname, contact_no, email, address, city, county, postcode, bank_name, bank_holder_name, account_no, sort_code)          


@egb_api.api_class(resource_name='ess')
class EssUpdatedApi(remote.Service, EssHelper): 
    @endpoints.method(EssHelper.ESS_UPDATED_AUTH_CONTAINER, 
                      EssUpdatedList,
                      name='updated.auth',
                      path='ess/updated/auth',
                      http_method='GET')
    def ess_updated(self, request):
         
        token = request.token
        user_status = request.user_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt_admin(token, ip_address)

        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
                     
        ess_updated_list = self.get_ess_updated(user_status)
                                       
        return self.construct_ess_updated(ess_updated_list)        
  
@egb_api.api_class(resource_name='holiday')
class HolidayApi(remote.Service, HolidayHelper): 
    @endpoints.method(HolidayHelper.HOLIDAY_DETAIL_CONTAINER, 
                      HolidayDetailList,
                      name='get',
                      path='holiday/get',
                      http_method='GET')
    
    def holiday_detail(self, request):
        
        token = request.token
        year = request.year
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
    
        client_id  = payload['client_id'] 
                     
        holidays = self.get_holiday_detail(client_id, year)
                                                 
        return self.construct_holiday_detail(holidays)       
    
     
@egb_api.api_class(resource_name='holiday')
class HolidayListApi(remote.Service, HolidayHelper): 
    
    @endpoints.method(HolidayHelper.HOLIDAY_DETAIL_LIST_CONTAINER, 
                      HolidayDetailList,
                      name='list',
                      path='holiday/list',
                      http_method='GET')
    
    def holiday_detail_list(self, request):
        
        token = request.token
        status = request.status
        year = request.year

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        JwtHelper().decode_holiday_auth_jwt(token, ip_address)

        holidays = self.get_holiday_list(status, year)
                                       
        return self.construct_holiday_detail(holidays)     

        

@egb_api.api_class(resource_name='holiday')
class HolidayUpdateApi(remote.Service, HolidayHelper): 
    
    @endpoints.method(HolidayHelper.HOLIDAY_DETAIL_UPDATE_CONTAINER, 
                      HolidayDetailResponse,
                      name='update',
                      path='holiday/update',
                      http_method='POST')
    
    def holiday_detail_update(self, request):
        
        token = request.token
        holiday_key = request.holiday_key
        user_id = request.user_id
        days_off = request.days_off
        allowance = request.allowance
        allowance_type = request.allowance_type
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        JwtHelper().decode_holiday_auth_jwt(token, ip_address)
            
        return self.holiday_update_amend(user_id, holiday_key, allowance_type, allowance, days_off)
                              
                              
        
@egb_api.api_class(resource_name='holiday')
class HolidayBookApi(remote.Service, HolidayHelper): 
    
    @endpoints.method(HolidayHelper.HOLIDAY_INSERT, 
                      HolidayBookResponse,
                      name='book',
                      path='holiday/book',
                      http_method='POST')
    
    def holiday_book(self, request):
        
        token = request.token
        start_date = request.start_date
        end_date = request.end_date
        start_halfday = request.start_halfday
        end_halfday = request.end_halfday
        taken = request.taken
        ip_address =  self.request_state.headers['host']
        #Pending
        status = 1
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        #Pending
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id = payload['client_id']
        user_id = payload['user_id']
                                       
        return self.holiday_book_insert(user_id, client_id, start_date, end_date, start_halfday, end_halfday, taken, status)
    


@egb_api.api_class(resource_name='holiday')
class HolidayBookAmendApi(remote.Service, HolidayHelper): 
    
    @endpoints.method(HolidayHelper.HOLIDAY_INSERT_AMEND, 
                      HolidayBookResponse,
                      name='book.amend',
                      path='holiday/amend',
                      http_method='POST')
    
    def holiday_book_amend(self, request):
        
        token = request.token
        holiday_book_key = request.holiday_book_key
        start_date = request.start_date
        end_date = request.end_date
        start_halfday = request.start_halfday
        end_halfday = request.end_halfday
        total_days = request.total_taken
        ip_address =  self.request_state.headers['host']
        hashed = request.hashed
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        #Pending
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id = payload['client_id']
        user_id = payload['user_id']
                                       
        return self.holiday_book_amend_update(user_id, holiday_book_key, start_date, end_date, start_halfday, end_halfday, total_days, hashed)
        

@egb_api.api_class(resource_name='holiday')
class HolidayBookAuthApi(remote.Service, HolidayHelper): 
    
    @endpoints.method(HolidayHelper.HOLIDAY_INSERT_AUTH, HolidayBookResponse,
                      name='book.auth',
                      path='holiday/book/auth',
                      http_method='POST')
    
    def holiday_book_auth(self, request):
        
        token = request.token
        user_id = request.user_id
        holiday_key = request.holiday_key
        start_date = request.start_date
        end_date = request.end_date
        start_halfday = request.start_halfday
        end_halfday = request.end_halfday
        taken = request.taken
        ip_address =  self.request_state.headers['host']
        #Accepted
        status = 4
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_holiday_auth_jwt(token, ip_address)
                                   
        return self.holiday_book_insert_auth(holiday_key, user_id, start_date, end_date, start_halfday, end_halfday, taken, status)

        
        
@egb_api.api_class(resource_name='holiday')
class HolidayBookWithdrawApi(remote.Service, HolidayHelper): 
    
    @endpoints.method(HolidayHelper.HOLIDAY_CANCEL_WITHDRAW, 
                      HolidayBookResponse,
                      name='book.withdraw',
                      path='holiday/book/withdraw',
                      http_method='POST')
    
    def holiday_book_withdraw(self, request):
        
        token = request.token
        holiday_book_key = request.holiday_book_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
        
        user_id  = payload['user_id'] 
                     
        return self.holiday_book_withdraw_update(user_id, holiday_book_key, hashed)
        

@egb_api.api_class(resource_name='holiday')
class HolidayBookCancelApi(remote.Service, HolidayHelper): 
    
    @endpoints.method(HolidayHelper.HOLIDAY_CANCEL_WITHDRAW, 
                      HolidayBookResponse,
                      name='book.cancel',
                      path='holiday/book/cancel',
                      http_method='POST')
    
    def holiday_book_cancel(self, request):
        
        token = request.token
        holiday_book_key = request.holiday_book_key
        hashed = request.hashed
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        user_id  = payload['user_id'] 
        
        return self.holiday_book_cancel_update(user_id, holiday_book_key, hashed)
    
        

@egb_api.api_class(resource_name='holiday')
class HolidayBookApprovalApi(remote.Service, HolidayHelper): 
    
    @endpoints.method(HolidayHelper.HOLIDAY_APPROVAL, 
                      HolidayBookResponse,
                      name='book.approval',
                      path='book/approval',
                      http_method='POST')
    
    def holiday_book_approval(self, request):
        
        tokenVar = request.token
        holiday_book_key = request.holiday_book_key
        hashed = request.hashed
        status = request.status
        
        if status not in self.get_holiday_approval_status():
            status = 2
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_holiday_auth_jwt(tokenVar, ip_address)
            
        client_id  = payload['client_id'] 
                    
        return self.holiday_book_approval_update(client_id, holiday_book_key, hashed, status)

        

@egb_api.api_class(resource_name='holiday')
class HolidayBookListApi(remote.Service, HolidayHelper): 
    @endpoints.method(HolidayHelper.HOLIDAY_BOOK_LIST, 
                      HolidayBookList,
                      name='book.list',
                      path='holiday/book/list',
                      http_method='GET')
    def holiday_book_list(self, request):
        
        token = request.token
        holiday_book_status = request.holiday_book_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']   
            
        holiday_book = self.get_holiday_book_list(client_id, holiday_book_status)
            
        return self.construct_holiday_book_list(holiday_book)
        

@egb_api.api_class(resource_name='holiday')
class HolidayBookListAuthApi(remote.Service, HolidayHelper): 
    @endpoints.method(HolidayHelper.HOLIDAY_BOOK_AUTH_LIST, 
                      HolidayBookList,
                      name='book.list.auth',
                      path='holiday/book/list/auth',
                      http_method='GET')
    def holiday_book_list(self, request):
        
        token = request.token
        user_status = request.user_status
        holiday_book_status = request.holiday_book_status

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        JwtHelper().decode_holiday_auth_jwt(token, ip_address)
            
        holiday_book_list = self.get_holiday_book_list_auth(user_status, holiday_book_status)

        return self.construct_holiday_book_list(holiday_book_list)
                   
     
@egb_api.api_class(resource_name='trs')
class TotalRewardApi(remote.Service, TotalRewardHelper): 
         
    @endpoints.method(TotalRewardHelper.TRS_CONTAINER, 
                      TotalReward,
                      name='get',
                      path='trs/get',
                      http_method='GET')
    
    def trs(self, request):
         
        token = request.token

        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()

        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id = payload['client_id']
        user_id = int(payload['user_id'])
                     
        return self.get_total_reward(client_id, user_id)
        

@egb_api.api_class(resource_name='reward')
class RewardPoint(remote.Service, RewardPointHelper): 
    
    @endpoints.method(RewardPointHelper.REWARD_POINT_CONTAINER, 
                      RewardPointResponse,
                      name='points.insert',
                      path='reward/points/insert',
                      http_method='GET')
    
    def reward_points(self, request):
        
        token = request.token
        granted_to = request.granted_to
        points = request.points
        reason = request.reason
    
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']    
        user_id  = payload['user_id']   
            
        return self.insert_reward_point(client_id, user_id, granted_to, points, reason)
    
    
@egb_api.api_class(resource_name='reward')
class RewardPointList(remote.Service, RewardPointHelper): 
    
    @endpoints.method(RewardPointHelper.REWARD_POINT_LIST_CONTAINER, 
                      RewardPointList,
                      name='points.list',
                      path='reward/points/list',
                      http_method='GET')
    
    def reward_points_list(self, request):
        
        token = request.token
    
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id']    
        
        reward_point_list = self.get_reward_points_list(client_id)
            
        return self.contruct_list_point(reward_point_list)
        
        

@egb_api.api_class(resource_name='reward')
class RewardPointsApproval(remote.Service, RewardPointHelper): 
    
    @endpoints.method(RewardPointHelper.REWARD_POINT_APPROVAL_CONTAINER, 
                      RewardPointResponse,
                      name='points.approve',
                      path='reward/points/approve',
                      http_method='POST')
    
    def reward_points_approval(self, request):
        
        token = request.token
        hash_token = request.hash
        reward_key = request.reward_key
        status = request.status
        reason = request.reason
    
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        JwtHelper().decode_jwt_admin(token, ip_address)
            
        return self.reward_points_approval_update(reward_key, hash_token, status, reason)
        

@egb_api.api_class(resource_name='payslip')
class PayslipDatesApi(remote.Service, PayslipHelper): 
    
    @endpoints.method(PayslipHelper.PAYSLIP_LIST_DATES_CONTAINER, 
                      PayslipDates,
                      name='dates',
                      path='payslip/dates',
                      http_method='GET')
    
    def payslip_dates(self, request):
         
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id']    
                
        payslips = self.get_payslip_dates(client_id, user_id)
                         
        return self.construct_payslip_list_dates(payslips)        

           
     
@egb_api.api_class(resource_name='payslip')
class PayslipApi(remote.Service, PayslipHelper): 
    @endpoints.method(PayslipHelper.PAYSLIP_CONTAINER, 
                      PayslipList,
                      name='get',
                      path='payslip/get',
                      http_method='GET')
    def payslip(self, request):
         
        token = request.token
        
        date = request.date
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
                     
        payslips = self.get_payslip(client_id, user_id, date)
        
        return self.construct_payslip(payslips)        
        
        
@egb_api.api_class(resource_name='beneficiary')
class BeneficiaryApi(remote.Service, BeneficiaryHelper): 
    @endpoints.method(BeneficiaryHelper.BENEFICIARY_CONTAINER, Beneficiary,
                      name='insert',
                      path='beneficiary/insert',
                      http_method='POST')
    def beneficiary(self, request):
         
        token = request.token
        relationship = request.relationship
        firstname = request.firstname
        lastname = request.lastname
        dob = request.dob
        pension_percent = request.pension_percent
        life_percent = request.life_percent
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
        
        return self.insert_beneficiary(client_id, user_id, firstname, lastname, relationship, dob, pension_percent, life_percent)
    
        
@egb_api.api_class(resource_name='response')
class ResponseApi(remote.Service, ResponseHelper): 
         
    @endpoints.method(ResponseHelper.RESPONSE_CONTAINER, Response,
                      name='get',
                      path='response/get',
                      http_method='GET')
    
    def response(self, request):
        
        token = request.token
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired() 
        
        payload = JwtHelper().decode_jwt(token, ip_address)
        
        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
    
        # renamed variable to make the purpose more clear      
        has_left = self.has_left(client_id, user_id) 
                                 
        if has_left is False:
                
            # renamed variable             
            response = self.create_response(client_id, user_id)
            
            # renamed variable 
            response_message = self.construct_response(response)
        
            return response_message
        
        else:   
            
            raise ErrorHelper.response_not_found()
        

@egb_api.api_class(resource_name='wage')
class WageListApi(remote.Service, WageListHelper): 
    @endpoints.method(WageListHelper.WAGE_LIST_CONTAINER, 
                      WageCheckList,
                      name='list',
                      path='wage/list',
                      http_method='GET')
    def wage_list(self, request):
        
        token = request.token
        user_status = request.user_status
        
        ip_address =  self.request_state.headers['host']
#         authorisation =  self.request_state.headers['x-auth-token']
#         if not authorisation:
#             ErrorHelper.getAuthorizationRequired()
        
        payload = JwtHelper().decode_jwt(token, ip_address)
            
        client_id  = payload['client_id'] 
        user_id  = payload['user_id'] 
                     
        list_wages = self.get_list_wages(user_status)
    
        return self.construct_list_wages(list_wages)



application = endpoints.api_server([egb_api])
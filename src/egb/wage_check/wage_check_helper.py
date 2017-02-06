"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 27 Jan 2017

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from egb.user.user import UserModel
from egb.employee.employee import EmployeeModel
from egb.wage_check.wage_check import WageCheck, WageCheckList
from egb.car.car import CarModel, CarSignupModel
from egb.generic.car import CarTypeHelper
from egb.ccv.ccv import CcvModel, CcvSignupModel
from egb.generic.ctw import CtwTypeHelper
from egb.ctw.ctw import CtwModel, CtwSignupModel
from egb.ess.ess import EssModel
from egb.pension.pension import PensionModel, PensionSignupModel
from protorpc import messages
import endpoints


wage_list = {}


class WageListHelper():
    
    WAGE_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                      user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=False))
    
    def get_list_wages(self, user_status):
        
        user_key = self.get_user_key(user_status)
        self.get_ess(user_key)
        self.get_employee(user_key)
        self.get_ccv_signup_contribution(user_key)
        self.get_car_signup_contribution(user_key)
        self.get_ctw_signup_contribution(user_key)
        self.get_pension_signup_contribution(user_key)
        return wage_list

    
    def get_user_key(self, user_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        for user in qryUser:
            
            wage_list[int(user.id())] = {}
            wage_list[int(user.id())]['client_id'] = user.id()
            
        return qryUser
    

    def get_ess(self, qryUser):

        qryEss = EssModel.query(EssModel.user.IN(qryUser)).fetch()
        
        for ess in qryEss:

            if wage_list[(ess.user.id())]:
                wage_list[(ess.user.id())]['firstname'] = ess.firstname
                wage_list[(ess.user.id())]['lastname'] = ess.lastname

    
    
    def get_employee(self, qryUser):

        qryEmployee = EmployeeModel.query(EmployeeModel.user.IN(qryUser)).fetch()
        
        for employee in qryEmployee:

            if wage_list[employee.user.id()]:
                wage_list[(employee.user.id())]['user_id'] = employee.user_id
                wage_list[(employee.user.id())]['salary'] = employee.salary
                wage_list[(employee.user.id())]['weekly_hours'] = employee.weekly_hours
                
                

    def get_car_signup_contribution(self, qryUser):

        qryCarSignup = CarSignupModel.query(CarSignupModel.user.IN(qryUser),
                                            CarSignupModel.status.IN([CarTypeHelper.get_status_type(1), 
                                                                      CarTypeHelper.get_status_type(3),
                                                                      CarTypeHelper.get_status_type(5)])).order(-CarSignupModel.submitted).fetch()
                                            
        
        if qryCarSignup:
        
            for car_signup in qryCarSignup:
                
                if wage_list[(car_signup.user.id())]:
                    
                    wage_list[(car_signup.user.id())]['car'] = car_signup.gross_cost
        
        else:
            
            self.get_car_contribution(qryUser)
                

    def get_car_contribution(self, qryUser):

        qryCar = CarModel.query(CarModel.user.IN(qryUser),
                                CarModel.status == CarTypeHelper.get_status_type(1)).order(-CarModel.submitted).fetch()
        
        for car in qryCar:
            
            if wage_list[(car.user.id())]:
                
                wage_list[(car.user.id())]['car'] = car.gross_cost
                

    def get_ctw_signup_contribution(self, qryUser):

        qryCtwSignup = CtwSignupModel.query(CtwSignupModel.user.IN(qryUser),
                                            CtwSignupModel.status.IN([CtwTypeHelper.get_status_type(1),
                                                                      CtwTypeHelper.get_status_type(3),
                                                                      CtwTypeHelper.get_status_type(5)])).order(-CtwSignupModel.submitted).fetch()
                                            
        
        if qryCtwSignup:
        
            for ctw_signup in qryCtwSignup:
                
                if wage_list[int(ctw_signup.user.id())]:
                    
                    wage_list[int(ctw_signup.user.id())]['ctw'] = ctw_signup.gross_cost
        
        else:
            
            self.get_ctw_contribution(qryUser)
                

    def get_ctw_contribution(self, qryUser):

        qryCtw = CtwModel.query(CtwModel.user.IN(qryUser),
                                CtwModel.status == CtwTypeHelper.get_status_type(1)).order(-CtwModel.submitted).fetch()
        
        for ctw in qryCtw:
            
            if wage_list[int(ctw.user.id())]:
                
                wage_list[int(ctw.user.id())]['ctw'] = ctw.gross_cost
                

    def get_ccv_signup_contribution(self, qryUser):

        qryCcvSignup = CcvSignupModel.query(CcvSignupModel.user.IN(qryUser)).fetch()
    
        
        if qryCcvSignup:
            
            for ccv_signup in qryCcvSignup:
                
                if wage_list[int(ccv_signup.user.id())]:
                    
                    wage_list[int(ccv_signup.user.id())]['ccv'] = ccv_signup.contribution
        
        else:
            
            self.get_ccv_contribution(qryUser)
        
        
    def get_ccv_contribution(self, qryUser):

        qryCcv = CcvModel.query(CcvModel.user.IN(qryUser)).fetch()
        
        for ccv in qryCcv:
            
            if wage_list[int(ccv.user.id())]:
                
                wage_list[int(ccv.user.id())]['ccv'] = ccv.contribution
                

    def get_pension_signup_contribution(self, qryUser):

        qryPensionSignup = PensionSignupModel.query(PensionSignupModel.user.IN(qryUser)).fetch()
        
        if qryPensionSignup:
            
            for pension_signup in qryPensionSignup:
                
                if wage_list[int(pension_signup.user.id())]:
                    
                    if pension_signup.tax_saving == 'SALARY_SACRIFICE':
                        
                        wage_list[int(pension_signup.user.id())]['pension_contribution'] = pension_signup.employee_contribution
                        
        else:
            
            self.get_pension_contribution(qryUser)
                
                
    def get_pension_contribution(self, qryUser):

        qryPension = PensionModel.query(PensionModel.user.IN(qryUser)).fetch()
        
        for pension in qryPension:
            
            if wage_list[int(pension.user.id())]:
                
                if pension.tax_saving == 'SALARY_SACRIFICE':
                    
                    wage_list[int(pension.user.id())]['pension_contribution'] = pension.employee_contribution
                    
                
    
    def construct_list_wages(self, list_wages):
        
        wage_chech_listArr = []
        
        for wage in list_wages:
            
            user_id = 0
            client_id = 0
            firstname=""
            lastname=""
            wage_check = list_wages[wage]
            salary = 0.00;
            weekly_hours = 0.00
            car = 0.00
            ctw = 0.00
            ccv = 0.00
            pension = 0.00
            
            if 'user_id' in  wage_check.keys():
                user_id = wage_check['user_id']
                
            if 'client_id' in  wage_check.keys():
                client_id = wage_check['client_id']

            if 'firstname' in  wage_check.keys():
                firstname = wage_check['firstname']
                
            if 'lastname' in  wage_check.keys():
                lastname = wage_check['lastname']

            if 'salary' in  wage_check.keys():
                salary = wage_check['salary']
                
            if 'weekly_hours' in  wage_check.keys():
                weekly_hours = wage_check['weekly_hours']

            if 'car' in  wage_check.keys():
                car = wage_check['car']

            if 'ctw' in  wage_check.keys():
                ctw = wage_check['ctw']
                
            if 'ccv' in  wage_check.keys():
                ccv = wage_check['ccv']
                
            if 'pension_contribution' in  wage_check.keys():
                pension = wage_check['pension_contribution']
                
            weekly_salary = salary/52
            
            if salary != 0:
                
                hourly_salary = weekly_salary/weekly_hours
            
                total_sacrifice = pension + ccv + car
                total_sacrifice_weekly = total_sacrifice * 12 / 52
                total_sacrifice_hourly = total_sacrifice_weekly/weekly_salary
                total_sacrificed = hourly_salary - total_sacrifice_hourly
                
                wage_chech_listArr.append(WageCheck(user_id=user_id,
                                                    client_id=client_id,
                                                    firstname=firstname,
                                                    lastname=lastname,
                                                    salary=salary,
                                                    weekly_hours=weekly_hours,
                                                    car=car,
                                                    ccv=ccv,
                                                    ctw=ctw,
                                                    pension=pension,
                                                    total_sacrificed=total_sacrificed))
        
        return WageCheckList(wage_check_list=wage_chech_listArr)
            


        
        
        
                
        
        














from protorpc import messages
from egb.car.car import Car, CarList, CarModel, CarSignupModel, CarSignup, CarSignupList, CarSignupResponse
from egb.generic.car import CarTypeHelper, StatusType
from egb.ess.ess import EssModel
from egb.user.user import UserModel
from google.appengine.ext import ndb
from libs.parse.parse import Parse
from libs.tokenGenerate.token import Token
from egb.utils.error import ErrorHelper
from egb.name_field.name_field import ManagerField, EmployeeField, NameFieldHelper
from egb.user.user_helper import UserHelper
from libs.date_time.date_time import DateTime
import endpoints
    
class CarHelper(Parse, CarTypeHelper, UserHelper, NameFieldHelper):
    
    CAR_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    CAR_SIGNUP_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))

    CAR_SIGNUP_LIST_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                 user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                                 car_signup_status=messages.EnumField(StatusType, 3, repeated=True))

    CAR_SIGNUP_APPROVAL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                car_signup_key=messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                hashed=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                                status=messages.EnumField(StatusType, 4, required=True))
    
    
    def get_car(self, client_id, user_id):
                                           
        cars = CarModel.query(CarModel.user == ndb.Key('UserModel', client_id),
                              CarModel.status.IN([self.get_status_type(5),
                                                 self.get_status_type(1)])).fetch()

        if cars:
            
            return cars
        
        raise ErrorHelper.car_not_found()
    
    def construct_car(self, cars):
        
        carsArr = []
        
        for car in cars:
            
            submitted = self.parseDateFormatHyphen(car.submitted)
            
            car = Car(user_id=car.user_id,
                      provider_name=car.provider_name,
                      product_type=car.product_type,
                      product_variation=car.product_variation,
                      gross_cost=car.gross_cost,
                      status=car.status,
                      submitted=submitted)
            
            carsArr.append(car)
            
        return CarList(car_list = carsArr)
    

    def car_signup_list_get(self, client_id, user_id):
        
        qryCarSignup = CarSignupModel.query(CarSignupModel.user == ndb.Key('UserModel', client_id),
                                            CarSignupModel.user_id==user_id).fetch()
        
        if qryCarSignup:
            
            return qryCarSignup
        
        raise ErrorHelper.car_signup_not_found()
    
    
    def car_signup_list_auth_get(self, user_status, car_signup_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryCarSignup = CarSignupModel.query(CarSignupModel.user.IN(qryUser),
                                            CarSignupModel.status.IN(car_signup_status)).fetch()
        
        if qryCarSignup:
            
            return qryCarSignup
        
        raise ErrorHelper.car_signup_not_found()
    
    
    def construct_car_signup_list(self, car_signup_list):

        car_signup_listArr = []
        
        print car_signup_list

        ess_list = EssModel.get_ess(self.get_key_list(car_signup_list))
        
        for car_signup in car_signup_list:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if car_signup.manager:
                
                manager_key = car_signup.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if car_signup.user:
                
                employee_key = car_signup.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
            
            submitted = self.parseDateTimeFormatHyphen(car_signup.submitted)
                        
            car_signup_list = CarSignup(user_id=car_signup.user_id,
                                        car_signup_key=car_signup.key.id(),
                                        gross_cost=car_signup.gross_cost,
                                        token=car_signup.token,
                                        submitted=submitted,
                                        status=car_signup.status,
                                        manager=ManagerField(firstname=manager_firstname, 
                                                             lastname=manager_lastname),
                                        employee=EmployeeField(firstname=employee_firstname, 
                                                               lastname=employee_lastname))
            
            car_signup_listArr.append(car_signup_list) 
            
        return CarSignupList(car_signup_list=car_signup_listArr)


    def car_signup_approval_update(self, client_id, user_id, car_signup_key, hashed, status):
        
        qryCarSignup = CarSignupModel.query(CarSignupModel.key == ndb.Key('CarSignupModel', car_signup_key),
                                            CarSignupModel.token == hashed,
                                            CarSignupModel.status == self.get_status_type(3)).get()
        
        
        if qryCarSignup:
            
            car_key = CarModel(provider_name=qryCarSignup.provider_name,
                               product_type=qryCarSignup.product_type,
                               product_variation=qryCarSignup.product_variation,
                               user=qryCarSignup.user,
                               user_id=qryCarSignup.user_id,
                               status=status,
                               gross_cost=qryCarSignup.gross_cost)
                     
            car_key.put()
            
            tokenVar = Token.generate_token()
            qryCarSignup.car = car_key.key
            qryCarSignup.token = tokenVar
            qryCarSignup.status = status
            qryCarSignup.submitted = DateTime.getCurrentDateTime()
            qryCarSignup.manager = ndb.Key('UserModel', client_id)
            qryCarSignup.put()               
        
            return CarSignupResponse(message="Successfully %s" % (status))
        
        
        raise ErrorHelper.car_signup_not_found()
    
    
        

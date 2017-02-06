from protorpc import messages
from egb.employee.employee import EmployeeModel, EmployeeList
from egb.employee.employee import Employee
from google.appengine.ext import ndb
from libs.parse.parse import Parse
from egb.utils.error import ErrorHelper
import endpoints
    
class EmployeeTypeHelper(Parse):
    
    EMPLOYEE_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    def get_employee(self, client_id, user_id):
                                         
        employees = EmployeeModel.query(EmployeeModel.user == ndb.Key('UserModel', client_id)).fetch()

        if employees:
            
            return employees
        
        raise ErrorHelper.employee_not_found()


    def construct_employee(self, employees):
        
        employeesArr = []
        
        for employee in employees:

            start_date = self.parseDateFormatHyphen(employee.start_date)
            end_date = self.parseDateFormatHyphen(employee.end_date)
            employee = Employee(user_id=employee.user_id,
                                gender=employee.gender,
                                employee_id=employee.employee_id,
                                job_title=employee.job_title,
                                start_date=start_date,
                                end_date=end_date,
                                annual_salary=employee.salary,
                                hourly_rate=employee.hourly_rate,
                                currency=employee.currency,
                                bonus=employee.bonus,
                                commission=employee.commission,
                                overtime=employee.overtime,
                                weekly_hours=employee.weekly_hours)
            
            employeesArr.append(employee)
        
        return EmployeeList(employee_list=employeesArr)


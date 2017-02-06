from google.appengine.ext import ndb
from egb.holiday.holiday import HolidayBook, HolidayBookList, HolidayBookResponse
from egb.holiday.holiday import Holiday, HolidayDetailResponse
from egb.holiday.holiday import HolidayDetailList
from egb.holiday.holiday import HolidayModel
from egb.holiday.holiday import HolidayBookModel
from egb.generic.holiday import HolidayTypeHelper, Allowance
from egb.user.user import UserModel
from egb.ess.ess import EssModel
from egb.name_field.name_field import EmployeeField, ManagerField, NameFieldHelper
from libs.parse.parse import Parse
from libs.date_time.date_time import DateTime
from libs.tokenGenerate.token import Token
from protorpc import messages
from egb.user.user_helper import UserHelper
from egb.utils.error import ErrorHelper

import endpoints

HOLIDAY_APPROVAL_STATUS = [2, 4]
    
class HolidayHelper(Parse, HolidayTypeHelper, UserHelper, NameFieldHelper):
    
    HOLIDAY_DETAIL_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                       year=messages.IntegerField(2, variant=messages.Variant.INT32, required=True))

    HOLIDAY_DETAIL_LIST_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                status=messages.IntegerField(2, variant=messages.Variant.INT32, required=False),
                                                                year=messages.IntegerField(3, variant=messages.Variant.INT32, required=True))
    
    HOLIDAY_DETAIL_UPDATE_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                                  holiday_key = messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                                  user_id = messages.IntegerField(3, variant=messages.Variant.INT32, required=True),
                                                                  days_off = messages.StringField(4, variant=messages.Variant.STRING, required=False),
                                                                  allowance = messages.FloatField(5, variant=messages.Variant.FLOAT, required=True),
                                                                  allowance_type = messages.IntegerField(6, variant=messages.Variant.INT32, required=True))
    
    HOLIDAY_LIST_AUTH = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    HOLIDAY_INSERT = endpoints.ResourceContainer(token = messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                 start_date = messages.StringField(2, variant=messages.Variant.STRING, required=True),
                                                 end_date = messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                 start_halfday = messages.IntegerField(4, variant=messages.Variant.INT32, required=True),
                                                 end_halfday = messages.IntegerField(5, variant=messages.Variant.INT32, required=True),
                                                 taken = messages.FloatField(6, variant=messages.Variant.FLOAT, required=True))
    
    HOLIDAY_INSERT_AUTH = endpoints.ResourceContainer(token = messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                      user_id = messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                      holiday_key = messages.IntegerField(3, variant=messages.Variant.INT64, required=True),
                                                      start_date = messages.StringField(4, variant=messages.Variant.STRING, required=True),
                                                      end_date = messages.StringField(5, variant=messages.Variant.STRING, required=True),
                                                      start_halfday = messages.IntegerField(6, variant=messages.Variant.INT32, required=True),
                                                      end_halfday = messages.IntegerField(7, variant=messages.Variant.INT32, required=True),
                                                      taken = messages.FloatField(8, variant=messages.Variant.FLOAT, required=True))
    
    HOLIDAY_INSERT_AMEND = endpoints.ResourceContainer(token = messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                 holiday_ook_key = messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                 start_date = messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                 end_date = messages.StringField(4, variant=messages.Variant.STRING, required=True),
                                                 start_halfday = messages.IntegerField(5, variant=messages.Variant.INT32, required=True),
                                                 end_halfday = messages.IntegerField(6, variant=messages.Variant.INT32, required=True),
                                                 total_taken = messages.FloatField(7, variant=messages.Variant.FLOAT, required=True),
                                                 hashed = messages.StringField(8, variant=messages.Variant.STRING, required=True))
    
    HOLIDAY_CANCEL_WITHDRAW = endpoints.ResourceContainer(token = messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                          holiday_book_key = messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                          hashed = messages.StringField(3, variant=messages.Variant.STRING, required=True))
    
    HOLIDAY_APPROVAL = endpoints.ResourceContainer(token = messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                   holiday_book_key = messages.IntegerField(2, variant=messages.Variant.INT64, required=True),
                                                   hashed = messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                   status = messages.IntegerField(4, variant=messages.Variant.INT32, required=True))
    
    HOLIDAY_BOOK_LIST = endpoints.ResourceContainer(token = messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                    holiday_book_status = messages.StringField(2, variant=messages.Variant.STRING, required=True))
    
    HOLIDAY_BOOK_AUTH_LIST = endpoints.ResourceContainer(token = messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                         user_status = messages.IntegerField(2, variant=messages.Variant.INT32, required=True),
                                                         holiday_book_status = messages.StringField(3, variant=messages.Variant.STRING, required=True))
    
    
    def get_holiday_approval_status(self):
        
        return HOLIDAY_APPROVAL_STATUS
    
    
    
    def get_holiday_detail(self, client_id, year):
                                           
        holidays = HolidayModel.query(HolidayModel.user == ndb.Key('UserModel', client_id), 
                                      HolidayModel.year == year).fetch()
        
        if holidays:

            return holidays
        
        raise ErrorHelper.holiday_not_found()
    

    def construct_holiday_detail(self, holiday_list):

        holidaysArr = []
        
        ess_list = EssModel.get_ess(self.get_key_list(holiday_list))  
        
        for holiday in holiday_list:
            
            employee_firstname = ""
            employee_lastname = ""
                  
            if holiday.user:
                
                employee_key = holiday.user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
                
            holiday = Holiday(holiday_key=holiday.key.id(),
                              user_id=holiday.user_id,
                              team = holiday.team,
                              days_off=holiday.days_off,
                              allowance=holiday.allowance,
                              allowance_type=holiday.allowance_type,
                              employee=EmployeeField(firstname=employee_firstname, 
                                                     lastname=employee_lastname),
                              year=holiday.year)
             
            holidaysArr.append(holiday)
        
        return HolidayDetailList(holiday_detail_list = holidaysArr)
        
    
    
    def get_holiday_list(self, user_status, year):
    
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)

        holiday_list = HolidayModel.query(HolidayModel.user.IN(qryUser)).fetch()
        
        if holiday_list:
            
            return holiday_list 
        
        raise ErrorHelper.holiday_not_found()
    
    
    def holiday_update_amend(self, user_id, holiday_key, allowance_type, allowance, days_off):
        
        allowance_type = self.get_allowance_type(allowance_type)
        
        if days_off:
            
            days_off = days_off.split(',')
            
        else:
            
            days_off = []
            
                                           
        holidays = HolidayModel.query(HolidayModel.key == ndb.Key('HolidayModel', holiday_key),
                                      HolidayModel.user_id == user_id).get()
        
        if holidays:    
    
            holidays.allowance_type = allowance_type
            holidays.allowance = allowance    
            holidays.days_off = days_off
            holidays.put()
            
            return HolidayDetailResponse(message = "Successfully updated")
        
        raise ErrorHelper.holiday_not_found()
    
    
    def get_holiday_book(self, client_id):
                                           
        holidays = HolidayModel.query(HolidayModel.user == ndb.Key('UserModel', client_id)).get()

        if holidays:
            
            return holidays
        
        raise ErrorHelper.holiday_not_found()
    

    def holiday_book_insert(self, user_id, client_id, start_date, end_date, start_halfday, end_halfday, taken, status):
        
        qryHoliday = HolidayModel.query(HolidayModel.user == ndb.Key('UserModel', client_id)).get()
        
        if qryHoliday:
        
            tokenVar = Token.generate_token()
            start_date  = self.parseDate(start_date)
            end_date  = self.parseDate(end_date)
            status = self.get_status_type(status)
            start_halfday = self.get_halfday_type(start_halfday)
            end_halfday = self.get_halfday_type(end_halfday)
            allowance_type = self.get_allowance_type(qryHoliday.allowance_type)

            HolidayBookModel(holiday=ndb.Key('HolidayModel',qryHoliday.key.id()),
                             user = ndb.Key('UserModel', client_id),
                             user_id=user_id,
                             start_date=start_date,
                             end_date=end_date,
                             start_halfday=start_halfday,
                             end_halfday=end_halfday,
                             status=status,
                             allowance_type=allowance_type,
                             token=tokenVar,
                             taken=taken).put()
                                     
            return HolidayBookResponse(message="Successfully Booked")
        
        raise ErrorHelper.holiday_not_found()
    
    def holiday_book_insert_auth(self, holiday_key, user_id, start_date, end_date, start_halfday, end_halfday, taken, status):
        
        qryHoliday = HolidayModel.query(HolidayModel.key == ndb.Key('HolidayModel', holiday_key)).get()
        
        if qryHoliday:
        
            tokenVar = Token.generate_token()
            start_date  = self.parseDate(start_date)
            end_date  = self.parseDate(end_date)
            status = self.get_status_type(status)
            start_halfday = self.get_halfday_type(start_halfday)
            end_halfday = self.get_halfday_type(end_halfday)
            
            HolidayBookModel(holiday=ndb.Key('HolidayModel',qryHoliday.key.id()),
                             user= UserModel.query(UserModel.user_id == user_id).get().key,
                             user_id=user_id,
                             start_date=start_date,
                             end_date=end_date,
                             start_halfday=start_halfday,
                             end_halfday=end_halfday,
                             allowance_type=qryHoliday.allowance_type,
                             status=status,
                             token=tokenVar,
                             taken=taken).put()
                                     
            return HolidayBookResponse(message="Successfully Booked")
        
        raise ErrorHelper.holiday_not_found()
    
    
    def holiday_book_amend_update(self, user_id, holiday_book_key, start_date, end_date, start_halfday, end_halfday, total_days, hashed):
        
        qryHolidayBook = HolidayBookModel.query(HolidayBookModel.key == ndb.Key('HolidayBookModel', holiday_book_key),
                                                HolidayBookModel.token == hashed,
                                                HolidayBookModel.user_id == user_id,
                                                ndb.OR(HolidayBookModel.status == self.get_status_type(1),
                                                       HolidayBookModel.status == self.get_status_type(4))).get()
         
        if qryHolidayBook:
        
            tokenVar = Token.generate_token()
            start_date  = self.parseDate(start_date)
            end_date  = self.parseDate(end_date)
            status = self.get_status_type(1)
            start_halfday = self.get_halfday_type(start_halfday)
            end_halfday = self.get_halfday_type(end_halfday)
            
            qryHolidayBook.start_date = start_date
            qryHolidayBook.end_date = end_date
            qryHolidayBook.status = status
            qryHolidayBook.start_halfday = start_halfday
            qryHolidayBook.end_halfday = end_halfday
            qryHolidayBook.token = tokenVar
            qryHolidayBook.submitted = DateTime.getCurrentDateTime()
            qryHolidayBook.put()
                                     
            return HolidayBookResponse(message="Successfully Amended")
        
        raise ErrorHelper.holiday_book_not_found()
                                 
    
    def holiday_book_withdraw_update(self, user_id, holiday_book_key, hashed):
                                           
        holidays = HolidayBookModel.query(HolidayBookModel.key == ndb.Key('HolidayBookModel', holiday_book_key),
                                          HolidayBookModel.user_id == user_id,
                                          HolidayBookModel.status == self.get_status_type(1),
                                          HolidayBookModel.token == hashed).get()
        if holidays:
            
            status = self.get_status_type(3)
            tokenVar = Token.generate_token()  
            
            holidays.token = tokenVar             
            holidays.status = status
            holidays.submitted = DateTime.getCurrentDateTime()
            holidays.put()
            
            return HolidayBookResponse(message="Successfully Withdrawn")
            
        
        raise ErrorHelper.holiday_not_found()
    
    

    def holiday_book_cancel_update(self, user_id, holiday_book_key, hashed):
                                           
        holidays = HolidayBookModel.query(HolidayBookModel.key == ndb.Key('HolidayBookModel', holiday_book_key),
                                          HolidayBookModel.user_id == user_id,
                                          HolidayBookModel.status == self.get_status_type(4),
                                          HolidayBookModel.token == hashed).get()

        if holidays:
            
            status = self.get_status_type(2)
            tokenVar = Token.generate_token()  
            
            holidays.token = tokenVar               
            holidays.status = status
            holidays.submitted = DateTime.getCurrentDateTime()
            holidays.put()
            
            return HolidayBookResponse(message="Successfully canceled")
        
        raise ErrorHelper.holiday_not_found()
    
    

    def holiday_book_approval_update(self, client_id, holiday_book_key, hashed, status):
                                           
        holidays = HolidayBookModel.query(HolidayBookModel.key == ndb.Key('HolidayBookModel', holiday_book_key),
                                          HolidayBookModel.token == hashed,
                                          ndb.OR(HolidayBookModel.status != self.get_status_type(2),
                                                 HolidayBookModel.status != self.get_status_type(4))).get()

        if holidays:

            holidays.token = Token.generate_token()            
            holidays.status = self.get_status_type(status)
            holidays.submitted = DateTime.getCurrentDateTime()
            holidays.manager = ndb.Key('UserModel', client_id)
            holidays.put()
            getStatus = self.get_status_type(status)
            
            return HolidayBookResponse(message="Successfully " + str(getStatus))
            
        raise ErrorHelper.holiday_not_found()
    

    def get_holiday_book_list(self, client_id, holiday_book_status):
        
        statusArr = []

        for status in holiday_book_status.split(','):
            
            statusArr.append(self.get_status_type(int(status)))
                                           
        holiday_book = HolidayBookModel.query(HolidayBookModel.user == ndb.Key('UserModel', client_id),
                                              HolidayBookModel.status.IN(statusArr)).fetch()
                                              
        if  holiday_book:
    
            return holiday_book
            
        raise ErrorHelper.holiday_book_list_not_found()
    
    
    def get_holiday_book_list_auth(self, user_status, holiday_book_status):
        
        user_keyArr = []
        
        holiday_book_statusArr = []
        
        for status in holiday_book_status.split(','):
            
            holiday_book_statusArr.append(self.get_status_type(int(status)))
        
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch()
        
        for user in qryUser:
            
            user_keyArr.append(user.key)
                                           
        holiday_book_list = HolidayBookModel.query(HolidayBookModel.user.IN(user_keyArr), 
                                                   HolidayBookModel.status.IN(holiday_book_statusArr)).fetch()
        
        if holiday_book_list:
            
            return holiday_book_list
        
        raise ErrorHelper.holiday_book_list_not_found()
    


    def construct_holiday_book_list(self, holiday_books):
        
        user_keyArr = []
        holiday_booksArr = []
        
        for user in holiday_books:
            
            if user.manager:
                user_keyArr.append(user.manager)
            
            if user.holiday.get().user:
                user_keyArr.append(user.holiday.get().user)
                
                
        ess_list = EssModel.get_ess(user_keyArr)       
                                    
        for holiday_book in holiday_books:
            
            manager_firstname = ""
            manager_lastname = ""
            employee_firstname = ""
            employee_lastname = ""
            
            if holiday_book.manager:
                
                manager_key = holiday_book.manager.id()
                manager_firstname = ess_list[manager_key]['firstname']
                manager_lastname = ess_list[manager_key]['lastname']
                  
            if holiday_book.holiday.get().user:
                
                employee_key = holiday_book.holiday.get().user.id()
                employee_firstname = ess_list[employee_key]['firstname']
                employee_lastname = ess_list[employee_key]['lastname']
            
            start_date = self.parseDateFormatHyphen(holiday_book.start_date)
            end_date = self.parseDateFormatHyphen(holiday_book.end_date)
            submitted = self.parseDateFormatHyphen(holiday_book.submitted)

            holiday_book = HolidayBook(holiday_book_key = holiday_book.key.id(),
                                       user_id = holiday_book.user_id,
                                       start_date = start_date,
                                       end_date = end_date,
                                       start_halfday = holiday_book.start_halfday,
                                       end_halfday = holiday_book.end_halfday,
                                       taken = holiday_book.taken,
                                       status = holiday_book.status,
                                       allowance_type = holiday_book.allowance_type,
                                       submitted = submitted,
                                       manager=ManagerField(firstname=manager_firstname, 
                                                       lastname=manager_lastname),
                                       employee=EmployeeField(firstname=employee_firstname, 
                                                         lastname=employee_lastname),
                                       token = holiday_book.token)
            
            holiday_booksArr.append(holiday_book)

        return HolidayBookList(holiday_book_list=holiday_booksArr)
    
    
    
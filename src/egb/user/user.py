from google.appengine.ext import ndb
from protorpc import messages
from egb.employer.employer import EmployerModel
    
# TODO - What should be sent as a standard request    
class User(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    employee_id = messages.IntegerField(2, required=True)
    email = messages.StringField(3, required=True)
    dob = messages.StringField(4, required=True)
    
class UserList(messages.Message):
    user_list = messages.MessageField(User, 1, repeated=True)
      
class UserModel(ndb.Model):
    employer = ndb.KeyProperty(kind=EmployerModel)
    user_id = ndb.IntegerProperty(required=True)
    employee_id = ndb.IntegerProperty(required=True)
    email = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    dob = ndb.DateProperty(required=True)
    android_id = ndb.StringProperty(repeated=True, required=False)    
    android_gcm = ndb.StringProperty(repeated=True, required=False)
    android_pin = ndb.IntegerProperty(repeated=True, required=False)
    iphone_id = ndb.StringProperty(repeated=True, required=False)
    iphone_gcm = ndb.StringProperty(repeated=True, required=False)
    iphone_pin = ndb.IntegerProperty(repeated=True, required=False)
    hash = ndb.StringProperty(required=True)
    access_token =  ndb.StringProperty(required=False)
    logged_in = ndb.DateTimeProperty(required=False)
    status = ndb.IntegerProperty(required=True)
    roles = ndb.StringProperty(repeated=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_count(cls):
        return cls.query().count()
    
    @classmethod
    def get_submitted(cls):
        dateSubmitted = cls.query().order(-cls.submitted).get();
        if dateSubmitted:
            return dateSubmitted.submitted
        else:
            return False
    
    @classmethod
    def get_user_active_status_key(cls, status):
        user_keyArr = []
        
        if status == 1 or status == 0:
            qryUser = cls.query(cls.status == status).fetch() 
        else:
            qryUser = cls.query().fetch() 
        
        for user in qryUser:
            user_keyArr.append(ndb.Key('UserModel', user.key.id()))   
            
        return user_keyArr
     
    
        
from protorpc import messages
from egb.user.user import UserModel, User, UserList
from google.appengine.ext import ndb
from libs.parse.parse import Parse
from egb.utils.error import ErrorHelper
import endpoints
    
class UserHelper(Parse):
    
    USER_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    def get_user(self, client_id, user_id):
                           
        users = UserModel.query(UserModel.key == ndb.Key('UserModel', client_id), 
                                UserModel.user_id == user_id).fetch()
        
        if users:

            return users
        
        raise  ErrorHelper.user_not_found()
    
    
    def construct_user(self, users):
        
        userArr = []
        
        for user in users:
            
            dob = self.parseDateFormatHyphen(user.dob)
            
            user = User(user_id=user.user_id,
                        employee_id=user.employee_id,
                        email=user.email,
                        dob=dob)
            
            userArr.append(user)
    
        return UserList(user_list=userArr)

    
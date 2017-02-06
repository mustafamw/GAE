from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from egb.user.user import UserModel
from protorpc import messages
from egb.generic.ess import TitleType

class EssResponse(messages.Message):
    message = messages.StringField(1, required=True)
   
class Ess(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    firstname = messages.StringField(2, required=False)
    lastname = messages.StringField(3, required=False)
    maiden_name = messages.StringField(4, required=False)
    address = messages.StringField(5, required=False)
    city = messages.StringField(6, required=True)
    county = messages.StringField(7, required=True)
    postcode = messages.StringField(8, required=True)
    contact_no = messages.StringField(9, required=False)
    bank_holder_name = messages.StringField(10, required=False)
    bank_name = messages.StringField(11, required=False)
    account_no = messages.IntegerField(12, required=False)
    sort_code = messages.StringField(13, required=False)
    title = messages.EnumField(TitleType, 14, required=True)
    ni_no = messages.StringField(15, required=False)
    
class EssList(messages.Message):
    ess_list = messages.MessageField(Ess, 1, repeated=True)
                                     
                                     
class EssModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    title = msgprop.EnumProperty(TitleType, required=True)
    firstname = ndb.StringProperty(required=False)
    lastname = ndb.StringProperty(required=False)
    maiden_name = ndb.StringProperty(required=False)
    address = ndb.StringProperty(required=False) 
    city = ndb.StringProperty(required=False)
    county = ndb.StringProperty(required=False) 
    postcode = ndb.StringProperty(required=False)        
    contact_no = ndb.StringProperty(required=False)   
    bank_holder_name = ndb.StringProperty(required=False) 
    bank_name = ndb.StringProperty(required=False)
    account_no = ndb.IntegerProperty(required=False)
    sort_code = ndb.StringProperty(required=False)
    submitted = ndb.DateTimeProperty(auto_now_add=True)
    ni_no = ndb.StringProperty(required=False)
    
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
    def get_ess(cls, user_key):
        
        ess_list_obj = {}
        
        qryEss = cls.query(cls.user.IN(user_key)).fetch()
        
        for ess in qryEss:
            
            ess_list_obj[ess.user.id()] = {'firstname': ess.firstname,
                                           'lastname': ess.lastname}
        
        return ess_list_obj
    

class EssUpdated(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    firstname = messages.StringField(2, required=False)
    lastname = messages.StringField(3, required=False)
    maiden_name = messages.StringField(4, required=False)
    address = messages.StringField(5, required=False)
    city = messages.StringField(6, required=True)
    county = messages.StringField(7, required=True)
    postcode = messages.StringField(8, required=True)
    contact_no = messages.StringField(9, required=False)
    email = messages.StringField(10, required=False)
    bank_holder_name = messages.StringField(11, required=False)
    bank_name = messages.StringField(12, required=False)
    account_no = messages.IntegerField(13, required=False)
    sort_code = messages.StringField(14, required=False)
    title = messages.EnumField(TitleType, 15, required=True)
    ni_no = messages.StringField(16, required=False)
    submitted = messages.StringField(17, required=True)
    
    
class EssUpdatedList(messages.Message):
    ess_updated_list = messages.MessageField(EssUpdated, 1, repeated=True)


class EssUpdatedModel(ndb.Model):
    ess = ndb.KeyProperty(kind=EssModel, required=True)
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    ni_no = ndb.StringProperty(required=False)
    title = msgprop.EnumProperty(TitleType, required=True)
    firstname = ndb.StringProperty(required=False)
    lastname = ndb.StringProperty(required=False)
    maiden_name = ndb.StringProperty(required=False)
    address = ndb.StringProperty(required=False) 
    city = ndb.StringProperty(required=False)
    county = ndb.StringProperty(required=False) 
    postcode = ndb.StringProperty(required=False)        
    contact_no = ndb.StringProperty(required=False) 
    email = ndb.StringProperty(required=False)   
    bank_holder_name = ndb.StringProperty(required=False) 
    bank_name = ndb.StringProperty(required=False)
    account_no = ndb.IntegerProperty(required=False)
    sort_code = ndb.StringProperty(required=False)
    submitted = ndb.DateTimeProperty(auto_now_add=True)

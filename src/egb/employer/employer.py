from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.employer import EmployerVariation
    
    
class Employer(messages.Message):
    name = messages.StringField(1, required=True)
    variation = messages.EnumField(EmployerVariation, 2, required=True)
    window_life_start = messages.StringField(3, required=False)
    window_life_end = messages.StringField(4, required=False)
    window_cic_start = messages.StringField(5, required=False)
    window_cic_end = messages.StringField(6, required=False)
    window_pmi_start = messages.StringField(7, required=False)
    window_pmi_end = messages.StringField(8, required=False)
    window_ctw_start = messages.StringField(9, required=False)
    window_ctw_end = messages.StringField(10, required=False)
    window_wg_start = messages.StringField(11, required=False)
    window_wg_end = messages.StringField(12, required=False)       
    web_link = messages.StringField(13, required=True)
    handbook_link = messages.StringField(14, required=True)
    contact_link = messages.StringField(15, required=True)
    contact_email = messages.StringField(16, required=True)
    contact_phone = messages.StringField(17, required=True)
    bumf = messages.StringField(18, required=True)
    email_ess = messages.StringField(19, required=False)
    email_holiday = messages.StringField(20, required=False)
    email_pension = messages.StringField(21, required=False)
    email_life = messages.StringField(22, required=False)
    email_cic = messages.StringField(23, required=False)
    email_gip = messages.StringField(24, required=False)
    email_cp = messages.StringField(25, required=False)
    email_dental = messages.StringField(26, required=False)
    email_ha = messages.StringField(27, required=False)
    email_hr = messages.StringField(28, required=False)
    email_default = messages.StringField(29, required=True)
    image_links=messages.StringField(30, required=False)
    welcome_note=messages.StringField(31, required=False)
    company_icon=messages.StringField(32, required=False)
    company_slogan=messages.StringField(33, required=False)
    

class EmployerList(messages.Message):
    employer_list = messages.MessageField(Employer, 1, repeated=True)
    
    
class EmployerModel(ndb.Model):
    name = ndb.StringProperty(required=True)
    variation = msgprop.EnumProperty(EmployerVariation, required=True, indexed=True)
    window_life_start = ndb.DateProperty(required=False)    
    window_life_end = ndb.DateProperty(required=False)
    window_cic_start = ndb.DateProperty(required=False)
    window_cic_end = ndb.DateProperty(required=False)
    window_pmi_start = ndb.DateProperty(required=False)    
    window_pmi_end = ndb.DateProperty(required=False)
    window_ctw_start = ndb.DateProperty(required=False)
    window_ctw_end = ndb.DateProperty(required=False)
    window_wg_start = ndb.DateProperty(required=False)
    window_wg_end = ndb.DateProperty(required=False)
    web_link = ndb.StringProperty(required=True)
    handbook_link = ndb.StringProperty(required=False)
    contact_link = ndb.StringProperty(required=False)
    contact_email = ndb.StringProperty(required=False)
    contact_phone = ndb.StringProperty(required=False)
    bumf = ndb.StringProperty(required=True)
    email_ess = ndb.StringProperty(required=False)
    email_holiday = ndb.StringProperty(required=False)
    email_pension = ndb.StringProperty(required=False)
    email_life = ndb.StringProperty(required=False)
    email_cic = ndb.StringProperty(required=False)
    email_gip = ndb.StringProperty(required=False)
    email_cp = ndb.StringProperty(required=False)
    email_dental = ndb.StringProperty(required=False)
    email_ha = ndb.StringProperty(required=False)
    email_hr = ndb.StringProperty(required=False)
    email_default = ndb.StringProperty(required=True)
    image_links = ndb.StringProperty(required=False)
    welcome_note = ndb.StringProperty(required=False)
    company_icon = ndb.StringProperty(required=False)
    company_slogan = ndb.StringProperty(required=False)
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


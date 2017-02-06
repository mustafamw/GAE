from protorpc import messages
from egb.ess.ess import Ess, EssList, EssModel, EssResponse, EssUpdated, EssUpdatedModel,EssUpdatedList
from egb.generic.ess import TitleType
from google.appengine.ext import ndb
from egb.utils.error import ErrorHelper
from egb.user.user import UserModel
from libs.parse.parse import Parse
import endpoints
    
class EssHelper(Parse):
    
    ESS_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    ESS_UPDATED_AUTH_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                             user_status=messages.IntegerField(2, variant=messages.Variant.INT32, required=True))
    
    ESS_AMEND_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                       title=messages.EnumField(TitleType, 2, required=True),
                                                       ni_no=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                       firstname=messages.StringField(4, variant=messages.Variant.STRING, required=True),
                                                       lastname=messages.StringField(5, variant=messages.Variant.STRING, required=True),
                                                       contact_no=messages.StringField(6, variant=messages.Variant.STRING, required=True),
                                                       email=messages.StringField(7, variant=messages.Variant.STRING, required=True),
                                                       address=messages.StringField(8, variant=messages.Variant.STRING, required=True),
                                                       city=messages.StringField(9, variant=messages.Variant.STRING, required=True),
                                                       county=messages.StringField(10, variant=messages.Variant.STRING, required=True),
                                                       postcode=messages.StringField(11, variant=messages.Variant.STRING, required=True),
                                                       bank_name=messages.StringField(12, variant=messages.Variant.STRING, required=True),
                                                       bank_holder_name=messages.StringField(13, variant=messages.Variant.STRING, required=True),
                                                       account_no=messages.IntegerField(14, variant=messages.Variant.INT32, required=True),
                                                       sort_code=messages.StringField(15, variant=messages.Variant.STRING, required=True))
    
    def get_ess(self, client_id, user_id):
                                           
        esss = EssModel.query(EssModel.user == ndb.Key('UserModel', client_id)).fetch()
        
        if esss:
            
            return esss
        
        raise ErrorHelper.ess_not_found()
    
    
    def construct_ess(self, esss):
        
        esssArr = []
            
        for ess in esss:
            
            ess = Ess(user_id=ess.user_id,
                      title=ess.title,
                      firstname=ess.firstname,
                      lastname=ess.lastname,
                      maiden_name=ess.maiden_name,
                      address=ess.address,
                      city=ess.city,
                      county=ess.county,
                      postcode=ess.postcode,
                      contact_no=ess.contact_no,
                      bank_holder_name=ess.bank_holder_name,
                      bank_name=ess.bank_name,
                      account_no=ess.account_no,
                      sort_code=ess.sort_code,
                      ni_no=ess.ni_no)
            
            esssArr.append(ess)
            
        return EssList(ess_list = esssArr)
    
    
    def ess_ammend_update(self, client_id, user_id, ni_no, title, firstname, lastname, contact_no, email, address, city, county, postcode, bank_name, bank_holder_name, account_no, sort_code):

        qryUser = UserModel.query(UserModel.key == ndb.Key('UserModel', client_id),
                                  UserModel.user_id == user_id).get()
        
        if qryUser:
            qryUser.email = email
            qryUser.put()
        else:
            raise ErrorHelper.user_not_found()
                                        
        qryEss = EssModel.query(EssModel.user == ndb.Key('UserModel', client_id),
                                EssModel.user_id == user_id).get()
        
        if qryEss:
            
            qryEss.ni_no = ni_no
            qryEss.title = title
            qryEss.firstname = firstname
            qryEss.lastname = lastname
            qryEss.contact_no = contact_no
            qryEss.address = address
            qryEss.city = city
            qryEss.county = county
            qryEss.postcode = postcode
            qryEss.bank_name = bank_name
            qryEss.bank_holder_name = bank_holder_name
            qryEss.account_no = account_no
            qryEss.sort_code = sort_code
            
            qryEss.put()
            
            EssUpdatedModel(ess=qryEss.key,
                            user=qryEss.user,
                            user_id=qryEss.user_id,
                            ni_no=qryEss.ni_no,
                            title=qryEss.title,
                            firstname=qryEss.firstname,
                            lastname=qryEss.lastname,
                            contact_no=qryEss.contact_no,
                            email=email,
                            address=qryEss.address,
                            city=qryEss.city,
                            county=qryEss.county,
                            postcode=qryEss.postcode,
                            bank_name=qryEss.bank_name,
                            bank_holder_name=qryEss.bank_holder_name,
                            account_no=qryEss.account_no,
                            sort_code=qryEss.sort_code).put()
            
            
            return EssResponse(message="Successfully amended")
        
        raise ErrorHelper.ess_not_found()
    
    
    def get_ess_updated(self, user_status):
        
        qryUser = UserModel.query(UserModel.status == user_status).fetch(keys_only=True)
        
        qryEssUpdated = EssUpdatedModel.query(EssUpdatedModel.user.IN(qryUser)).fetch()
        
        if qryEssUpdated:
            
            return qryEssUpdated
        
        raise ErrorHelper.ess_updated_not_found()
    

    def construct_ess_updated(self, ess_updated):
        
        ess_updatedArr = []
            
        for ess in ess_updated:
            
            submitted = self.parseDateFormatHyphen(ess.submitted)
            
            ess_update = EssUpdated(user_id=ess.user_id,
                                    title=ess.title,
                                    firstname=ess.firstname,
                                    lastname=ess.lastname,
                                    maiden_name=ess.maiden_name,
                                    address=ess.address,
                                    city=ess.city,
                                    county=ess.county,
                                    postcode=ess.postcode,
                                    contact_no=ess.contact_no,
                                    email=ess.email,
                                    bank_holder_name=ess.bank_holder_name,
                                    bank_name=ess.bank_name,
                                    account_no=ess.account_no,
                                    sort_code=ess.sort_code,
                                    ni_no=ess.ni_no,
                                    submitted=submitted)
            
            ess_updatedArr.append(ess_update)
            
        return EssUpdatedList(ess_updated_list = ess_updatedArr)
        
        



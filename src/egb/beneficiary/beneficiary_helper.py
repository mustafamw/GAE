"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 22 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from egb.generic.beneficiary import RelationshipHelper
from egb.beneficiary.beneficiary import Beneficiary
from egb.beneficiary.beneficiary import BeneficiaryModel
from protorpc import messages
from google.appengine.ext import ndb
from libs.parse.parse import Parse
import endpoints
from egb.user.user import UserModel

class BeneficiaryHelper(RelationshipHelper, Parse):
    
    BENEFICIARY_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                        relationship=messages.StringField(2, variant=messages.Variant.STRING, required=True),
                                                        firstname=messages.StringField(3, variant=messages.Variant.STRING, required=True),
                                                        lastname=messages.StringField(4, variant=messages.Variant.STRING, required=True),
                                                        dob=messages.StringField(5, variant=messages.Variant.STRING, required=True),
                                                        life_percent=messages.StringField(6, variant=messages.Variant.STRING, required=False),
                                                        pension_percent=messages.StringField(7, variant=messages.Variant.STRING, required=False))
     
    def insert_beneficiary(self, client_id, user_id, firstname, lastname, relationship, dob, pension_percent, life_percent):
        
        firstname = firstname.split(',')
        lastname = lastname.split(',')
        dob = dob.split(',')
        dob = self.parseDateList(dob)
        relationship = relationship.split(',')
        pension_percent = self.parseFloatList(pension_percent)
        life_percent = self.parseFloatList(life_percent)
        
        qryUser = UserModel.query(UserModel.key == ndb.Key('UserModel', client_id)).get().key
        
        qryBeneficiary = BeneficiaryModel.query(BeneficiaryModel.user == qryUser,
                                                BeneficiaryModel.user_id == user_id).get()
        
        if qryBeneficiary:
            qryBeneficiary.relationship = relationship
            qryBeneficiary.firstname = firstname
            qryBeneficiary.lastname = lastname
            qryBeneficiary.dob = dob
            qryBeneficiary.pension_percent = pension_percent
            qryBeneficiary.life_percent == life_percent
            qryBeneficiary.put()
            
            return Beneficiary(message="Successfully Ammended")
        
            
        BeneficiaryModel(user=ndb.Key('UserModel', client_id),
                         user_id=user_id,
                         relationship=relationship,
                         firstname=firstname,
                         lastname=lastname,
                         dob=dob,
                         pension_perecent=pension_percent,
                         life_percent=life_percent).put()
                             
        return Beneficiary(message="Successfully inserted")
            
            
    





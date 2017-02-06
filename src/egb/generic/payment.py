from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

from protorpc import messages

class PaymentType(messages.Enum):
    SALARY = 1
    BONUS = 2
    COMMISSION = 3
    MILEAGE = 4
    HEALTH_CARE = 5
    STUDENT_LOAN = 6    

   
class Payment(messages.Message):
    paymentType = messages.EnumField(PaymentType, 1, required=False)
    hours = messages.FloatField(2, required=False)
    rate = messages.FloatField(3, required=False)
    gross_cost = messages.FloatField(4, required=False)
                                     
                                     
class PaymentModel(ndb.Model):
    paymentType = msgprop.EnumProperty(PaymentType, required=True, indexed=True)
    hours = ndb.FloatProperty(required=False)  
    rate = ndb.FloatProperty(required=True)
    gross_cost = ndb.FloatProperty(required=True)


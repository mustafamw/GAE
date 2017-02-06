from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

from protorpc import messages

class DeductionType(messages.Enum):
    LEISURE = 1
    RANDOM = 2   

   
class Deduction(messages.Message):
    deductionType = messages.EnumField(4, required=False)
    gross_cost = messages.FloatField(7, required=False)
                                     
                                     
class DeductionModel(ndb.Model):
    deductionType = msgprop.EnumProperty(DeductionType, required=True, indexed=True)
    gross_cost = ndb.FloatProperty(required=True)
from protorpc import messages
from egb.employee.employee import SalaryTrs
from egb.cic.cic import CicTrs
from egb.pmi.pmi import PmiTrs
from egb.pension.pension import PensionTrs
from egb.life.life import LifeTrs
from egb.cashplan.cashplan import CashplanTrs
from egb.gip.gip import GipTrs
from egb.dental.dental import DentalTrs

class TotalReward(messages.Message):
    user_id = messages.IntegerField(1, required=False)
    salary = messages.MessageField(SalaryTrs, 2, required=False)
    ccv = messages.FloatField(4, required=False)
    ctw = messages.FloatField(5, required=False)
    cic = messages.MessageField(CicTrs, 6, required=False)
    gip = messages.MessageField(GipTrs, 7, required=False)
    pmi = messages.MessageField(PmiTrs, 8, required=False)
    pension = messages.MessageField(PensionTrs, 9, required=False)
    life = messages.MessageField(LifeTrs, 10, required=False)
    dental = messages.MessageField(DentalTrs, 11, required=False)
    cashplan = messages.MessageField(CashplanTrs, 12, required=False)
    
    
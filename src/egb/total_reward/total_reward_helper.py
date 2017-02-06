from google.appengine.ext import ndb
from protorpc import messages

from egb.total_reward.total_reward import TotalReward
from egb.employee.employee import SalaryTrs
from egb.cic.cic import CicTrs
from egb.pmi.pmi import PmiTrs
from egb.pension.pension import PensionTrs
from egb.life.life import LifeTrs
from egb.cashplan.cashplan import CashplanTrs
from egb.gip.gip import GipTrs
from egb.dental.dental import DentalTrs

from egb.employee.employee import EmployeeModel
from egb.pension.pension import PensionModel
from egb.ccv.ccv import CcvModel
from egb.life.life import LifeModel
from egb.pmi.pmi import PMIModel
from egb.gip.gip import GipModel
from egb.dental.dental import DentalModel
from egb.ctw.ctw import CtwModel
from egb.cic.cic import CicModel
from egb.cashplan.cashplan import CashplanModel


import endpoints
    
class TotalRewardHelper:
    
    TRS_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    def get_total_reward(self, client_id, user_id):                                           
        
        qryEmployee = EmployeeModel.query(EmployeeModel.user==ndb.Key('UserModel',client_id), EmployeeModel.user_id==user_id).get()
        qryPension = PensionModel.query(PensionModel.user==ndb.Key('UserModel',client_id), PensionModel.user_id == user_id).get()
        qryCcv = CcvModel.query(CcvModel.user==ndb.Key('UserModel',client_id), CcvModel.user_id == user_id).get()
        qryLife = LifeModel.query(LifeModel.user==ndb.Key('UserModel',client_id), LifeModel.user_id == user_id).get()
        qryPmi = PMIModel.query(PMIModel.user==ndb.Key('UserModel',client_id), PMIModel.user_id == user_id).get()
        qryGip = GipModel.query(GipModel.user==ndb.Key('UserModel',client_id), GipModel.user_id == user_id).get()
        qryDental = DentalModel.query(DentalModel.user==ndb.Key('UserModel',client_id), DentalModel.user_id == user_id).get()
        qryCtw = CtwModel.query(CtwModel.user==ndb.Key('UserModel',client_id), CtwModel.user_id == user_id).get()
        qryCic = CicModel.query(CicModel.user==ndb.Key('UserModel',client_id), CicModel.user_id == user_id).get()
        qryCashplan = CashplanModel.query(CashplanModel.user==ndb.Key('UserModel',client_id), CashplanModel.user_id == user_id).get()
    
        
        salary = 0.00
        bonus = 0.00
        commission = 0.00
        tax_rate = 0.00
        pension_employer_contribution = 0.00
        pension_employer_contribution_percentage = 0.00
        life_premium_core = 0.00
        life_core_multiple = 0.00
        cashplan_premium_who = 0.00
        cashplan_premium_core = 0.00
        cashplan_premium_cover_level = 0.00
        pmi_premium_who = 0.00
        pmi_premium_core = 0.00
        pmi_premium_cover_level = 0.00
        gip_premium_core = 0.00
        cic_premium_core = 0.00
        cic_core_multiple = 0.00
        ctw = 0.00
        ccv = 0.00
        
        if qryEmployee:
            salary = qryEmployee.salary
            bonus = qryEmployee.bonus
            commission = qryEmployee.commission
            
        if salary >= 50000:
            tax_rate = 0.42
        else:
            tax_rate = 0.32
               
        if qryPension:
            pension_employer_contribution = qryPension.employer_contribution
            pension_employer_contribution_percentage = qryPension.employer_contribution_percent
            
        if qryLife:
            life_premium_core = qryLife.gross_cost
            life_core_multiple = qryLife.flex_multiple
            
        if qryCashplan:
            cashplan_premium_who = qryCashplan.premium_who
            cashplan_premium_core = qryCashplan.premium_core
            cashplan_premium_cover_level = qryCashplan.premium_cover_level
            
        if qryPmi:
            pmi_premium_who = qryPmi.premium_who
            pmi_premium_core = qryPmi.premium_core
            pmi_premium_cover_level = qryPmi.premium_cover_level
            
        if qryDental:
            dental_premium_who = qryDental.premium_who
            dental_premium_core = qryDental.premium_core
            dental_premium_cover_level = qryDental.premium_cover_level

            
        if qryGip:
            gip_premium_core = qryGip.premium_core
            
        if qryCic:
            cic_premium_core = qryCic.gross_cost
            cic_core_multiple = qryCic.flex_multiple
        
        if qryCtw:
            ctw = qryCtw.gross_cost * tax_rate
            
        if qryCcv:
            ccv = qryCcv.contribution * tax_rate
        
        
        total_rewards = TotalReward(user_id=user_id,
                                    salary=SalaryTrs(salary=salary,
                                                  bonus=bonus,
                                                  commission=commission),
                                    ctw=ctw,
                                    cic=CicTrs(premium_core=cic_premium_core,
                                            core_multiple=cic_core_multiple),
                                    pmi=PmiTrs(premium_who=pmi_premium_who,
                                            premium_cover_level=pmi_premium_cover_level,
                                            premium_core=pmi_premium_core),
                                    cashplan=CashplanTrs(premium_who=cashplan_premium_who,
                                                      premium_cover_level=cashplan_premium_cover_level,
                                                      premium_core=cashplan_premium_core),
                                    dental=DentalTrs(premium_who=dental_premium_who,
                                                    premium_cover_level=dental_premium_cover_level,
                                                    premium_core=dental_premium_core),
                                    gip=GipTrs(premium_core=gip_premium_core),
                                    ccv=ccv,
                                    life=LifeTrs(premium_core=life_premium_core,
                                              core_multiple=life_core_multiple),
                                    pension=PensionTrs(employer_contribution=pension_employer_contribution,
                                                    employer_contribution_percentage=pension_employer_contribution_percentage))

        return total_rewards
    
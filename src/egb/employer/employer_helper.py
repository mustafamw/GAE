from protorpc import messages
from egb.employer.employer import Employer, EmployerList, EmployerModel, EmployerVariation
from egb.user.user import UserModel
from google.appengine.ext import ndb
from libs.parse.parse import Parse
from egb.utils.error import ErrorHelper
import endpoints
    
class EmployerHelper(Parse):
    
    EMPLOYER_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    def get_variation(self, variation):
            
        if variation == 1:
            return EmployerVariation.ONE
        elif variation == 2:
            return EmployerVariation.TWO
        elif variation == 3:
            return EmployerVariation.THREE
        elif variation == 4:
            return EmployerVariation.FOUR
        elif variation == 5:
            return EmployerVariation.FIVE
    
        return EmployerVariation.ONE
    
    
    def get_employer(self, client_id, user_id):

        qryUser = UserModel.query(UserModel.key == ndb.Key('UserModel', client_id)).get().employer
        
        if qryUser:     
                                
            qryEmployer = EmployerModel.query(ancestor=qryUser).fetch()
            
            if qryEmployer:
                
                return qryEmployer
            
            raise ErrorHelper.employer_not_found()
        
        raise ErrorHelper.user_not_found()()
    


    def construct_employer(self, employers):
        
        employersArr = []
        
        for employer in employers:
            
            window_life_start = self.parseDateFormatDots(employer.window_life_start)
            window_life_end = self.parseDateFormatDots(employer.window_life_end)
            window_CIC_start = self.parseDateFormatDots(employer.window_cic_start)
            window_CIC_end = self.parseDateFormatDots(employer.window_cic_end)
            window_PMI_start = self.parseDateFormatDots(employer.window_pmi_start)
            window_PMI_end = self.parseDateFormatDots(employer.window_pmi_end)
            window_CTW_start = self.parseDateFormatDots(employer.window_ctw_start)
            window_CTW_end = self.parseDateFormatDots(employer.window_ctw_end)
            window_WG_start = self.parseDateFormatDots(employer.window_wg_start)
            window_WG_end = self.parseDateFormatDots(employer.window_wg_end)
            
            employer = Employer(name=employer.name,
                                variation=employer.variation,
                                window_life_start=window_life_start,
                                window_life_end=window_life_end,
                                window_CIC_start=window_CIC_start,
                                window_CIC_end=window_CIC_end,
                                window_PMI_start=window_PMI_start,
                                window_PMI_end=window_PMI_end,
                                window_CTW_start=window_CTW_start,
                                window_CTW_end=window_CTW_end,
                                window_WG_start=window_WG_start,
                                window_WG_end=window_WG_end,
                                web_link=employer.web_link,                            
                                handbook_link=employer.handbook_link,
                                contact_link=employer.contact_link,
                                contact_email=employer.contact_email,
                                contact_phone=employer.contact_phone,
                                bumf=employer.bumf,
                                email_ESS=employer.email_ess,
                                email_holiday=employer.email_holiday,
                                email_pension=employer.email_pension,
                                email_life=employer.email_life,
                                email_CIC=employer.email_cic,
                                email_GIP=employer.email_gip,                            
                                email_CP=employer.email_cp,
                                email_dental=employer.email_dental,
                                email_HA=employer.email_ha,
                                email_HR=employer.email_hr,
                                email_default=employer.email_default,
                                image_links=employer.image_links,
                                welcome_note=employer.welcome_note,
                                company_icon=employer.company_icon,
                                company_slogan=employer.company_slogan)
            
            employersArr.append(employer) 
        
        return EmployerList(employer_list=employersArr)
        

from protorpc import messages
from egb.health_assessment.health_assessment import HealthAssessment, HealthAssessmentList, HealthAssessmentModel
from google.appengine.ext import ndb
from egb.utils.error import ErrorHelper
import endpoints
    
class HealthAssessHelper:
    
    HEALTHASSESS_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))
    
    def get_health_assessment(self, client_id, user_id):
                                           
        health_assessments = HealthAssessmentModel.query(HealthAssessmentModel.user == ndb.Key('UserModel', client_id)).fetch()
                                                         
        if health_assessments:

            return health_assessments
        
        raise ErrorHelper.ha_not_found()
    
    
    def construct_health_assessment(self, health_assessments):
        
        health_assessmentsArr = []
        
        for health_assessment in health_assessments:
            
            health_assessment = HealthAssessment(user_id=health_assessment.user_id,
                                                 provider_name=health_assessment.provider_name,
                                                 product_type=health_assessment.product_type,
                                                 product_variation=health_assessment.product_variation,
                                                 flexible=health_assessment.flexible,
                                                 who=health_assessment.who,
                                                 cover_level=health_assessment.cover_level,
                                                 premium_core=health_assessment.premium_core,
                                                 premium_flex=health_assessment.premium_flex,
                                                 gross=health_assessment.gross_cost,
                                                 net=health_assessment.net)
            
            health_assessmentsArr.append(health_assessment)
            
        return HealthAssessmentList(health_assessment_list = health_assessmentsArr)

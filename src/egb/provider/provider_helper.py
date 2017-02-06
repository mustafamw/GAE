from protorpc import messages
from egb.provider.provider import ProviderModel
from egb.provider.provider import Provider, ProviderList
from egb.generic.product import ProductTypeHelper
from egb.utils.error import ErrorHelper
import endpoints
    
class ProviderHelper():    
    
    PROVIDER_CONTAINER = endpoints.ResourceContainer( provider_name=messages.StringField(1, variant=messages.Variant.STRING, required=True),
                                                  product_type=messages.StringField(2, variant=messages.Variant.STRING, required=True),
                                                  product_variation=messages.StringField(3, variant=messages.Variant.STRING, required=True))
    

    def get_provider(self, provider_name, product_type, product_variation):
                                           
        providers = ProviderModel.query(ProviderModel.provider_name == provider_name,
                                        ProviderModel.product_type == ProductTypeHelper.get_product_type(product_type),
                                        ProviderModel.product_variation == ProductTypeHelper.get_product_variation(product_variation)).fetch()
                                        
        if providers:

            return providers
        
        raise ErrorHelper.provider_not_found()
    

    def construct_provider(self, providers):
        
        providersArr = []
        
        for provider in providers:
            
            provider = Provider(provider_name=provider.provider_name,
                    product_type=provider.product_type,
                    product_variation=provider.product_variation,
                    web_link=provider.web_link,
                    icon_link=provider.icon_link,
                    bumf=provider.bumf)
            
            providersArr.append(provider) 
            
        return ProviderList(provider_list = providersArr)

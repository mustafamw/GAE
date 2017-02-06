from protorpc import messages

class ProductType(messages.Enum):
    LIFE = 1
    PENSION = 2
    Cic = 3
    Gip = 4
    PMI = 5
    CP = 6
    DENTAL = 7
    HEALTH = 8
    Ccv = 9
    Ctw = 10
    CAR = 11
    
class ProductVariation(messages.Enum):
    DEFAULT = 1
    CAR_ALLOWANCE = 2
    
    
class ProductTypeHelper():
    
    @staticmethod
    def get_product_type(product_type):
            
        product_type = int(product_type)    
            
        if product_type == 1:
            return ProductType.LIFE
        elif product_type == 2:
            return ProductType.PENSION
        elif product_type == 3:
            return ProductType.Cic
        elif product_type == 4:
            return ProductType.Gip
        elif product_type == 5:
            return ProductType.PMI
        elif product_type == 6:
            return ProductType.CP
        elif product_type == 7:
            return ProductType.DENTAL
        elif product_type == 8:
            return ProductType.HEALTH
        elif product_type == 9:
            return ProductType.Ccv
        elif product_type == 10:
            return ProductType.Ctw
        elif product_type == 11:
            return ProductType.CAR
        
        return ProductType.LIFE
    
    
    @staticmethod
    def get_product_variation(product_variation):
            
        product_variation = int(product_variation)    
            
        if product_variation == 1:
            return ProductVariation.DEFAULT
        elif product_variation == 2:
            return ProductVariation.CAR_ALLOWANCE
        
        return ProductVariation.DEFAULT

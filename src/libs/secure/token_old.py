import random
import string
import logging

from egb.utils.helper import UtilsHelper

from egb.secure import token

DEBUG = logging.getLogger().isEnabledFor(UtilsHelper.get_level())

# http://pythonhosted.org/passlib/lib/passlib.hash.html
from passlib.handlers.sha2_crypt import sha256_crypt

def get_token():
        
        myToken = token.generate_token()
        
        if DEBUG:
            logging.info("token " +myToken)
            
        return myToken

def generate_token():
    
    myHash = sha256_crypt.encrypt("password1", rounds=200000, salt_size=16)
        
    if DEBUG:
        logging.debug("in get_token")
        logging.info('hash ' +myHash)
        logging.info('resolved = ' + str(sha256_crypt.verify("password1", myHash)))
        
    size=12 
    chars=string.ascii_uppercase + string.digits
        
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
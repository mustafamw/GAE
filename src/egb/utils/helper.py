# https://cloud.google.com/appengine/articles/logging
import logging
import timeit

LEVEL = logging.DEBUG

class UtilsHelper():
    
    @staticmethod
    def get_elapsed(message, then):
        
        now = timeit.default_timer()        
        elapsed = (now - then)

        logging.info(message + ' :Elapsed: ' +str(elapsed))
        
    @staticmethod
    def get_level():
        return LEVEL


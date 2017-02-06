"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 9 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

import datetime, time

class DateTime():
    
    @staticmethod 
    def addDateTimeMinute(value):
        
        added = datetime.timedelta(minutes = value)
        
        return added
    
    @staticmethod 
    def getCurrentDateTime():
    
        currrent_datetime = datetime.datetime.now()
        
        return currrent_datetime
    
    
    @staticmethod 
    def getCurrentUnixDateTime():
        
        currrent_datetime_unix = time.time()
        
        return currrent_datetime_unix
  
  
  
    @staticmethod 
    def getUnixToDateTime(unix):
        
        date = datetime.datetime.utcfromtimestamp(unix)
      
        return date
    
    
    @staticmethod
    def getDateYear(date):
        year = date.year
        return year






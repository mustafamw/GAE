"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 7 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""
from libs.dateutil.parser import parse

class Parse():
    
    def parseDate(self, date):
        date = parse(date, dayfirst=True)
        return date
    
    def parseDateList(self, listDates):
        datesArr = []
        for date in listDates:
            date = self.parseDate(date)
            datesArr.append(date)
        return datesArr
    
    def parseDateFormatHyphen(self, date):
        date = date.strftime('%Y-%m-%d')
        return date
    
    def parseDateTimeFormatHyphen(self, date):
        date = date.strftime('%Y-%m-%dT%H:%M:%S')
        return date
    
    def parseDateFormatSlash(self, date):
        date = date.strftime('%d/%m/%Y')
        return date
    
    def parseDateFormatDots(self, date):
        date = date.strftime('%d.%m.%Y')
        return date
    
    def parseEmail(self, email):
        pass
    
    def stringToLower(self, string):
        return string.lower()

    def stringToUpper(self, string):
        return string.upper()
    
    def parseInteger(self, integer):
        return int(integer)
    
    def parseFloat(self, floatVal):
        return float(floatVal)
    
    def parseFloatList(self, floatList):
        floatArr = []
        if "," in floatList:
            floatList = floatList.split(',')
            for floatVal in floatList:
                floatVal = self.parseFloat(floatVal)
                floatArr.append(floatVal)
        else:
            floatVal = self.parseFloat(floatList)
            floatArr.append(floatVal)
        
        return floatArr
        
            
        
    
    






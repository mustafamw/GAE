"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 27 Oct 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from google.appengine.ext import ndb

class FloodModel(ndb.Model):
    ip_address = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    attempt = ndb.IntegerProperty(required=True)
    expiry = ndb.DateTimeProperty(auto_now_add=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)








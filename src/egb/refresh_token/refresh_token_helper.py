"""
Copyright (C) 2016 EG Benefits. All rights reserved.
Unauthorised copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Created on 8 Nov 2016

@Mustafa Mohamed: mustafa.mohamed@ernestgrant.com
"""

from protorpc import messages
import endpoints

REFRESH_TOKEN_CONTAINER = endpoints.ResourceContainer(token=messages.StringField(1, variant=messages.Variant.STRING, required=True))





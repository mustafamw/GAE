from protorpc import messages

class LoginBody(messages.Message):
    username = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)
    

class LoginDesktopResponse(messages.Message):
    token = messages.StringField(1, required=True)
    expiry = messages.IntegerField(2, required=True)
    

class LoginMobileResponse(messages.Message):
    token = messages.StringField(1, required=True)
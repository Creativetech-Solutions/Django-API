import re
from api.Custom.Token import *
from django.conf import settings
class Verification():
    def apiToken(self, apikey):
        if apikey is None:
            return False

        if(apikey.find('.') == -1):
            if settings.API['key'] == apikey:
                return True
            else:
                return False
        else:
            key_and_token = re.split(',|\.',apikey)
            if settings.API['key'] == key_and_token[0]:
                return True
            else:
                return False

    def accessToken(self, token, user_id=0):
        key_and_token = re.split(',|\.',token)
        t = Token()
        response = t.isValidToken(key_and_token[1], user_id)
        return response

    def verifyPermissions(self, user=None, method=None):
        if method is not None:
            if method == "WLInvoices" and 'user_type' in user and user['user_type'] == 'White Label Partner':
                return True
            elif method == "staffs" and 'user_type' in user and user['user_type'] == 'Operational':
                return True
            else:
                return False
        else:
            return True

    def checkUserType(self, userType):
        if userType is not None and userType !="" and (userType == '1' or userType == '8' or userType == '9' or userType == '3'):
            return True
        else:
            return False
import psycopg2
from django.db import connections, transaction, DatabaseError, IntegrityError
import json
# import secrets
from api.Custom.Dict import *
from datetime import datetime, timedelta
import random
class Token(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
	    self.data = []
	    self.cursor = connections['default'].cursor()

    # create user access toke by user id
    def createToken(self, staff):
    	# delete token if exist
	    userId = staff['staff_and_agents_id']
	    if staff['type'] == '8':
	    	userType = 'Wholesale Partner'
	    elif staff['type'] == '9':
	    	userType = 'White Label Partner'
	    elif staff['type'] == '3':
	    	userType = 'Operational'
	    elif staff['type'] == '1':
	    	userType = 'Commission Partner'
	    else:
	    	userType = ""

	    self.deleteToken(userId, userType)
	    # token = secrets.token_hex(nbytes=32)
	    token = hex(random.getrandbits(256))
	    expireTime = datetime.now() + timedelta(hours=12)
	    # refreshToken = secrets.token_hex(nbytes=32)
	    refreshToken = hex(random.getrandbits(256))
	    refTokenExpTime = datetime.now() + timedelta(days=60)
	    resp = self.saveToken(
	    userId,
	    userType,
	    str(token),
	    expireTime,
	    refreshToken,
	    refTokenExpTime," "
        )
	    return resp
        
    def saveToken(self, userId,userType, token, expireTime, refreshToken, refTokenExpTime, permissionIds):
	    #return expireTime
	    cursor = self.cursor
	    cursor.execute('SELECT access_token FROM tokens WHERE access_token = %s', [token])
	    old_token = self.dictfetchOne(cursor)
	    if 'access_token' in old_token: # token already exist create again
	    	self.createToken(userId, userType)

	    cursor = self.cursor
	    cursor.execute('INSERT INTO tokens (access_token, refresh_token, access_token_exp_time, refresh_token_exp_time, user_id, user_type,permission_ids) VALUES (%s, %s, %s, %s, %s, %s, %s)',[token, refreshToken, expireTime, refTokenExpTime, userId, userType, permissionIds])
	    return {'tokens':{'access_token':token, 'refresh_token':refreshToken}, 'user_type':userType}

    def isValidToken(self, token, user_id):
	    cursor = self.cursor
	    cursor.execute('SELECT id,user_type,permission_ids,access_token_exp_time FROM tokens WHERE access_token = %s AND user_id = %s'
		               , (token, int(user_id)))
	    token = self.dictfetchOne(cursor)
	    if 'id' not in token:
	    	return {'isSuccess': False, 'data': 'Access Token Is Not Valid', 'errors': ''}
	    else:
		    expTime = datetime.strptime(token['access_token_exp_time'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f')
		    present = (datetime.now()).strftime('%Y-%m-%d %I:%M:%S')
		    if expTime < present:
		        return {'isSuccess': False,
		                'errors': 'Access Token Is Expired', 'data': ''}
		    else:
		        return {'isSuccess': True, 'data': token, 'errors': ''}

    def deleteToken(self, userId, userType):
    	cursor = self.cursor
    	cursor.execute('DELETE FROM tokens WHERE user_id = %s AND user_type = %s',[int(userId), userType])
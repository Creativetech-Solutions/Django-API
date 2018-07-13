import random
import hashlib, binascii
class Dict(object):
    def __init__(self):
        self.data = []

    def dictfetchOne(self, cursor):
        fields = [field[0] for field in cursor.description]
        vals = cursor.fetchone()
        if not vals:
            return {}
        return dict(zip(fields, vals))

    def dictfetchall(self, cursor):
        fields = [field[0] for field in cursor.description]
        return [
            dict(zip(fields, row))
            for row in cursor.fetchall()
        ]

    def generatePassword(self, password, salt=""):
        if salt == "":
            salt = hex(random.getrandbits(128)).encode('utf-8')
        else:
            salt = salt.encode('utf-8')
            
        password = password.encode('utf-8')
        # password = hex(int(password)).encode()
        # dk = hashlib.pbkdf2_hmac('sha256',b'mypass',salt, 1000000)
        dk = hashlib.pbkdf2_hmac('sha256',password,salt, 1000000)
        return {'salt':salt.decode("utf-8"), 'pass':binascii.hexlify(dk).decode("utf-8")}
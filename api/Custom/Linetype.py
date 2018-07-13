import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Linetype(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def getLineTypes(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT * FROM line_type"
        cursor.execute(query)
        line_types = self.dictfetchall(cursor)
        return line_types
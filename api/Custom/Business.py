import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Business(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def getBusinessTypes(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT * FROM business_type ORDER BY type_description"
        cursor.execute(query)
        businesstypes = self.dictfetchall(cursor)
        return businesstypes
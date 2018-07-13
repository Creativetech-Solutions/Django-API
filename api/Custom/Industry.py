import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Industry(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def getIndustries(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT * FROM prospect_industries ORDER BY prospect_industries"
        cursor.execute(query)
        industries = self.dictfetchall(cursor)
        return industries
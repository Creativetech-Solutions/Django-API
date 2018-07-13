import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Country(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def getCountries(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT * FROM cdc ORDER BY country"
        cursor.execute(query)
        countries = self.dictfetchall(cursor)
        return countries
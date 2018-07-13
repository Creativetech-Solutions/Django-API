import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Position(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def getPositions(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT * FROM company_position"
        cursor.execute(query)
        positions = self.dictfetchall(cursor)
        return positions
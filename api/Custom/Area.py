import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Area(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []
    
    def getAreaNames(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT na.* FROM national_area_name na"
        variables = []
        if 'area_code' in data:
            query += " INNER JOIN national_phone_codes np ON na.national_area_name_id = np.national_area_name_id AND np.area_code LIKE %s"
            variables.append('%'+str(data['area_code'])+'%');

        query +=" ORDER BY na.area_name"

        if 'area_code' in data:
            query += " LIMIT 1"

        cursor.execute(query,variables)
        areanames = self.dictfetchall(cursor)
        return areanames
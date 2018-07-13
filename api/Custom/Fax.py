import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Fax(Dict):
    def __init__(self):
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM uf1_users")
        # records = cursor.fetchall()
        # pprint.pprint(records)
        self.data = []

    def getFaxCharges(self, data):
        staff_id = data['staff_id']
        variables = []
        cursor = connections['ufone_db'].cursor()
        query = "SELECT fd.*, clients.client_id, clients.client_name FROM clients INNER JOIN faxware_cdr_view fd ON(fd.client_id = clients.client_id AND clients.staff_and_agents_id = %s)"
        variables.append(staff_id)
        if 'client_id' in data and data['client_id'] != "":
            query += " WHERE clients.client_id = %s"
            variables.append(data['client_id'])

        query += " ORDER BY clients.client_id"
        
        # if limit != "":
        #     query += " LIMIT %s"
        #     variables.append(limit)

        cursor.execute(query,tuple(variables))
        phones = self.dictfetchall(cursor)
        return phones
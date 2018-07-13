import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Tollfree(Dict):
    def __init__(self):
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM uf1_users")
        # records = cursor.fetchall()
        # pprint.pprint(records)
        self.data = []

    def getTollFreeAll(self, data):
        staff_id = data['staff_id']
        variables = []

        cursor = connections['ufone_db'].cursor()
        query = "SELECT cd.*, clients.client_id, clients.client_name FROM clients INNER JOIN ana_tollfree_all cd ON(cd.client_id = clients.client_id AND clients.staff_and_agents_id = %s)"
        variables.append(staff_id)
        if 'client_id' in data and data['client_id'] != "":
            query += " WHERE clients.client_id = %s"
            variables.append(data['client_id'])

        query += " ORDER BY clients.client_id"
        
        # if limit != "":
        #     query += " LIMIT %s"
        #     variables.append(limit)

        cursor.execute(query,tuple(variables))
        tollfree = self.dictfetchall(cursor)
        return tollfree

    
    def getTollFreeCalls(self, data):
        staff_id = data['staff_id']
        variables = []

        cursor = connections['ufone_db'].cursor()
        query = "SELECT cd.*, clients.client_id, clients.client_name FROM clients INNER JOIN toll_free_cdr_view cd ON(cd.client_id = clients.client_id AND clients.staff_and_agents_id = %s)"
        variables.append(staff_id)
        if 'client_id' in data and data['client_id'] != "":
            query += " WHERE clients.client_id = %s"
            variables.append(data['client_id'])

        query += " ORDER BY clients.client_id"
        
        # if limit != "":
        #     query += " LIMIT %s"
        #     variables.append(limit)

        cursor.execute(query,tuple(variables))
        tollfree = self.dictfetchall(cursor)
        return tollfree

    def getTollFree(self, data):
        variables = [data['client_id']]
        staff_id = data['staff_id']
        cursor = connections['ufone_db'].cursor()
        query = ("SELECT *, CASE WHEN line_type_id = 5 THEN 'Active'WHEN line_type_id = 6 "
            "THEN 'Disabled'WHEN line_type_id = 7 THEN 'Inactive' ELSE  '' END AS line_status from test.client_toll_free WHERE client_id = %s")

        if 'client_toll_free_id' in data:
            query += " AND client_toll_free_id = %s"
            variables.append(data['client_toll_free_id'])

        cursor.execute(query,variables)
        toll_free = self.dictfetchall(cursor)
        return toll_free


    def createTollfree(self, data):
        cursor = connections['ufone_db'].cursor()
        tollfree = data['data']
        variables = []
        fields = [
        {'field':'toll_free_number', 'type':'varchar'},{'field':'national_area_name_id', 'type':'int'},
        {'field':'line_type_id', 'type':'int'}, {'field':'is_mobile', 'type':'bool'}, 
        {'field':'local_term_phone_rate', 'type':'double'},{'field':'national_term_phone_rate', 'type':'double'},
        {'field':'cellphone_term_phone_rate', 'type':'double'},{'field':'local_term_cell_rate', 'type':'double'},
        {'field':'national_term_cell_rate', 'type':'double'}, {'field':'cellphone_term_cell_rate', 'type':'double'},
        {'field':'activation_date', 'type':'date'}, {'field':'terminating_number', 'type':'varchar'},
        {'field':'cancelled_date', 'type':'date'}, {'field':'min_charge', 'type':'bool'},{'field':'minimum_fee', 'type':'double'}
        ]

        # try:
        if 'client_toll_free_id' in tollfree and tollfree['client_toll_free_id'] != "":
            query = ""
            for index in fields:
                if index['field'] in tollfree:
                    if query == "":
                        query = "UPDATE test.client_toll_free SET "+index['field']+" = %s"
                    else:
                        query += ", "+index['field']+" = %s"
                    variables.append(tollfree[index['field']])

            query += " WHERE client_toll_free_id = %s"
            variables.append(tollfree['client_toll_free_id'])
            cursor.execute(query,variables)
            return {'tollfree_updated':True}
        else:
            query = "INSERT INTO test.client_toll_free (client_id"
            variables.append(data['client_id']);
            values = ") VALUES (%s"
            for index in fields:
                if index['field'] in tollfree:
                    # if ((contact[index['field']] is None or contact[index['field']] == '') and index['type'] == 'date'):
                    # contact[index['field']] = 'NULL'
                    query += ", "+index['field']
                    values += ", %s"
                    variables.append(tollfree[index['field']])

            query += values + ')'
            cursor.execute(query,variables)
            return {'tollfree_created':True}
        # except:
        #     return {'contact_created':False}




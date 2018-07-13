import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Phone(Dict):
    def __init__(self):
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM uf1_users")
        # records = cursor.fetchall()
        # pprint.pprint(records)
        self.data = []

    def getPhones(self, data):
        staff_id = data['staff_id']
        variables = []

        cursor = connections['ufone_db'].cursor()
        query = "SELECT cd.*, clients.client_id, clients.client_name FROM clients INNER JOIN ana_phone_summary_view cd ON(cd.client_id = clients.client_id AND clients.staff_and_agents_id = %s)"
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

    def getPhoneCalls(self, data):
        staff_id = data['staff_id']
        variables = []
        cursor = connections['ufone_db'].cursor()
        query = "SELECT cd.*, clients.client_id, clients.client_name FROM clients INNER JOIN clear_cdr cd ON(cd.client_id = clients.client_id AND clients.staff_and_agents_id = %s)"
        variables.append(staff_id)
        if 'client_id' in data and data['client_id'] != "":
            query += " WHERE clients.client_id = %s"
            variables.append(data['client_id'])

        query += " ORDER BY cd.date_time DESC"
        
        # if limit != "":
        #     query += " LIMIT %s"
        #     variables.append(limit)

        cursor.execute(query,tuple(variables))
        phones = self.dictfetchall(cursor)
        return phones

    def getClientPhones(self, data):
        variables = [data['client_id']]
        staff_id = data['staff_id']
        cursor = connections['ufone_db'].cursor()
        query = ("SELECT cp.*, (SELECT area_name FROM national_area_name WHERE national_area_name_id = cp.national_area_name_id  ) as national_area_name"
        ", (SELECT line_type_description FROM line_type WHERE line_type_id = cp.line_type_id  ) as line_type"
        " from test.client_to_phone cp WHERE cp.client_id = %s")

        if 'phone_id' in data:
            query += " AND cp.client_to_phone_id = %s"
            variables.append(data['phone_id'])

        query += " ORDER BY cp.line_type_id DESC"
        
        cursor.execute(query,variables)
        clientphones = self.dictfetchall(cursor)
        return clientphones

    def getMobiles(self, data):
        variables = [data['client_id']]
        staff_id = data['staff_id']
        cursor = connections['ufone_db'].cursor()
        query = ("SELECT cp.*, (SELECT area_name FROM national_area_name WHERE national_area_name_id = cp.national_area_name_id  ) as national_area_name"
            ", (SELECT mobile_plan_name FROM mobile_plan WHERE mobile_plan_id = cp.mobile_plan_id  ) as mobile_plan_name"
        ", (SELECT line_type_description FROM line_type WHERE line_type_id = cp.line_type_id  ) as line_type"
        " from test.client_to_phone cp WHERE cp.client_id = %s")

        if 'mobile_id' in data:
            query += " AND cp.client_to_phone_id = %s"
            variables.append(data['mobile_id'])

        query += " AND cp.line_type_id IN (8, 9, 10, 11) ORDER BY cp.line_type_id DESC"
        
        cursor.execute(query,variables)
        clientmoibles = self.dictfetchall(cursor)
        return clientmoibles

    def createPhones(self, data):
        cursor = connections['ufone_db'].cursor()
        phone = data['data']
        variables = [data['client_id']]
        fields = [{'field':'calling_number', 'type':'varchar'},{'field':'linked_to_number', 'type':'varchar'},{'field':'client_line_rent', 'type':'double'},
        {'field':'national_area_name_id','type':'int'}, {'field':'line_type_id', 'type':'int'},{'field':'activated_date', 'type':'date'},
        {'field':'description', 'type':'varchar'}, {'field':'cancelled_date', 'type':'date'},{'field':'ucs_job_id', 'type':'int'},
        {'field':'mobile_plan_id', 'type':'int'}, {'field':'scource_telecom', 'type':'bool'},{'field':'mobile_owners_name', 'type':'varchar'},
        {'field':'mobile_group_plan_id', 'type':'int'}]

        #try:
        if 'client_to_phone_id' in phone and phone['client_to_phone_id'] != "":
            query = ""
            for index in fields:
                if index['field'] in phone:
                    if query == "":
                        query = "UPDATE test.client_to_phone SET "+index['field']+" = '"+phone[index['field']]+"'"
                    else:
                        query += ", "+index['field']+" = '"+phone[index['field']]+"'"

            query += " WHERE client_to_phone_id = "+phone['client_to_phone_id']
            cursor.execute(query)
            return {'phone_updated':True}
        else:
            query = "INSERT INTO test.client_to_phone (client_id"
            values = ") VALUES (%s"
            for index in fields:
                if index['field'] in phone:
                    # if ((contact[index['field']] is None or contact[index['field']] == '') and index['type'] == 'date'):
                    # contact[index['field']] = 'NULL'
                    query += ", "+index['field']
                    values += ", %s"
                    variables.append(phone[index['field']])

            query += values + ')'
            cursor.execute(query,variables)
            return {'phone_created':True}
        # except:
        #     return {'contact_created':False}


import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Staff(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def getAllStaffs(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT staff_and_agents_id, staff_agent_name FROM staff_and_agents"
        variables = []
        if 'search_str' in data:
            query += (" WHERE staff_agent_name ILIKE %s or CAST(staff_and_agents_id AS TEXT) LIKE %s"
                " or phone LIKE %s or fax LIKE %s or email ILIKE %s or postal_address_1 ILIKE %s or "
                " postal_address_2 ILIKE %s or postal_address_3 ILIKE %s or notes ILIKE %s or contact ILIKE %s")
            variables.extend(10 * ['%'+data['search_str']+'%'])

        query += " ORDER BY staff_agent_name"

        if 'limit' in data and data['limit'] != "":
            query += " LIMIT %s"
            variables.append(data['limit'])#, 

        cursor.execute(query,variables)
        staffs = self.dictfetchall(cursor)
        return staffs

    def getStaff(self, data):
        variables = []
        cursor = connections['ufone_db'].cursor()
        if 'partner_id' in data:
            Q = "SELECT * FROM staff_and_agents WHERE staff_and_agents_id = %s "
            variables.append(data['partner_id'])
            cursor.execute(Q,tuple(variables))
            return self.dictfetchOne(cursor)

    def createStaff(self, data):
        cursor = connections['ufone_db'].cursor()
        staff = data['data']
        variables = []
        fields = [
        # {'field':'staff_agent_name', 'type':'varchar'},{'field':'type', 'type':'varchar'},
        {'field':'password', 'type':'varchar'},{'field':'password_salt', 'type':'varchar'},{'field':'password_mush_change', 'type':'boolean'}
        # ,{'field':'fax', 'type':'varchar'},{'field':'email', 'type':'varchar'},{'field':'postal_address_1', 'type':'varchar'},
        # {'field':'postal_address_2', 'type':'varchar'},{'field':'postal_address_3', 'type':'varchar'},{'field':'notes', 'type':'varchar'},
        # {'field':'contact', 'type':'varchar'},{'field':'start_date', 'type':'date'},
        # {'field':'end_date', 'type':'date'},{'field':'comission_type', 'type':'varchar'},{'field':'comission_factor', 'type':'real'},
        # {'field':'gstnumber', 'type':'varchar'},{'field':'bank_account', 'type':'varchar'}, {'field':'phone','type':'varchar'}
        # ,{'field':'holding_account', 'type':'int'}
        ]

        try:
            query = ""
            pass_salt = ""
            if 'staff_and_agents_id' in staff and staff['staff_and_agents_id'] != "":
                for index in fields:
                    if index['field'] in staff:
                        # check field password then generate password
                        if index['field'] == 'password':
                            if staff[index['field']] is None or staff[index['field']] == "":
                                continue

                            pass_data = self.generatePassword(staff[index['field']])
                            staff[index['field']] = pass_data['pass']
                            pass_salt = pass_data['salt']

                        if query == "":
                            query = "UPDATE staff_and_agents SET "+index['field']+" = '"+staff[index['field']]+"'"
                        else:
                            query += ", "+index['field']+" = '"+staff[index['field']]+"'"

                #update password salt
                if pass_salt != "":
                    query += ", password_salt = '"+pass_salt+"'"
                    variables.append(pass_salt)

                query += " WHERE staff_and_agents_id = "+staff['staff_and_agents_id']
                cursor.execute(query,variables)
                return {'staff_updated':True}
            else:
                values = ""
                for index in fields:
                    if index['field'] in staff:
                        # check field password then generate password
                        if index['field'] == 'password':
                            if staff[index['field']] is None or staff[index['field']] == "":
                                continue

                            pass_data = self.generatePassword(staff[index['field']])
                            staff[index['field']] = pass_data['pass']
                            pass_salt = pass_data['salt']

                        if query == "":
                            query = "INSERT INTO staff_and_agents ("+index['field']
                            values = ") VALUES (%s"
                        else:
                            query += ", "+index['field']
                            values += ", %s"
                        variables.append(staff[index['field']])

                # insert password salt
                if pass_salt != "":
                    query += ", password_salt"
                    values += ", %s"
                    variables.append(pass_salt)

                query += values + ')'
                cursor.execute(query,variables)
                return {'staff_created':True}
        except:
            return {'staff_created':False}

import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Stcharge(Dict):
    def __init__(self):
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM uf1_users")
        # records = cursor.fetchall()
        # pprint.pprint(records)
        self.data = []

    def getStCharges(self, data):
        staff_id = data['staff_id']
        variables = []

        cursor = connections['ufone_db'].cursor()
        # query = "SELECT st.*, clients.client_id, clients.client_name FROM clients INNER JOIN wl_enduser.standing_charges_view st ON(st.client_id = clients.client_id AND clients.staff_and_agents_id = %s)"
        query = "SELECT st.*, clients.client_id, clients.client_name FROM clients INNER JOIN wl_partner.standing_charges_view_wl st ON(st.client_id = clients.client_id AND clients.staff_and_agents_id = %s)"
        variables.append(staff_id)
        if 'client_id' in data and data['client_id'] != "":
            query += " WHERE clients.client_id = %s"
            variables.append(data['client_id'])

        query += " ORDER BY clients.client_id"
        
        # if limit != "":
        #     query += " LIMIT %s"
        #     variables.append(limit)

        cursor.execute(query,tuple(variables))
        charges = self.dictfetchall(cursor)
        return charges

    def getStandingCharges(self, data):
        variables = [data['client_id']]
        cursor = connections['ufone_db'].cursor()

        query = ("SELECT s.*, p.provider_id, p.provider_name, (SELECT calling_number FROM test.client_to_phone WHERE client_to_phone_id = s.client_to_phone_id)"
        "FROM test.standing_charges s INNER JOIN service_providers p ON p.provider_id::varchar = s.provider_name WHERE s.client_id = %s")

        if 'standing_charge_id' in data:
            query += " AND standing_charge_id = %s"
            variables.append(data['standing_charge_id'])

        cursor.execute(query,variables)
        st_charge = self.dictfetchall(cursor)
        return st_charge


    def createStandingCharges(self, data):
        cursor = connections['ufone_db'].cursor()
        st_charges = data['data']
        variables = []
        fields = [
        {'field':'provider_name', 'type':'varchar'},{'field':'standing_charge_date_time', 'type':'date'},
        {'field':'standing_charge_description', 'type':'varchar'}, {'field':'charged_in', 'type':'varchar'}, 
        {'field':'retail_price', 'type':'double'},{'field':'wholesale_price', 'type':'double'},
        {'field':'invoice_date', 'type':'date'},{'field':'client_to_phone_id', 'type':'int'},
        {'field':'client_toll_free_id', 'type':'int'}, {'field':'deactivate_date', 'type':'date'},
        {'field':'quantity', 'type':'double'}, {'field':'unit_cost', 'type':'double'},
        {'field':'wl_price', 'type':'double'}
        ]

        # try:
        if 'standing_charge_id' in st_charges and st_charges['standing_charge_id'] != "":
            query = ""
            for index in fields:
                if index['field'] in st_charges:
                    if query == "":
                        query = "UPDATE test.standing_charges SET "+index['field']+" = %s"
                    else:
                        query += ", "+index['field']+" = %s"
                    variables.append(st_charges[index['field']])

            query += " WHERE standing_charge_id = %s"
            variables.append(st_charges['standing_charge_id'])
            cursor.execute(query,variables)
            return {'st_charges_updated':True}
        else:
            variables.append(data['client_id']);
            query = "INSERT INTO test.standing_charges (client_id"
            values = ") VALUES (%s"
            for index in fields:
                if index['field'] in st_charges:
                    # if ((contact[index['field']] is None or contact[index['field']] == '') and index['type'] == 'date'):
                    # contact[index['field']] = 'NULL'
                    query += ", "+index['field']
                    values += ", %s"
                    variables.append(st_charges[index['field']])

            query += values + ')'
            cursor.execute(query,variables)
            return {'st_charges_created':True}
        # except:
        #     return {'contact_created':False}

    def createOneOffCharges(self, data):
        cursor = connections['ufone_db'].cursor()
        charges = data['data']
        variables = []
        fields = [
        {'field':'invoice_number', 'type':'int'},{'field':'other_charges_date', 'type':'date'},
        {'field':'other_charges_description', 'type':'varchar'}, {'field':'other_charges_quantity', 'type':'double'}, 
        {'field':'other_charges_nett_amount', 'type':'double'},{'field':'other_charges_gst_amount', 'type':'double'},
        {'field':'other_charges_gross_amount', 'type':'double'},{'field':'other_charges_age', 'type':'varchar'},
        {'field':'invoice_date', 'type':'date'}, {'field':'other_charges_cost', 'type':'double'},
        {'field':'other_charges_calling_number', 'type':'varchar'}, {'field':'other_charges_duration', 'type':'double'},
        {'field':'supplier', 'type':'varchar'}, {'field':'supplier_invoice', 'type':'varchar'},
        {'field':'supplier_invoice_date', 'type':'date'},{'field':'wl_retail', 'type':'double'}
        ]

        # try:
        if 'other_charges_transaction_id' in charges and charges['other_charges_transaction_id'] != "":
            query = ""
            for index in fields:
                if index['field'] in charges:
                    if query == "":
                        query = "UPDATE test.other_charges SET "+index['field']+" = %s"
                    else:
                        query += ", "+index['field']+" = %s"
                    variables.append(charges[index['field']])

            query += " WHERE other_charges_transaction_id = %s"
            variables.append(charges['other_charges_transaction_id'])
            cursor.execute(query,variables)
            return {'charge_updated':True}
        else:
            query = "INSERT INTO test.other_charges (client_id"
            variables.append(data['client_id']);
            values = ") VALUES (%s"
            for index in fields:
                if index['field'] in charges:
                    query += ", "+index['field']
                    values += ", %s"
                    variables.append(charges[index['field']])

            query += values + ')'
            cursor.execute(query,variables)
            return {'charge_created':True}
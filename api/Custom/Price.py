import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Price(Dict):
    def __init__(self):
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM uf1_users")
        # records = cursor.fetchall()
        # pprint.pprint(records)
        self.data = []

    def getClientPrices(self, data):
        staff_id = data['staff_id']
        limit = data['limit']
        search_str = data['search_str']
        variables = []

        cursor = connections['ufone_db'].cursor()
        if 'pricing_id' not in data:
            query = "SELECT wp.*, clients.client_id, clients.client_name FROM clients INNER JOIN white_label_pricing wp ON (wp.client_id = clients.client_id AND clients.staff_and_agents_id = %s)"
            variables.append(staff_id)
            if 'client_id' in data and data['client_id'] != "":
                query += " WHERE clients.client_id = %s"
                variables.append(data['client_id'])

            query += " ORDER BY clients.client_id"
            
            if limit != "":
                query += " LIMIT %s"
                variables.append(limit)

            cursor.execute(query,tuple(variables))
            prices = self.dictfetchall(cursor)
        else:
            query = "SELECT wp.*, clients.client_id, clients.client_name FROM clients INNER JOIN white_label_pricing wp ON (wp.client_id = clients.client_id AND clients.staff_and_agents_id = %s AND wp.wl_pricing_id=%s) ORDER BY clients.client_id"
            variables.extend([staff_id, data['pricing_id']])
            cursor.execute(query,tuple(variables))
            prices = self.dictfetchOne(cursor)
        return prices

    def updateClientPrices(self, data):
        variables = []
        cursor = connections['ufone_db'].cursor()
        query = "SELECT wp.wl_pricing_id FROM clients INNER JOIN white_label_pricing wp ON (wp.client_id = clients.client_id AND clients.staff_and_agents_id = %s AND wp.wl_pricing_id=%s)"
        variables.extend([data['staff_id'], data['pricing_id']])
        cursor.execute(query,tuple(variables))
        prices = self.dictfetchOne(cursor)

        if 'wl_pricing_id' in prices:
            cols = ['local','national','mobile','intz1','intz2','intz3','tf_local','tf_nat','tf_mob','tf_min','sip','ddi','ext','device']
            query = ""
            for index in cols:
                if index in data['data']:
                    if query == "":
                        query = "UPDATE white_label_pricing SET "+index+' = '+data['data'][index]
                    else:
                        query += ", "+index+" = "+data['data'][index]

            query += ' WHERE wl_pricing_id = %s'
            cursor.execute(query,tuple([data['pricing_id']]))
        return prices

    def insertClientPriceById(self, client_id, data):
        prices = self.getDefaultPrices()

        try:
            for key in data:
                if data[key] != "":
                    prices[key.replace("price_","")] = data[key]
                
            cursor = connections['ufone_db'].cursor()
            query = "INSERT INTO test.white_label_pricing (client_id, local, national, mobile, intz1, intz2, intz3, tf_local, tf_nat, tf_mob, tf_min, sip, ddi, ext, device) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,[client_id, prices['local'], prices['national'],prices['mobile'],prices['intz1'] ,prices['intz2'] ,prices['intz3'] ,prices['tf_local'],prices['tf_nat'],prices['tf_mob'], prices['tf_min'], prices['sip'], prices['ddi'], prices['ext'], prices['device']])
            return cursor.lastrowid
        except:
            return 0

    def getDefaultPrices(self):
        cursor = connections['ufone_db'].cursor()
        cursor.execute("SELECT * FROM white_label_pricing_defaults")
        prices = self.dictfetchOne(cursor)
        return prices
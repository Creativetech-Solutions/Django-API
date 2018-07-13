import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Payment(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def paymentOptions(self, data):
        return [
            {'id': 1, 'name':'Cheque'},
            {'id': 2, 'name':'Credit Card'},
            {'id': 3, 'name':'Direct Debit'},
            {'id': 4, 'name':'Direct Credit'},
            {'id': 5, 'name':'Web'},
        ]

    def getPayments(self, data):
        client_id = data['client_id']
        cursor = connections['ufone_db'].cursor()
        query = "SELECT * FROM payments WHERE client_id = %s"
        cursor.execute(query,[client_id])
        payments = self.dictfetchall(cursor)
        return payments
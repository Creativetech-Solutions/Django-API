import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Invoice(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def getClientInvoicesByStaff(self, data, userType):
        staff_id = data['staff_id']
        limit = data['limit']
        search_str = data['search_str']
        client_id = data['client_id']
        variables = []

        if userType == 'Operational':
            staff_check = False
        else:
            staff_check = True

        cursor = connections['ufone_db'].cursor()
        if client_id == "":
            query = "SELECT DISTINCT ON (clients.client_id) clients.client_name,  accounts_rx.* FROM clients INNER JOIN accounts_rx ON (accounts_rx.client_id = clients.client_id"
            if staff_check:
                query += " AND clients.staff_and_agents_id = %s"
                variables.append(staff_id)

            query += ") ORDER BY clients.client_id ASC, accounts_rx.invoice_date DESC"
        else:
            query = "SELECT clients.client_name,  accounts_rx.* FROM clients INNER JOIN accounts_rx ON (accounts_rx.client_id = clients.client_id"
            if staff_check:
                query += " AND clients.staff_and_agents_id = %s"
                variables.append(staff_id)

            query += " AND clients.client_id = %s) ORDER BY clients.client_id ASC, accounts_rx.invoice_date DESC"
            variables.append(client_id)

        if limit != "":
            query += " LIMIT %s"
            variables.append(limit)

        cursor.execute(query,tuple(variables))
        invoices = self.dictfetchall(cursor)
        return invoices

    def getClientWLInvoicesByStaff(self, data):
        staff_id = data['staff_id']
        limit = data['limit']
        search_str = data['search_str']
        client_id = data['client_id']
        variables = []

        cursor = connections['ufone_db'].cursor()
        if client_id == "":
            query = ("SELECT DISTINCT ON (acc.client_id) c.client_name, acc.*, c.client_id FROM accounts_rx_wl acc "
                "INNER JOIN clients_wl cw ON cw.wl_client_id = acc.client_id INNER JOIN clients c ON c.client_id = cw.client_id "
                "AND c.staff_and_agents_id = %s ORDER BY acc.client_id ASC, acc.invoice_date DESC")
            variables.append(staff_id)
        else:
            query = ("SELECT  acc.*,cw.client_name FROM accounts_rx_wl acc INNER JOIN clients_wl cw "
                "ON cw.wl_client_id = acc.client_id INNER JOIN clients c ON c.client_id = cw.client_id "
                "AND c.staff_and_agents_id = %s AND c.client_id = %s ORDER BY acc.client_id ASC, acc.invoice_date DESC")
            variables.extend([staff_id,client_id])

        if limit != "":
            query += " LIMIT %s"
            variables.append(limit)

        cursor.execute(query,tuple(variables))
        invoices = self.dictfetchall(cursor)
        return invoices

    def getOneOffInvoices(self, data):
        client_id = data['client_id']
        cursor = connections['ufone_db'].cursor()
        query = "SELECT oc.* FROM oneoff_invoices oc WHERE oc.client_id = %s ORDER BY oc.invoice_date DESC"
        cursor.execute(query,[client_id])
        oneoffinvoices = self.dictfetchall(cursor)
        return oneoffinvoices
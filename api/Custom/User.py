import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class User(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    # login function
    def authenticateUser(self, data):
        cursor = connections['ufone_db'].cursor()
        account = data.get('username')
        password = data.get('password')
        query = "SELECT staff_and_agents_id,staff_agent_name,phone,fax,email,postal_address_1,password,type,password_salt FROM staff_and_agents WHERE staff_and_agents_id = %s"
        cursor.execute(query,[int(account)])
        staff = self.dictfetchOne(cursor)
        if 'staff_and_agents_id' in staff :
            pass_data = self.generatePassword(password, staff['password_salt'])
            if pass_data['pass'] == staff['password']:
                staff.pop('password', None)
                staff.pop('password_salt', None)
                return staff
        return staff

    def getUserServices(self, data, userType):
        cursor = connections['ufone_db'].cursor()
        account = data['staff_id']
        query = ("SELECT SUM(arx.invoice_net_amount) as total_amt, SUM(arx.toll_traffic_amount) as toll_calls_amt," 
            " SUM(arx.local_traffic_amount) as local_ditto_amt, SUM(arx.fax_traffic_amount) as fax_amt,"
            " SUM(arx.standing_charges_amount) as st_charges_amt"
            " FROM clients INNER JOIN accounts_rx_all_current_view arx ON "
            " (arx.client_id = clients.client_id AND clients.staff_and_agents_id = %s AND clients.head_office = FALSE "
            " AND arx.client_id != (SELECT holding_account FROM staff_and_agents WHERE staff_and_agents_id = %s))")
        cursor.execute(query, 2 * [int(account)])
        services = self.dictfetchOne(cursor)
        return services

    def feeds(self, data):
        cursor = connections['ufone_db'].cursor()
        account = data['staff_id']
        # cursor.execute("SELECT c.client_id, c.client_name, (SELECT SUM(retail) FROM clear_cdr WHERE clear_cdr.client_id = c.client_id) Calling, (SELECT SUM(st.unit_cost*st.quantity) FROM wl_enduser.standing_charges_view st WHERE st.client_id = c.client_id) St_charges,(SELECT SUM(fd.cost) FROM faxware_cdr_view fd WHERE fd.client_id = c.client_id) fax_calls FROM staff_and_agents s INNER JOIN clients c ON c.staff_and_agents_id = s.staff_and_agents_id WHERE s.staff_and_agents_id = %s",[int(account)])
        feeds = {'toll_free':0}
        cursor.execute("SELECT SUM(retail) as calling FROM clear_cdr INNER JOIN clients c ON clear_cdr.client_id = c.client_id AND c.staff_and_agents_id = %s",[int(account)])
        feeds['calling'] = self.dictfetchOne(cursor)

        cursor.execute("SELECT SUM(st.unit_cost) as st_charges FROM wl_enduser.standing_charges_view st INNER JOIN clients c ON st.client_id = c.client_id AND c.staff_and_agents_id = %s",[int(account)])
        feeds['st_charges'] = self.dictfetchOne(cursor)

        cursor.execute("SELECT SUM(fd.cost) as fax FROM faxware_cdr_view fd INNER JOIN clients c ON fd.client_id = c.client_id AND c.staff_and_agents_id = %s",[int(account)])
        feeds['fax'] = self.dictfetchOne(cursor)

        return feeds

    def getServiceProviders(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT * FROM service_providers"
        cursor.execute(query)
        providers = self.dictfetchall(cursor)
        return providers
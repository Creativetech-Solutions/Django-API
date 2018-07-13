import psycopg2
from django.db import connections
from collections import namedtuple
import json
from api.Custom.Dict import *
from api.Custom.Price import *

class Client(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def getClientsByStaff(self, data, userType):
        #  check optional params
        if 'limit' not in data:
            data['limit'] = ""
        if 'search_str' not in data:
            data['search_str'] = ""
        if 'multi_search_params' not in data:
            data['multi_search_params'] = ""

        if userType == 'White Label Partner':
            return self.getWlClients(data)
        elif userType == 'Wholesale Partner':
            return self.getWSClients(data)
        elif userType == 'Operational':
            return self.getOpsClients(data)

    def getWlClients(self, data):
        staff_id = data['staff_id']
        limit = data['limit']
        search_str = data['search_str']
        multi_search = data['multi_search_params']
        variables = []

        cursor = connections['ufone_db'].cursor()
        # if limit == "1":
        #     query = "SELECT cwl.*  FROM clients_wl cwl "
        # else:
        #     query = "SELECT cwl.physical_address_2, cwl.physical_address_1, clients.client_contact,cwl.client_id,cwl.wl_client_id,clients.client_name, cwl.client_email, cwl.client_phone_number FROM clients_wl cwl "

        query = "SELECT cwl.*  FROM clients_wl cwl INNER JOIN clients ON cwl.client_id = clients.client_id WHERE clients.staff_and_agents_id = %s "
        variables.append(staff_id)
        if 'client_id' in data:
            query += "AND clients.client_id = %s"
            variables.append(data['client_id'])

        if search_str != "":
            query += " AND (clients.client_name ILIKE %s OR clients.client_phone_number ILIKE %s OR clients.client_email ILIKE %s OR cwl.client_email ILIKE %s OR cwl.client_phone_number ILIKE %s OR cwl.client_name ILIKE %s)"
            variables += 6 * ['%'+search_str+'%']

        if multi_search != "":
            if multi_search['client_name'] != "":
                client_name = multi_search['client_name']
                query += " AND clients.client_name ILIKE %s OR cwl.client_name ILIKE %s"
                variables += 2 * ['%'+client_name+'%']

            if multi_search['client_email'] != "":
                client_email = multi_search['client_email']
                query += " AND (clients.client_email ILIKE %s OR cwl.client_email ILIKE %s) "
                variables += 2 * ['%'+client_email+'%']

            if multi_search['client_phone'] != "":
                client_phone = multi_search['client_phone']
                query += " AND (clients.client_phone_number ILIKE %s OR clients.client_phone_number2 ILIKE %s) "
                variables += 2 * ['%'+client_phone+'%']

            if multi_search['client_area'] != "":
                cl_area = multi_search['client_area']
                query += " AND clients.area ILIKE %s "
                variables.append('%'+cl_area+'%')

            if multi_search['client_contact'] != "":
                client_contact = multi_search['client_contact']
                query += " AND clients.client_contact ILIKE %s "
                variables.append('%'+client_contact+'%')

            if multi_search['client_fax'] != "":
                client_fax = multi_search['client_fax']
                query += " AND clients.client_fax_number ILIKE %s "
                variables.append('%'+client_fax+'%')
        
        cursor.execute(query,tuple(variables))
        if limit == "1":
            clients = self.dictfetchOne(cursor)
        else:
            clients = self.dictfetchall(cursor)
        return clients

    def getWSClients(self,data):
        staff_id = data['staff_id']
        limit = data['limit']
        search_str = data['search_str']
        multi_search = data['multi_search_params']
        variables = []

        cursor = connections['ufone_db'].cursor()
        # if limit == "1":
        #     query = "SELECT clients.* FROM clients "
        # else:
        #     query = "SELECT client_id, client_name, area, postal_address_1, postal_address_2,postal_address_3, physical_address_1, notes, client_phone_number, client_fax_number, client_email  FROM clients "

        query = "SELECT clients.* FROM clients WHERE staff_and_agents_id = %s "
        variables.append(staff_id)
        if 'client_id' in data:
            query += "AND clients.client_id = %s "
            variables.append(data['client_id'])

        if search_str != "":
            query += " AND (client_name ILIKE %s OR client_phone_number ILIKE %s  OR client_email ILIKE %s )"
            variables += 3 * ['%'+search_str+'%']

        if multi_search != "":
            if multi_search['client_name'] != "":
                client_name = multi_search['client_name']
                query += " AND client_name ILIKE %s "
                variables.append('%'+client_name+'%')

            if multi_search['client_email'] != "":
                client_email = multi_search['client_email']
                query += " AND client_email ILIKE %s "
                variables.append('%'+client_email+'%')

            if multi_search['client_phone'] != "":
                client_phone = multi_search['client_phone']
                query += " AND client_phone_number ILIKE %s client_phone_number2 ILIKE %s"
                variables += 2 * ['%'+client_phone+'%']

            if multi_search['client_contact'] != "":
                client_contact = multi_search['client_contact']
                query += " AND client_contact ILIKE %s "
                variables.append('%'+client_contact+'%')

            if multi_search['client_fax'] != "":
                client_fax = multi_search['client_fax']
                query += " AND client_fax_number ILIKE %s "
                variables.append('%'+client_fax+'%')

            if multi_search['client_area'] != "":
                cl_area = multi_search['client_area']
                query += " AND area ILIKE %s "
                variables.append('%'+cl_area+'%')

        if limit != "":
            query += " LIMIT %s"
            variables.append(limit)

        cursor.execute(query,tuple(variables))
        if limit == "1" or 'client_id' in data:
            clients = self.dictfetchOne(cursor)
        else:
            clients = self.dictfetchall(cursor)
        return clients

    def getOpsClients(self, data):
        staff_id = data['staff_id']
        limit = data['limit']
        search_str = data['search_str']
        variables = []

        cursor = connections['ufone_db'].cursor()
        if 'client_id' in data:
            Q = ("SELECT c.*, s.staff_and_agents_id, s.staff_agent_name, s.type,"
                "CASE WHEN s.type = '3' THEN 'Direct' WHEN s.type = '8' THEN 'Wholesale'"
                "WHEN s.type = '9' THEN 'Whitelabel' ELSE '' END as type FROM clients c "
                "INNER JOIN staff_and_agents s ON s.staff_and_agents_id = c.staff_and_agents_id WHERE client_id = %s")
            
            variables.append(data['client_id'])
            cursor.execute(Q,tuple(variables))
            return self.dictfetchOne(cursor)
        else:    
            Q = self.makeQuery(search_str,data)

            if Q:
                
                cursor.execute(Q['query'],tuple(Q['variables']))

                if limit == "1":
                    clients = self.dictfetchOne(cursor)
                else:
                    clients = self.dictfetchall(cursor)
                return clients


    # create client for white label/wholesale users
    def createClient(self, data, userType):
        if(userType == 'Operational'):
            return self.opsCreateClient(data)
        cursor = connections['ufone_db'].cursor()
        client_name = data['data']['client_name']
        notes = data['data']['notes']
        staff_id = data['staff_id']

        # get partner name by id
        cursor.execute('SELECT staff_agent_name FROM staff_and_agents WHERE staff_and_agents_id = %s',  [staff_id])
        partner = self.dictfetchOne(cursor)

        client_name_full = partner['staff_agent_name']+'('+client_name+')'

        cursor.execute('SELECT client_id FROM test.clients WHERE client_name = %s ORDER BY client_id DESC LIMIT 1',  [client_name])
        clients = self.dictfetchOne(cursor)
        if 'client_id' not in clients:
            #account_fields = ['trade_name','email','post_address_1','phy_address_1','phone_num_1','fax_num','contact','post_address_2','post_address_3','phy_address_2','phone_num_2']
            try:
                columns = ['client_name','notes']
                values = [client_name, notes]
                if userType == 'White Label Partner':
                    if 'trade_name' in data['data']:
                        trade_name = data['data']['trade_name']
                    else:
                        trade_name = ""

                    if 'email' in data['data']:
                        email = data['data']['email']
                    else:
                        email = ""

                    if 'contact' in data['data']:
                        contact = data['data']['contact']
                    else:
                        contact = ""

                    if 'post_address_1' in data['data']:
                        post_address_1 = data['data']['post_address_1']
                    else:
                        post_address_1 = ""

                    if 'post_address_1' in data['data']:
                        post_address_2 = data['data']['post_address_2']
                    else:
                        post_address_2 = ""

                    if 'post_address_1' in data['data']:
                        post_address_3 = data['data']['post_address_3']
                    else:
                        post_address_3 = ""
                        
                    if 'phy_address_1' in data['data']:
                        phy_address_1 = data['data']['phy_address_1']
                    else:
                        phy_address_1 = ""

                    if 'phy_address_2' in data['data']:
                        phy_address_2 = data['data']['phy_address_2']
                    else:
                        phy_address_2 = ""
                        
                    if 'phone_num_1' in data['data']:
                        phone_num_1= data['data']['phone_num_1']
                    else:
                        phone_num_1 = ""
                        
                    if 'phone_num_2' in data['data']:
                        phone_num_2= data['data']['phone_num_2']
                    else:
                        phone_num_2 = ""
                        
                    if 'fax_num' in data['data']:
                        fax_num = data['data']['fax_num']
                    else:
                        fax_num = ""
                        
                    # default_price = data['data']['default_price']
                    # change_price = data['data']['change_price']
                    query = "INSERT INTO test.clients (client_name, trading_as, notes, staff_and_agents_id) VALUES (%s,%s,%s,%s)"
                    cursor.execute(query,[client_name_full, client_name, notes,staff_id])
                    # get client id of inserted row 
                    cursor.execute('SELECT client_id FROM test.clients WHERE oid = %s LIMIT 1',  [cursor.lastrowid])
                    client = self.dictfetchOne(cursor)

                    if data['data']['acc_type'] == "wl":
                        query = "INSERT INTO test.clients_wl (client_id, client_name, trading_as,client_email,postal_address_1,postal_address_2,postal_address_3,physical_address_1,physical_address_2,client_phone_number,client_phone_number2,client_fax_number, notes, client_contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(query,[client['client_id'], client_name, trade_name,email,post_address_1,post_address_2,post_address_3,phy_address_1,phy_address_2,phone_num_1,phone_num_2,fax_num, notes, contact])

                else:
                    query = "INSERT INTO test.clients (client_name, trading_as, notes, staff_and_agents_id) VALUES (%s,%s,%s,%s)"
                    cursor.execute(query,[client_name_full, client_name, notes,staff_id])
                    # getting client id
                    cursor.execute('SELECT client_id FROM test.clients WHERE oid = %s LIMIT 1',  [cursor.lastrowid])
                    client = self.dictfetchOne(cursor)

                if data['data']['prices'] is not None:   
                    p = Price()
                    pricing_id = p.insertClientPriceById(client['client_id'], data['data']['prices'])
                else:
                    pricing_id = 0    
                return {'client_id':client['client_id'], 'pricing_id':pricing_id}
            except:
                return {'client_id':0, 'pricing_id':0}
        else:
            return {'client_id':0, 'pricing_id':0}

    # create client for ops users
    def opsCreateClient(self, data):
        cursor = connections['ufone_db'].cursor()
        client = data['data']
        client_name = client['client_name']
        staff_id = data['staff_id']

        # get partner name by id
        cursor.execute('SELECT staff_agent_name FROM staff_and_agents WHERE staff_and_agents_id = %s',  [staff_id])
        partner = self.dictfetchOne(cursor)

        client_name_full = partner['staff_agent_name']+'('+client_name+')'

        cursor.execute('SELECT client_id FROM test.clients WHERE client_name = %s ORDER BY client_id DESC LIMIT 1',  [client_name])
        clients = self.dictfetchOne(cursor)
        if 'client_id' not in clients:
            #account_fields = ['trade_name','email','post_address_1','phy_address_1','phone_num_1','fax_num','contact','post_address_2','post_address_3','phy_address_2','phone_num_2']
            boalean_fields = ['charge_client_gst','group_print_bcast','client_flag','email_invoice','print_invoice','web_invoice','charge_call_per_sec','wl_enable', 'is_active','head_office']
            try:
                columns = ['client_name']
                values = [client_name]
                for key in boalean_fields:
                    if key in client:
                        client[key] = True
                    else:
                        client[key] = False
                    
                query = "INSERT INTO test.clients "
                query += "(client_name, faxware_account_name, area, postal_address_1, postal_address_2, postal_address_3, physical_address_1, physical_address_2, notes, client_phone_number, client_phone_number2, staff_and_agents_id, client_fax_number, client_email, client_contact, national_rate_plan, international_rate_plan, broadcast_rate_plan, client_pin, charge_client_gst_flag, group_print_bcast_flag, client_flag, country_id,area_name_id, is_active, client_type, invoice_to_email, invoice_to_print, invoice_to_web, account_manager_id, decision_maker, decision_maker_phone, account_manager_base_amount, industry_id, business_type_id, number_of_employees, head_office, operating_hours, trading_as, charge_calls_per_second, national_voip_rate_plan, international_voip_rate_plan, payment_option)"
                query += " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query,[client_name_full, client['faxware_acc_name'], client['area'], client['post_address_1'], client['post_address_2'], client['post_address_3'], client['phy_address_1'], client['phy_address_2'], client['notes'], client['phone_num_1'], client['phone_num_2'], client['staff_and_agents_id'], client['fax_num'], client['email'], client['contact'], client['national_rate_plan'], client['international_rate_plan'], client['broadcoast_rate_plan'], client['pin'], client['charge_client_gst'], client['group_print_bcast'], client['client_flag'], client['country_id'], client['area_name_id'], client['is_active'], client['client_type'], client['email_invoice'], client['print_invoice'], client['web_invoice'], client['account_mananger_id'], client['decision_maker'], client['decision_maker_phone'], client['account_mananger_base_amt'], client['industry_id'], client['business_type_id'], client['no_of_employees'], client['head_office'], client['operating_hrs'], client['trade_name'], client['charge_call_per_sec'], client['national_voip_rate_plan'], client['international_voip_rate_plan'], client['payment_option_id']])
                # get client id of inserted row 
                cursor.execute('SELECT client_id FROM test.clients WHERE oid = %s LIMIT 1',  [cursor.lastrowid])
                client = self.dictfetchOne(cursor)

                if data['data']['prices'] is not None:   
                    p = Price()
                    pricing_id = p.insertClientPriceById(client['client_id'], data['data']['prices'])
                else:
                    pricing_id = 0    
                return {'client_id':client['client_id'], 'pricing_id':pricing_id}
            except:
                return {'client_id':0, 'pricing_id':0, 'msg':'Error Occured! Account did not created'}
        else:
            return {'client_id':0, 'pricing_id':0, 'msg':'Client Name Already Exist'}

    def makeQuery(self, search_str, data):
        variables = []

        if 'partner_id' in data:
            query = "SELECT * FROM clients WHERE staff_and_agents_id = %s"
            variables = [data['partner_id']]
            return {"query":query, "variables":variables}

        try: 
            # toll free number search
            search_str = int(search_str)
            query = ("SELECT c.client_name, c.client_id, c.client_phone_number, cp.calling_number FROM clients c INNER JOIN client_to_phone cp on cp.client_id = c.client_id"
            " AND (cp.calling_number LIKE %s or CAST(c.client_id AS TEXT) LIKE %s)")
            variables += 2 * ['%'+str(search_str)+'%']
            return {"query":query, "variables":variables}

        except:
            search_str = search_str.lower()
            if search_str.startswith("ip:") :
                # ip address search
                search_str = str(search_str.replace("ip:",""))
                query = "SELECT c.client_name, c.client_id, r.radius_id, r.ip_address FROM clients c INNER JOIN test.radius r on c.client_id = r.account_number AND r.ip_address ILIKE %s"
                variables.append('%'+str(search_str)+'%')
                return {"query":query, "variables":variables}

            elif search_str.startswith("asid:"):
                # ip address search
                search_str = str(search_str.replace("asid:",""))
                query = "SELECT c.client_name, c.client_id, cp.calling_number, cp.client_to_phone_id FROM clients c INNER JOIN client_to_phone cp on c.client_id = cp.client_id AND cp.line_type_id = 14 AND cp.calling_number ILIKE %s"
                variables.append('%'+str(search_str)+'%')
                return {"query":query, "variables":variables}

            elif search_str.startswith("ddi:"):
                # ip address search
                search_str = str(search_str.replace("ddi:",""))
                query = "SELECT c.client_name, c.client_id, cp.calling_number, cp.client_to_phone_id FROM clients c INNER JOIN client_to_phone cp on c.client_id = cp.client_id AND cp.line_type_id = 13 AND cp.calling_number ILIKE %s"
                variables.append('%'+str(search_str)+'%')
                return {"query":query, "variables":variables}

            else:
                # full search
                query = ("SELECT DISTINCT ON (c.client_id) c.client_id, c.client_name, cp.calling_number, lt.line_type_description, lt.line_type_id FROM clients c INNER JOIN client_to_phone cp on c.client_id = cp.client_id INNER JOIN line_type lt ON cp.line_type_id = lt.line_type_id"
                " WHERE c.client_name ILIKE %s or c.postal_address_1 ILIKE %s or c.postal_address_2 ILIKE %s"
                " or c.physical_address_1 ILIKE %s or c.physical_address_2 ILIKE %s")
                variables += 5 * ['%'+search_str+'%']
                return {"query":query, "variables":variables}

            return False


    def getCredits(self, data, type):
        client_id = data['client_id']
        cursor = connections['ufone_db'].cursor()
        query = "SELECT * FROM credits WHERE client_id = %s AND date_part('year', credits_date) = date_part('year', CURRENT_DATE)"
        cursor.execute(query,[client_id])
        credits = self.dictfetchall(cursor)
        return credits

    def getContacts(self, data):
        variables = [data['client_id']]
        cursor = connections['ufone_db'].cursor()
        query = "SELECT c.*, p.position_description FROM test.contacts c LEFT JOIN company_position p ON c.job_position_id = p.position_id WHERE c.client_id = %s"
        if 'contact_id' in data:
            query += " AND c.contact_id = %s"
            variables.append(data['contact_id'])

        cursor.execute(query,variables)
        contacts = self.dictfetchall(cursor)
        return contacts

    def getAccountSummary(self, data):
        variables = [data['client_id']]
        cursor = connections['ufone_db'].cursor()
        query = ("SELECT accounts_rx.*, gross_credit AS Current_Credit, discount_allowed AS Current_Discount, gross_payment AS Current_Payment,  adjustment_amount AS OOChargesOLD"
        " FROM ((accounts_rx LEFT JOIN payments_per_client_view ON accounts_rx.client_id = payments_per_client_view.client_id)"
        " LEFT JOIN credits_per_client_view ON accounts_rx.client_id = credits_per_client_view.clients_id) WHERE accounts_rx.invoice_age='0' AND accounts_rx.client_id = %s")
        cursor.execute(query,variables)
        account_summary = self.dictfetchOne(cursor)
        return account_summary

    def createContact(self, data):
        cursor = connections['ufone_db'].cursor()
        contact = data['data']
        variables = [data['client_id']]
        fields = [{'field':'surname', 'type':'varchar'},{'field':'first_name', 'type':'varchar'},{'field':'salute', 'type':'varchar'},
        {'field':'job_position_id','type':'int'},
        {'field':'fax', 'type':'varchar'},{'field':'postal1', 'type':'varchar'},{'field':'postal2', 'type':'varchar'},
        {'field':'postal3', 'type':'varchar'},{'field':'physical1', 'type':'varchar'},{'field':'physical2', 'type':'varchar'},
        {'field':'notes', 'type':'varchar'},{'field':'decision_maker', 'type':'varchar'},
        {'field':'accounts_contact', 'type':'varchar'},{'field':'login', 'type':'varchar'},{'field':'password', 'type':'varchar'},
        {'field':'mobile', 'type':'varchar'},{'field':'phone', 'type':'varchar'},{'field':'email', 'type':'varchar'}]


        try:
            if 'contact_id' in contact and contact['contact_id'] != "":
                query = ""
                for index in fields:
                    if index['field'] in contact:
                        if query == "":
                            query = "UPDATE test.contacts SET "+index['field']+" = '"+contact[index['field']]+"'"
                        else:
                            query += ", "+index['field']+" = '"+contact[index['field']]+"'"

                query += " WHERE contact_id = "+contact['contact_id']
                cursor.execute(query)
                return {'contact_updated':True}
            else:
                query = "INSERT INTO test.contacts (client_id"
                values = ") VALUES (%s"
                for index in fields:
                    if index['field'] in contact:
                        # if ((contact[index['field']] is None or contact[index['field']] == '') and index['type'] == 'date'):
                        # contact[index['field']] = 'NULL'
                        query += ", "+index['field']
                        values += ", %s"
                        variables.append(contact[index['field']])

                query += values + ')'
                cursor.execute(query,variables)
                return {'contact_created':True}
        except:
            return {'contact_created':False}

    def getWhitelabel(self, data):
        variables = [data['client_id']]
        cursor = connections['ufone_db'].cursor()
        query = "SELECT p.*,c.* FROM clients_wl c LEFT JOIN white_label_pricing p ON p.client_id = c.client_id  WHERE c.client_id = %s"
        cursor.execute(query,variables)
        white_label = self.dictfetchOne(cursor)
        return white_label

    def createWhiteLabel(self, data):
        cursor = connections['ufone_db'].cursor()
        white_label = data['data']
        try:
            self.createEditWl(data['client_id'], white_label,cursor,)
            self.creaeEditWlPrice(data['client_id'], white_label,cursor)
            # make wl enabled 
            cursor.execute('UPDATE test.clients SET wl_enabled = TRUE WHERE client_id = %s', [white_label['client_id']])
            return {'whitelabel_updated':True}
        except:
            return {'whitelabel_updated':False}

    def editClient(self, data):
        cursor = connections['ufone_db'].cursor()
        client = data['data']
        variables = []
        fields = [{'field':'client_name', 'type':'varchar'},{'field':'trading_as', 'type':'varchar'},{'field':'postal_address_1', 'type':'varchar'},
        {'field':'postal_address_2','type':'varchar'},{'field':'security_answer', 'type': 'varchar'},{'field':'security_question', 'type':'varchar'},
        {'field':'postal_address_3', 'type':'varchar'},{'field':'physical_address_1', 'type':'varchar'},{'field':'physical_address_2', 'type':'varchar'},
        {'field':'area', 'type':'varchar'},{'field':'agent_id', 'type':'varchar'},{'field':'client_email', 'type':'varchar'},
        {'field':'client_phone_number', 'type':'varchar'},{'field':'client_fax_number', 'type':'varchar'},
        {'field':'client_type', 'type':'varchar'},{'field':'invoice_to_email', 'type':'varchar'},
        {'field':'invoice_to_print', 'type':'varchar'},{'field':'charge_client_gst_flag', 'type':'varchar'},{'field':'payment_option', 'type':'varchar'},
        {'field':'notes', 'type':'varchar'}, {'field':'client_rating', 'type':'varchar'},{'field':'client_pin','type':'varchar'},
        {'field':'international_voip_rate_plan','type':'varchar'},{'field':'national_voip_rate_plan','type':'varchar'}
        ]

        # try:
        if 'client_id' in client and client['client_id'] != "":
            query = ""
            for index in fields:
                if index['field'] in client:
                    if query == "":
                        query = "UPDATE test.clients SET "+index['field']+" = %s"
                    else:
                        query += ", "+index['field']+" = %s"
                    variables.append(client[index['field']])

            query += " WHERE client_id = %s"
            variables.append(client['client_id'])
            cursor.execute(query,variables)
            return {'client_updated':True}
        # except:
        #     return {'client_updated':False}

    def createEditWl(self, client_id, white_label,cursor):
        variables = []
        fields = [{'field':'client_name', 'type':'varchar'},{'field':'trading_as', 'type':'varchar'},{'field':'postal_address_1', 'type':'varchar'},
        {'field':'postal_address_2','type':'varchar'},
        {'field':'postal_address_3', 'type':'varchar'},{'field':'physical_address_1', 'type':'varchar'},{'field':'physical_address_2', 'type':'varchar'},
        {'field':'area', 'type':'varchar'},{'field':'agent_id', 'type':'varchar'},{'field':'client_email', 'type':'varchar'},
        {'field':'client_phone_number', 'type':'varchar'},{'field':'client_fax_number', 'type':'varchar'},
        {'field':'agent_customer_id', 'type':'varchar'},{'field':'client_type', 'type':'varchar'},{'field':'invoice_to_email', 'type':'varchar'},
        {'field':'invoice_to_print', 'type':'varchar'},{'field':'charge_client_gst_flag', 'type':'varchar'},{'field':'payment_option_id', 'type':'varchar'},
        {'field':'notes', 'type':'varchar'}
        ]
        if 'wl_client_id' in white_label and white_label['wl_client_id'] != "":
            query = ""
            for index in fields:
                if index['field'] in white_label:
                    if query == "":
                        query = "UPDATE test.clients_wl SET "+index['field']+" = %s"
                    else:
                        query += ", "+index['field']+" = %s"
                    variables.append(white_label[index['field']])

            query += " WHERE wl_client_id = %s"
            variables.append(white_label['wl_client_id'])
        else:
            query = "INSERT INTO test.clients_wl (client_id"
            variables.append(client_id);
            values = ") VALUES (%s"
            for index in fields:
                if index['field'] in white_label:
                    query += ", "+index['field']
                    values += ", %s"
                    variables.append(white_label[index['field']])

            query += values + ')'

        cursor.execute(query,variables)

    def creaeEditWlPrice(self, client_id,white_label,cursor):
        prices_fields = [{'field':'local', 'type':'double'},{'field':'national', 'type':'double'},{'field':'mobile', 'type':'double'},
        {'field':'intz1','type':'double'}, {'field':'intz2', 'type':'double'},{'field':'intz3', 'type':'double'},
        {'field':'tf_local', 'type':'double'}, {'field':'tf_nat', 'type':'double'},{'field':'tf_mob', 'type':'double'},
        {'field':'tf_min', 'type':'double'}, {'field':'sip', 'type':'double'},{'field':'ddi', 'type':'double'},
        {'field':'ext', 'type':'double'},{'field':'device', 'type':'double'}
        ]
        variables = []
        if 'wl_pricing_id' in white_label and white_label['wl_pricing_id'] != "":
            query = ""
            for index in prices_fields:
                if index['field'] in white_label:
                    if query == "":
                        query = "UPDATE test.white_label_pricing SET "+index['field']+" = %s"
                    else:
                        query += ", "+index['field']+" = %s"
                    variables.append(white_label[index['field']])

            query += " WHERE wl_pricing_id = %s"
            variables.append(white_label['wl_pricing_id'])
            cursor.execute(query,variables)
        else:
            query = "INSERT INTO test.white_label_pricing (client_id"
            variables.append(client_id);
            values = ") VALUES (%s"
            for index in prices_fields:
                if index['field'] in white_label:
                    query += ", "+index['field']
                    values += ", %s"
                    variables.append(white_label[index['field']])

            query += values + ')'
            cursor.execute(query,variables)

    def getOneOffCharges(self, data):
        variables = [data['client_id']]
        cursor = connections['ufone_db'].cursor()
        query = "SELECT * FROM other_charges_historic_view WHERE client_id = %s "
        if 'other_charges_transaction_id' in data:
            query += "AND other_charges_transaction_id = %s "
            variables.append(data['other_charges_transaction_id'])

        query += " ORDER BY invoice_date DESC, other_charges_description ASC"
        cursor.execute(query,variables)
        return self.dictfetchall(cursor)

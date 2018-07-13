import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
import requests
class Radius(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []
    
    def getRadius(self):

        radiusData = self.getRadiusData() 
        try:
            if radiusData['status'] == 1 :
                cursor = connections['ufone_db'].cursor()

                optionalInputs = ['Cidr','Ip6 Address','Notifications Email','Company Name','QoS Profile']

                for data in radiusData['data']:

                    if self.isEntryExist(data['Username'], cursor): # check if record exist then update
                        query = self.updateQuery(data['Username'])
                    else:
                        query = self.insertQuery()

                    for optInput in optionalInputs:
                        if optInput not in data:
                            data[optInput] = ""

                    if 'Use Ipv6' not in data:
                        data['Use Ipv6'] = 0
                    if 'Account Number' not in data or data['Account Number'] == '':
                        data['Account Number'] = 0

                    variables = [
                        data['Cust ID'], data['Username'], data['Password'], data['Over Price'], data['Special Price'],
                        data['Total Usage'], data['Usage Plan'], data['Plan ID'], data['IP Address'], data['Send Notifications'],
                        data['Notifications Email'], data['Suspended'], data['Is Delete'], data['Have Used 80'], data['Have Used 100'],
                        data['Have Used 120'], data['Cidr'], data['Account Number'], data['First Attempt Time'], data['Last Attempt Time'],
                        data['Attempt'], data['Do Not Bill For Data'], data['Company Name'], data['Bng Type'], data['Ip6 Address'],
                        data['Use Ipv6'], data['Mtime'], json.dumps(data['Muser']), data['Uuid'], data['Active'], data['Current Month Download'], 
                        data['Current Month Upload'], data['Current Month OnNet'], data['Current Month Total Traffic'], data['ASID'],
                        data['Plan Name'], data['Online'], data['QoS Profile'], data['Is IPOE'],
                    ]
                    cursor.execute(query, variables)

                return "Records Inserted Successfully"
            return "Record not found"
        except:
            return "Error has been record"

    def isEntryExist(self, username, cursor):
        cursor.execute('SELECT radius_id FROM test.radius WHERE username = %s LIMIT 1',  [username])
        radius = self.dictfetchOne(cursor)
        if 'radius_id' in radius and radius['radius_id'] is not None:
            return True
        else:
            return False

    def updateQuery(self,username):
        query = ("UPDATE test.radius "
        "SET cust_id = (%s), username = (%s), password = (%s), over_price = (%s), special_price = (%s), "
        " total_usage = (%s), usage_plan = (%s), plan_id = (%s), ip_address = (%s), send_notifications = (%s), "
        " notifications_email = (%s), suspended = (%s), is_delete = (%s), have_used_80 = (%s), have_used_100 = (%s),"
        " have_used_120 = (%s),  ci_dr = (%s), account_number = (%s), first_attempt_time = (%s), "
        " last_attempt_time = (%s), attempt = (%s), not_bill_for_data = (%s),  company_name = (%s), "
        " bng_type = (%s), ip6_address = (%s), use_ipv6 = (%s), mtime = (%s), muser = (%s),  uuid = (%s), "
        " active = (%s), curr_mon_download = (%s), curr_mon_upload = (%s), curr_mon_onnet = (%s), "
        " curr_mon_total_traffic = (%s),  asid = (%s), plan_name = (%s), online = (%s), qos_profile = (%s), is_ipoe = (%s) "
        " WHERE username = '"+username+"'")
        return query

    def insertQuery(self):
        query = ("INSERT INTO test.radius "
        " (cust_id, username, password, over_price, special_price, total_usage, usage_plan, plan_id, "
        "ip_address, send_notifications, notifications_email, suspended, is_delete, have_used_80, "
        "have_used_100, have_used_120, ci_dr, account_number, first_attempt_time, last_attempt_time, "
        "attempt, not_bill_for_data, company_name, bng_type, ip6_address, use_ipv6, mtime, muser, uuid, "
        "active, curr_mon_download, curr_mon_upload, curr_mon_onnet, curr_mon_total_traffic, asid, plan_name, "
        "online, qos_profile, is_ipoe) VALUES "
        "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        return query

    def getRadiusData(self): 
        # get radius data from api
        token = self.getToken()
        if token is not None:
            params = {"token": token, "limit":2}
            response = self.post(params, 'radius/list', 'get')
            return response.json()

        # return json.loads('{  "status": 1,  "data": [    {      "Cust ID": 101,      "Username": "ufone@ufone.nz",      "Password": "Ducbi6m8",      "Over Price": "0.00",      "Special Price": "0.00",      "Total Usage": 100,      "Usage Plan": "Charge-ALL",      "Plan ID": 283,      "IP Address": "45.118.188.1",      "Send Notifications": 1,      "Notifications Email": "david@ufone.co.nz",      "Suspended": "N",      "Is Delete": 0,      "Have Used 80": "2018-06-05",      "Have Used 100": "2018-06-05",      "Have Used 120": "2018-06-05",      "Cidr": "45.118.188.248/29",      "Account Number": "603",      "First Attempt Time": "0000-00-00 00:00:00",      "Last Attempt Time": "0000-00-00 00:00:00",      "Attempt": 0,      "Do Not Bill For Data": 0,      "Company Name": "UFONE Office",      "Bng Type": "alu",      "Ip6 Address": "2402:6f80:2000:0000::/56",      "Use Ipv6": 1,      "Mtime": "2017-07-18T18:19:43+00:00",      "Muser": {        "RecordType": "User",        "Uuid": "eb323735-922e-5d1f-8416-5080207e76fe",        "Name": "Samuel Lay"      },      "Uuid": "e228a2cf-21da-5963-abfd-92703d2f603b",      "Active": 1,      "Current Month Download": 1687672957256,      "Current Month Upload": 224856455931,      "Current Month OnNet": 0,      "Current Month Total Traffic": 1912529413187,      "ASID": "",      "Plan Name": "Office Plan",      "Online": true,      "QoS Profile": "sla-default",      "Is IPOE": 0    },    {      "Cust ID": 101,      "Username": "hayden.broadbelt@usurf.co.nz",      "Password": "7uDe9eHu",      "Over Price": "1.50",      "Special Price": "1.50",      "Total Usage": 120,      "Usage Plan": "Charge-ALL",      "Plan ID": 283,      "IP Address": "45.118.188.130",      "Send Notifications": 0,      "Notifications Email": "",      "Suspended": "N",      "Is Delete": 0,      "Have Used 80": "0000-00-00",      "Have Used 100": "0000-00-00",      "Have Used 120": "0000-00-00",      "Account Number": "779120",      "First Attempt Time": "0000-00-00 00:00:00",      "Last Attempt Time": "0000-00-00 00:00:00",      "Attempt": 0,      "Do Not Bill For Data": 0,      "Company Name": "",      "Bng Type": "alu",      "Mtime": "2015-08-04T00:50:52+00:00",      "Muser": {        "RecordType": "User",        "Uuid": "ca98955e-8c16-5083-9147-78386a584d82",        "Name": "Adele Good"      },      "Uuid": "e85934e9-043b-504e-97e9-92949e9ac6b4",      "Active": 1,      "Current Month Download": 0,      "Current Month Upload": 0,      "Current Month OnNet": 0,      "Current Month Total Traffic": 0,      "ASID": "",      "Plan Name": "Office Plan",      "Online": false,      "QoS Profile": "",      "Is IPOE": 0    }  ],  "recordsTotal": "390",  "recordsFiltered": "390",  "result": "success"}')

    def getToken(self): 
        # get token from api
        params = {"username": "ufone-ops", "password" : "4ze#hDK3BDd#^f9y"}
        response = self.post(params, 'login', 'post')
        response = response.json()
        if response['status'] == 1:
            return response['data']['token']
        else:
            return None


    def post(self, params, method, req_type): 
        # api request
        url = 'https://vumeda.devoli.com/api/'+method
        if req_type == 'post':
            return requests.post(url, params)
        else:
            return requests.get(url, params)
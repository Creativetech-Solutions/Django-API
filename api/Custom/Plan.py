import psycopg2
from django.db import connections
from collections import namedtuple
from api.Custom.Dict import *
import json
class Plan(Dict):
    def __init__(self):
    	# cursor = conn.cursor()
    	# cursor.execute("SELECT * FROM uf1_users")
    	# records = cursor.fetchall()
    	# pprint.pprint(records)
    	self.data = []

    def getMobilePlans(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT m.mobile_plan_id, m.mobile_plan_name FROM mobile_plan m"
        cursor.execute(query)
        industries = self.dictfetchall(cursor)
        return industries

    def getMobileGroupPlans(self, data):
        cursor = connections['ufone_db'].cursor()
        query = "SELECT m.mobile_group_plan_id, m.plan_name FROM mobile_group_plan m"
        cursor.execute(query)
        industries = self.dictfetchall(cursor)
        return industries

    def getRatePlans(self, data):
        return {
            'national':[
                {'id':'1', 'name':'VoIP 1310'},
                {'id':'2', 'name':'VoIP 2412'},
                {'id':'3', 'name':'PSTN 3815'},
                {'id':'4', 'name':'PSTN 4615'},
                {'id':'5', 'name':'Overflow'},
                {'id':'6', 'name':'VoIP WS'},
                {'id':'7', 'name':'PSTN WS'}
            ],
            'international':[
                {'id':'1', 'name':'PSTN'},
                {'id':'2', 'name':'PSTN WS'},
                {'id':'3', 'name':'Mobile 1'},
                {'id':'4', 'name':'Mobile 2'},
                {'id':'5', 'name':'VoIP1-Sharp'},
                {'id':'6', 'name':'VoIP2'},
                {'id':'7', 'name':'VoIP WS'}
            ],
        }
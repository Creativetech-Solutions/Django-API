from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.Serializers.Accountserializer import *
from api.Serializers.Clientserializer import *
from api.Serializers.Invoiceserializer import *
from api.Serializers.Verification import *
from api.Serializers.Priceserializer import *
from api.Custom.User import *
from api.Custom.Token import *
from api.Custom.Area import *
from api.Custom.Business import *
from api.Custom.Country import *
from api.Custom.Industry import *
from api.Custom.Client import *
from api.Custom.Invoice import *
from api.Custom.Price import *
from api.Custom.Staff import *
from api.Custom.Phone import *
from api.Custom.Tollfree import *
from api.Custom.Stcharge import *
from api.Custom.Payment import *
from api.Custom.Fax import *
from api.Custom.Radius import *
from api.Custom.Position import *
from api.Custom.Linetype import *
from api.Custom.Plan import *
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseRedirect,  HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import random
import hashlib, binascii

class Login(APIView, Verification):
    """
    create a new snippet.
    """
    def post(self, request, format=None):
        # return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        verified = self.apiToken(request.META.get('HTTP_AUTHORIZATION'))
        if not verified:
            data = {'data':'','errors':'API Key is not valid', 'isSuccess':False}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = Loginserializer(data=request.data)
        if serializer.is_valid():
            # jsondata = JSONRenderer().render(serializer.data)
            u = User()
            staff = u.authenticateUser(serializer.data)
            if 'staff_and_agents_id' in staff and self.checkUserType(staff['type']):
                t = Token()
                token = t.createToken(staff)
                staff['userType'] = token['user_type']
                data = {'data':{'tokens':token['tokens'],'user_info':staff}, 'errors':'', 'isSuccess':True }
                return Response(data, status=status.HTTP_201_CREATED)
            else :
                data = {'data':'', 'errors':'Account Credientials are not Valid','isSuccess':False}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def services(request):
    return performRequest(request, 'services')

@api_view(['POST'])
def clients(request):
    return performRequest(request, 'clients')

@api_view(['GET'])
def getClients(request):
    return performRequest(request, 'getClients')

@api_view(['GET'])
def getInvoices(request):
    return performRequest(request, 'getInvoices')

@api_view(['GET'])
def getOneOffInvoices(request):
    return performRequest(request, 'getOneOffInvoices', 'staffs')

@api_view(['GET'])
def getOneOffCharges(request):
    return performRequest(request, 'getOneOffCharges', 'staffs')

@api_view(['GET'])
def getCredits(request):
    return performRequest(request, 'getCredits','staffs')

@api_view(['GET'])
def getContacts(request):
    return performRequest(request, 'getContacts','staffs')

@api_view(['POST'])
def createContact(request):
    return performRequest(request, 'createContact','staffs')
    
@api_view(['POST'])
def updateContact(request):
    return performRequest(request, 'updateContact','staffs')

@api_view(['POST'])
def createPhone(request):
    return performRequest(request, 'createPhone','staffs')
    
@api_view(['POST'])
def updatePhone(request):
    return performRequest(request, 'updatePhone','staffs')

@api_view(['POST'])
def createClient(request):
    return performRequest(request, 'createClient')

@api_view(['POST'])
def createTollfree(request):
    return performRequest(request, 'createTollfree','staffs')
    
@api_view(['POST'])
def updateTollfree(request):
    return performRequest(request, 'updateTollfree','staffs')

@api_view(['GET'])
def getClientPhones(request):
    return performRequest(request, 'getClientPhones')

@api_view(['GET'])
def getMobiles(request):
    return performRequest(request, 'getMobiles')

@api_view(['GET'])
def getTollFree(request):
    return performRequest(request, 'getTollFree')

@api_view(['GET'])
def getLineTypes(request):
    return performRequest(request, 'getLineTypes')

@api_view(['GET'])
def getWhitelabel(request):
    return performRequest(request, 'getWhitelabel')

@api_view(['POST'])
def createWhiteLabel(request):
    return performRequest(request, 'createWhiteLabel')

@api_view(['POST'])
def updateWhiteLabel(request):
    return performRequest(request, 'updateWhiteLabel')

class Invoices(APIView, Verification):

    def post(self, request, format=None):
        verified = self.apiToken(request.META.get('HTTP_AUTHORIZATION'))
        if not verified:
            data = {'data':'','errors':'API Key is not valid', 'isSuccess':False}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = Invoiceserializer(data=request.data)
        if serializer.is_valid():
            response = self.accessToken(request.META.get('HTTP_AUTHORIZATION'), request.data['staff_id'])
            if not response['isSuccess']:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                verified = self.verifyPermissions(response['data'])
                if verified:
                    i = Invoice()
                    if 'limit' not in request.data:
                        request.data['limit'] = ""
                    if 'search_str' not in request.data:
                        request.data['search_str'] = ""
                    if 'client_id' not in request.data:
                        request.data['client_id'] = ""
                    invoices = i.getClientInvoicesByStaff(request.data, response['data']['user_type'])
                    data = {'data':{'invoices':invoices},'errors':'', 'isSuccess':True}
                    return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WLInvoices(APIView, Verification):

    def post(self, request, format=None):
        verified = self.apiToken(request.META.get('HTTP_AUTHORIZATION'))
        if not verified:
            data = {'data':'','errors':'API Key is not valid', 'isSuccess':False}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = Invoiceserializer(data=request.data)
        if serializer.is_valid():
            response = self.accessToken(request.META.get('HTTP_AUTHORIZATION'), request.data['staff_id'])
            if not response['isSuccess']:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                verified = self.verifyPermissions(response['data'], 'WLInvoices')
                if verified:
                    i = Invoice()
                    if 'limit' not in request.data:
                        request.data['limit'] = ""
                    if 'search_str' not in request.data:
                        request.data['search_str'] = ""
                    if 'client_id' not in request.data:
                        request.data['client_id'] = ""
                    wl_invoices = i.getClientWLInvoicesByStaff(request.data)
                    data = {'data':{'wl_invoices':wl_invoices},'errors':'', 'isSuccess':True}
                    return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def prices(request):
    return performRequest(request, 'prices')

@api_view(['POST'])
def updateprices(request):
    v = Verification()
    verified = v.apiToken(request.META.get('HTTP_AUTHORIZATION'))
    if not verified:
        data = {'data':'','errors':'API Key is not valid', 'isSuccess':False}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    response = v.accessToken(request.META.get('HTTP_AUTHORIZATION'), request.data['staff_id'])
    if not response['isSuccess']:
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    else:
        verified = v.verifyPermissions(response['data'])
        if verified:
            i = Price()
            prices = i.updateClientPrices(request.data)
            data = {'data':{'prices':prices},'errors':'', 'isSuccess':True}
            return Response(data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def getDefaultPrices(request):
    return performRequest(request, 'getDefaultPrices')

@api_view(['POST'])
def phones(request):
    return performRequest(request, 'phones')

@api_view(['POST'])
def tollfree(request):
    return performRequest(request, 'tollfree')

@api_view(['POST'])
def phoneCalls(request):
    return performRequest(request, 'phoneCalls')

@api_view(['POST'])
def tollFreeCalls(request):
    return performRequest(request, 'tollFreeCalls')

@api_view(['POST'])
def fax(request):
    return performRequest(request, 'getFax')

@api_view(['POST'])
def stcharges(request):
    return performRequest(request, 'getStcharges')

@api_view(['POST'])
def feeds(request):
    return performRequest(request, 'getFeeds')

@api_view(['GET'])
def staffs(request):
    return performRequest(request, 'getStaffs', 'staffs')

@api_view(['GET'])
def getBusinessTypes(request):
    return performRequest(request, 'getBusinessTypes', 'staffs')

@api_view(['GET'])
def getAreaNames(request):
    return performRequest(request, 'getAreaNames', 'staffs')

@api_view(['GET'])
def getIndustries(request):
    return performRequest(request, 'getIndustries', 'staffs')

@api_view(['GET'])
def getCountries(request):
    return performRequest(request, 'getCountries', 'staffs')

@api_view(['GET'])
def getPayments(request):
    return performRequest(request, 'getPayments', 'staffs')

@api_view(['GET'])
def getPaymentOptions(request):
    return performRequest(request, 'paymentOptions', 'staffs')

@api_view(['GET'])
def getCompanyPositions(request):
    return performRequest(request, 'getCompanyPositions', 'staffs')

@api_view(['GET'])
def getMobilePlans(request):
    return performRequest(request, 'getMobilePlans', 'staffs')

@api_view(['GET'])
def getMobileGroupPlans(request):
    return performRequest(request, 'getMobileGroupPlans', 'staffs')

@api_view(['GET'])
def getRatePlans(request):
    return performRequest(request, 'getRatePlans', 'staffs')

@api_view(['GET'])
def getServiceProviders(request):
    return performRequest(request, 'getServiceProviders', 'staffs')

@api_view(['GET'])
def getAccountSummary(request):
    return performRequest(request, 'getAccountSummary', 'staffs')

@api_view(['GET'])
def getStandingCharges(request):
    return performRequest(request, 'getStandingCharges', 'staffs')

@api_view(['POST'])
def createStandingCharges(request):
    return performRequest(request, 'createStandingCharges', 'staffs')

@api_view(['POST'])
def updateStandingCharges(request):
    return performRequest(request, 'updateStandingCharges', 'staffs')

@api_view(['GET'])
def getStaff(request):
    return performRequest(request, 'getStaff', 'staffs')

@api_view(['POST'])
def editStaff(request):
    return performRequest(request, 'editStaff', 'staffs')
    
@api_view(['POST'])
def editClient(request):
    return performRequest(request, 'editClient', 'staffs')
    
@api_view(['POST'])
def createOneOffCharges(request):
    return performRequest(request, 'createOneOffCharges', 'staffs')
    
@api_view(['POST'])
def updateOneOffCharges(request):
    return performRequest(request, 'updateOneOffCharges', 'staffs')


def performRequest(request, method, userType = ""):
    v = Verification()
    verified = v.apiToken(request.META.get('HTTP_AUTHORIZATION'))
    if not verified:
        data = {'data':'','errors':'API Key is not valid', 'isSuccess':False}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    serializer = Clientserializer(data=request.data)
    if serializer.is_valid():
        response = v.accessToken(request.META.get('HTTP_AUTHORIZATION'), request.data['staff_id'])
        if not response['isSuccess']:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            if userType != "":
                verified = v.verifyPermissions(response['data'], userType)
            else:
                verified = v.verifyPermissions(response['data'])

            if verified:
                if method == 'paymentOptions':
                    p = Payment()
                    paymentOptions = p.paymentOptions(request.data)
                    data = {'data':{'paymentOptions':paymentOptions},'errors':'', 'isSuccess':True}

                elif method == 'services':
                    u = User()
                    services = u.getUserServices(request.data, response['data']['user_type'])
                    data = {'data':{'services':services},'errors':'', 'isSuccess':True}

                elif method == 'getPayments':
                    p = Payment()
                    payments = p.getPayments(request.data)
                    data = {'data':{'payments':payments},'errors':'', 'isSuccess':True}

                elif method == 'getCountries':
                    c = Country()
                    countries = c.getCountries(request.data)
                    data = {'data':{'countries':countries},'errors':'', 'isSuccess':True}

                elif method == 'getIndustries':
                    i = Industry()
                    industries = i.getIndustries(request.data)
                    data = {'data':{'industries':industries},'errors':'', 'isSuccess':True}

                elif method == 'getAreaNames':
                    a = Area()
                    area_names = a.getAreaNames(request.data)
                    data = {'data':{'area_names':area_names},'errors':'', 'isSuccess':True}

                elif method == 'getBusinessTypes':
                    b = Business()
                    business_types = b.getBusinessTypes(request.data)
                    data = {'data':{'business_types':business_types},'errors':'', 'isSuccess':True}

                elif method == 'getCompanyPositions':
                    p = Position()
                    company_positions = p.getPositions(request.data)
                    data = {'data':{'company_positions':company_positions},'errors':'', 'isSuccess':True}

                elif method == 'getStaffs':
                    s = Staff()
                    staffs = s.getAllStaffs(request.data)
                    data = {'data':{'staffs':staffs},'errors':'', 'isSuccess':True}

                elif method == 'getFeeds':
                    u = User()
                    feeds = u.feeds(request.data)
                    data = {'data':{'feeds':feeds},'errors':'', 'isSuccess':True}

                elif method == 'getStcharges':
                    i = Stcharge()
                    stcharges = i.getStCharges(request.data)
                    data = {'data':{'stcharges':stcharges},'errors':'', 'isSuccess':True}

                elif method == 'tollFreeCalls':
                    i = Tollfree()
                    tollFreeCalls = i.getTollFreeCalls(request.data)
                    data = {'data':{'tollFreeCalls':tollFreeCalls},'errors':'', 'isSuccess':True}

                elif method == 'phoneCalls':
                    i = Phone()
                    phoneCalls = i.getPhoneCalls(request.data)
                    data = {'data':{'phoneCalls':phoneCalls},'errors':'', 'isSuccess':True}

                elif method == 'tollfree':
                    i = Tollfree()
                    tollfree = i.getTollFreeAll(request.data)
                    data = {'data':{'tollfree':tollfree},'errors':'', 'isSuccess':True}

                elif method == 'phones':
                    i = Phone()
                    phones = i.getPhones(request.data)
                    data = {'data':{'phones':phones},'errors':'', 'isSuccess':True}
                    return Response(data, status=status.HTTP_201_CREATED)

                elif method == 'getDefaultPrices':
                    i = Price()
                    prices = i.getDefaultPrices()
                    data = {'data':{'prices_default':prices},'errors':'', 'isSuccess':True}

                elif method == 'createClient':
                    c = Client()
                    client = c.createClient(request.data, response['data']['user_type'])
                    data = {'data':{'client':client},'errors':'', 'isSuccess':True}

                elif method == 'editClient':
                    c = Client()
                    client = c.editClient(request.data)
                    data = {'data':{'client':client},'errors':'', 'isSuccess':True}

                elif method == 'createContact':
                    c = Client()
                    contact = c.createContact(request.data)
                    data = {'data':{'contact':contact},'errors':'', 'isSuccess':True}

                elif method == 'updateContact':
                    c = Client()
                    contact = c.createContact(request.data)
                    data = {'data':{'contact':contact},'errors':'', 'isSuccess':True}

                elif method == 'createPhone':
                    p = Phone()
                    phone = p.createPhones(request.data)
                    data = {'data':{'phone':phone},'errors':'', 'isSuccess':True}

                elif method == 'updatePhone':
                    p = Phone()
                    phone = p.createPhones(request.data)
                    data = {'data':{'phone':phone},'errors':'', 'isSuccess':True}

                elif method == 'createTollfree':
                    t = Tollfree()
                    tollfree = t.createTollfree(request.data)
                    data = {'data':{'tollfree':tollfree},'errors':'', 'isSuccess':True}

                elif method == 'updateTollfree':
                    t = Tollfree()
                    tollfree = t.createTollfree(request.data)
                    data = {'data':{'tollfree':tollfree},'errors':'', 'isSuccess':True}

                elif method == 'createOneOffCharges':
                    t = Stcharge()
                    one_off_charge = s.createOneOffCharges(request.data)
                    data = {'data':{'one_off_charge':one_off_charge},'errors':'', 'isSuccess':True}

                elif method == 'updateOneOffCharges':
                    s = Stcharge()
                    one_off_charge = s.createOneOffCharges(request.data)
                    data = {'data':{'one_off_charge':one_off_charge},'errors':'', 'isSuccess':True}

                elif method == 'getCredits':
                    c = Client()
                    credits = c.getCredits(request.data, response['data']['user_type'])
                    data = {'data':{'credits':credits},'errors':'', 'isSuccess':True}

                elif method == 'getOneOffInvoices':
                    c = Invoice()
                    oneoffinvoices = c.getOneOffInvoices(request.data)
                    data = {'data':{'oneoffinvoices':oneoffinvoices},'errors':'', 'isSuccess':True}

                elif method == 'getOneOffCharges':
                    c = Client()
                    oneoffcharges = c.getOneOffCharges(request.data)
                    data = {'data':{'oneoffcharges':oneoffcharges},'errors':'', 'isSuccess':True}

                elif method == 'getContacts':
                    c = Client()
                    contacts = c.getContacts(request.data)
                    data = {'data':{'contacts':contacts},'errors':'', 'isSuccess':True}

                elif method == 'getClientPhones':
                    p = Phone()
                    client_phones = p.getClientPhones(request.data)
                    data = {'data':{'client_phones':client_phones},'errors':'', 'isSuccess':True}

                elif method == 'getMobiles':
                    p = Phone()
                    client_mobiles = p.getMobiles(request.data)
                    data = {'data':{'client_mobiles':client_mobiles},'errors':'', 'isSuccess':True}

                elif method == 'getLineTypes':
                    l = Linetype()
                    line_types = l.getLineTypes(request.data)
                    data = {'data':{'line_types':line_types},'errors':'', 'isSuccess':True}

                elif method == 'getMobilePlans':
                    p = Plan()
                    mobile_plans = p.getMobilePlans(request.data)
                    data = {'data':{'mobile_plans':mobile_plans},'errors':'', 'isSuccess':True}

                elif method == 'getRatePlans':
                    p = Plan()
                    rate_plans = p.getRatePlans(request.data)
                    data = {'data':{'rate_plans':rate_plans},'errors':'', 'isSuccess':True}

                elif method == 'getMobileGroupPlans':
                    p = Plan()
                    mobile_group_plans = p.getMobileGroupPlans(request.data)
                    data = {'data':{'mobile_group_plans':mobile_group_plans},'errors':'', 'isSuccess':True}

                elif method == 'getServiceProviders':
                    u = User()
                    providers = u.getServiceProviders(request.data)
                    data = {'data':{'providers':providers},'errors':'', 'isSuccess':True}

                elif method == 'getAccountSummary':
                    c = Client()
                    account_summary = c.getAccountSummary(request.data)
                    data = {'data':{'account_summary':account_summary},'errors':'', 'isSuccess':True}

                elif method == 'getTollFree':
                    t = Tollfree()
                    toll_free = t.getTollFree(request.data)
                    data = {'data':{'toll_free':toll_free},'errors':'', 'isSuccess':True}

                elif method == 'getStandingCharges':
                    s = Stcharge()
                    standing_charges = s.getStandingCharges(request.data)
                    data = {'data':{'standing_charges':standing_charges},'errors':'', 'isSuccess':True}

                elif method == 'createStandingCharges':
                    s = Stcharge()
                    standing_charges = s.createStandingCharges(request.data)
                    data = {'data':{'standing_charges':standing_charges},'errors':'', 'isSuccess':True}

                elif method == 'updateStandingCharges':
                    s = Stcharge()
                    standing_charges = s.createStandingCharges(request.data)
                    data = {'data':{'standing_charges':standing_charges},'errors':'', 'isSuccess':True}

                elif method == 'getStaff':
                    s = Staff()
                    staff = s.getStaff(request.data)
                    data = {'data':{'staff':staff},'errors':'', 'isSuccess':True}

                elif method == 'editStaff':
                    s = Staff()
                    staff = s.createStaff(request.data)
                    data = {'data':{'staff':staff},'errors':'', 'isSuccess':True}

                elif method == 'getWhitelabel':
                    c = Client()
                    white_label = c.getWhitelabel(request.data)
                    data = {'data':{'white_label':white_label},'errors':'', 'isSuccess':True}

                elif method == 'createWhiteLabel':
                    c = Client()
                    white_label = c.createWhiteLabel(request.data)
                    data = {'data':{'white_label':white_label},'errors':'', 'isSuccess':True}

                elif method == 'updateWhiteLabel':
                    c = Client()
                    white_label = c.createWhiteLabel(request.data)
                    data = {'data':{'white_label':white_label},'errors':'', 'isSuccess':True}

                elif method == 'clients':
                    c = Client()
                    clients = c.getClientsByStaff(request.data, response['data']['user_type'])
                    data = {'data':{'clients':clients},'errors':'', 'isSuccess':True}

                elif method == 'getClients':

                    c = Client()
                    clients = c.getClientsByStaff(request.data, response['data']['user_type'])
                    data = {'data':{'clients':clients},'errors':'', 'isSuccess':True}

                elif method == 'getInvoices':
                    #  check optional params
                    if 'limit' not in request.data:
                        request.data['limit'] = ""
                    if 'search_str' not in request.data:
                        request.data['search_str'] = ""
                    if 'multi_search_params' not in request.data:
                        request.data['multi_search_params'] = ""

                    i = Invoice()
                    invoices = i.getClientInvoicesByStaff(request.data, response['data']['user_type'])
                    data = {'data':{'invoices':invoices},'errors':'', 'isSuccess':True}

                elif method == 'prices':
                    #  check optional params
                    if 'limit' not in request.data:
                        request.data['limit'] = ""
                    if 'search_str' not in request.data:
                        request.data['search_str'] = ""

                    i = Price()
                    prices = i.getClientPrices(request.data)
                    data = {'data':{'prices':prices},'errors':'', 'isSuccess':True}
                else:
                    i = Fax()
                    faxCharges = i.getFaxCharges(request.data)
                    data = {'data':{'faxCharges':faxCharges},'errors':'', 'isSuccess':True}

                return Response(data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def getRadius(request):
    r = Radius()
    data = r.getRadius()
    return HttpResponse(data)


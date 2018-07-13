from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
# Create a router and register our viewsets with it.
router = DefaultRouter()

schema_view = get_schema_view(title='Restfull API')
# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/$', views.Login.as_view()),
    # url(r'^clients/$', views.Clients.as_view()),
    url(r'^invoices/$', views.Invoices.as_view()),
    url(r'^wl_invoices/$', views.WLInvoices.as_view()),
    url('clients/getClients', views.getClients),
    url('clients/getInvoices', views.getInvoices),
    url('clients/getCredits', views.getCredits),
    url('clients/getOneOffInvoices', views.getOneOffInvoices),
    url('clients/getOneOffCharges', views.getOneOffCharges),
    url('clients/getContacts', views.getContacts),
    url('clients/getClientPhones', views.getClientPhones),
    url('clients/getAccountSummary', views.getAccountSummary),
    url('clients/createContact', views.createContact),
    url('clients/updateContact', views.updateContact),
    url('clients/createPhone', views.createPhone),
    url('clients/updatePhone', views.updatePhone),
    url('clients/updateTollfree', views.updateTollfree),
    url('clients/createTollfree', views.createTollfree),
    url('clients/createStandingCharges', views.createStandingCharges),
    url('clients/updateStandingCharges', views.updateStandingCharges),
    url('clients/updateOneOffCharges', views.updateOneOffCharges),
    url('clients/createOneOffCharges', views.createOneOffCharges),
    url('clients/getPayments', views.getPayments),
    url('clients/getMobiles', views.getMobiles),
    url('clients/getTollFree', views.getTollFree),
    url('clients/getStandingCharges', views.getStandingCharges),
    url('clients/createWhiteLabel', views.createWhiteLabel),
    url('clients/updateWhiteLabel', views.updateWhiteLabel),
    url('clients/create', views.createClient),
    url('clients/edit', views.editClient),
    url('clients/getWhitelabel', views.getWhitelabel),
    url('clients', views.clients),
    url('prices/update', views.updateprices),
    url('prices/getDefaultPrices', views.getDefaultPrices),
    url('prices', views.prices),
    url('phones', views.phones),
    url('stcharges', views.stcharges),
    url('tollfreecalls', views.tollFreeCalls),
    url('tollfree', views.tollfree),
    url('phonecalls', views.phoneCalls),
    url('feeds', views.feeds),
    url('services', views.services),
    url('fax', views.fax),
    url('business/getBusinessTypes', views.getBusinessTypes),
    url('area/getAreaNames', views.getAreaNames),
    url('industry/getIndustries', views.getIndustries),
    url('country/getCountries', views.getCountries),
    url('payment/getPaymentOptions', views.getPaymentOptions),
    url('radius/getRadius', views.getRadius),
    url('positions/getCompanyPositions', views.getCompanyPositions),
    url('linetypes/getLineTypes', views.getLineTypes),
    url('plans/getMobilePlans', views.getMobilePlans),
    url('plans/getMobileGroupPlans', views.getMobileGroupPlans),
    url('plans/getRatePlans', views.getRatePlans),
    url('staff/getAllStaffs', views.staffs),
    url('staff/getStaff', views.getStaff),
    url('staff/editStaff', views.editStaff),
    url('providers/getServiceProviders', views.getServiceProviders),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
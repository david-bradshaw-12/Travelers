from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.login_page),
	url(r'^trips$', views.trips_page),
	url(r'^register$', views.register),
	url(r'logout$', views.log_out),
	url(r'login$', views.login),
	url(r'destination/add$', views.add_destination),
	url(r'destination/$', views.add_destination_page),
	url(r'destination/(?P<id>\d+)$', views.trip_view),
	url(r'destination/(?P<id>\d+)/add$', views.trip_add),
]
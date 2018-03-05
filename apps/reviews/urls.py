from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^success/(?P<num>\d+)$', views.success),
	url(r'^login$', views.login),
	url(r'^register$', views.register),
	url(r'^logout$', views.logout),
	url(r'^add/$', views.add),
	url(r'^create$', views.create),
	url(r'^review_page/(?P<num>\d+)/(?P<num2>\d+)$', views.review_page),
	url(r'^add_review/(?P<num>\d+)/(?P<num2>\d+)$', views.add_review),
	url(r'^profile/(?P<num>\d+)$', views.profile),
	url(r'^delete/(?P<num>\d+)/(?P<num2>\d+)$', views.delete),
]
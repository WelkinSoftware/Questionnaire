from django.conf.urls import patterns, url
from polls2 import views

urlpatterns = patterns('',
	# ex: /polls2/
	url(r'^$', views.index, name='index'),
	# ex: /polls2/5/
	url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
	# ex: /polls2/5/results/
	url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
	# ex: /polls2/5/vote/
	url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
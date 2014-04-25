from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from scrsites import views
from scrsites.books.views import search_form, search
from scrsites.contact.views import contact, contactThanks

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	(r'^search_form/$', search_form),
    (r'^search/$', search),
	(r'^contact/$', contact),
	(r'^contact/thanks/$', contactThanks),
	(r'^$', views.scrnrAdmin), # Staff administrative screen
	(r'^scrn/scrnrAdmin/$', views.scrnrAdmin), # Staff administrative screen
	(r'^scrn/$', views.scrnr, { 'quickExit' : False }), # accumulate risk and pt info then exit
	(r'^scrn/quickExit/$', views.scrnr, {'quickExit' : True }), # Quick exit logic
	(r'^scrn/explanations/(\w+)/$', views.scrnrexpln),
	(r'^scrn/p0/$', views.p0),
	(r'^scrn/p1/$', views.p1),
	(r'^scrn/p2/$', views.p2),
	(r'^scrn/p3/$', views.p3),
	(r'^scrn/p3a/$', views.p3a),
	(r'^scrn/p3b/$', views.p3b),
	(r'^scrn/p3c/$', views.p3c),
	(r'^scrn/p4/$', views.p4),
	(r'^scrn/p4a/$', views.p4a),
	(r'^scrn/p4b/$', views.p4b),
	(r'^scrn/p5/$', views.p5),
	(r'^scrn/aboveAverageRisk/$', views.aboveAverageRisk),
	(r'^scrn/AverageRisk/$', views.AverageRisk),
	(r'^scrn/IndetermRisk/$', views.IndetermRisk),
	(r'^scrn/Completion/$', views.Completion),
	(r'^scrn/setDebugOptions/$', views.setDebugOptions),	
	(r'^display_meta/$', views.display_meta),
	url(r'^polls/', include('polls.urls', namespace="polls")),
	url(r'^polls2/', include('polls2.urls', namespace="polls2")),
	url(r'^multiquest/', include('multiquest.urls', namespace="multiquest")),
	url(r'^sudoku/', include('sudoku.urls', namespace="sudoku")),
    # Examples:
    # url(r'^$', 'scrsites.views.home', name='home'),
    # url(r'^scrsites/', include('scrsites.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

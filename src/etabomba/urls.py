# coding=utf8

from django.conf.urls.defaults import *
from papers import views as papers_views
from accounts import views as accounts_views
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       
    # Home page
    (r'^$', papers_views.home),
    
    # Approve transaction page
    (u'^payment/(?P<p_no>[A-Za-zА-Яа-яЁё0-9]{1,25})/$', papers_views.payment),
    
    # Approve transaction page for Perfect Money requests
    (r'^approve/$', papers_views.approve),
    
    # Register paper page
    (r'^register/$', papers_views.register),
    
    # Set password page
    #(r'^password/$', accounts_views.password),
    
    # Change password page
    #(r'^password/change/$', accounts_views.password_change),
    
    # FAQ page
    (r'^faq/$', papers_views.faq),
    
    # About page
    (r'^about/$', papers_views.about),
    
    # Stats page
    (r'^stats/$', papers_views.stats),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    
)

# Serving static/media files when debug is True
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
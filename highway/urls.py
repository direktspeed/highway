from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'highway.views.index', name='index'),
    url(r'^logout/$', 'highway.views.logout', name='logout'),
    url(r'^manage/$', 'highway.views.manage', name='manage'),
    url(r'^create/$', 'highway.views.create', name='create'),
    url(r'^delete/(\d+)/$', 'highway.views.delete', name='delete'),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social'))
)

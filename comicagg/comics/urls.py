# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url

ajax_patterns = patterns('comicagg.comics.ajax.views',
    url(r'^add_comic/$', 'add_comic', name='add_comic'),
    url(r'^remove_comic/$', 'remove_comic', name='remove_comic'),
    url(r'^remove_comic_list/$', 'remove_comic_list', name='remove_comic_list'),
    url(r'^report_comic/$', 'report_comic', name='report_comic'),

    url(r'^organize/forget/$', 'forget_new_comic', name='forget_new_comic'),
    url(r'^organize/save/$', 'save_selection', name='save'),

    url(r'^mark_read/$', 'mark_read', name='mark_read'),
    url(r'^mark_all_read/$', 'mark_all_read', name='mark_all_read'),
)

admin_patterns = patterns('comicagg.comics.adminviews.views',
    url(r'^update/$', 'admin_update_view', name='update_comics'),
    url(r'^update/(?P<comic_id>\d+)/$', 'admin_update_view', name='update_comic'),
    url(r'^reported/(?P<chids>[\w-]+)/$', 'admin_reported', name='reported'),                    
)

urlpatterns = patterns('comicagg.comics.views',
    url(r'^$', 'read_view', name='index'),
    url(r'^read/$', 'read_view', name='read'),
    url(r'^add/$', 'organize', {'add': True}, name='add'),
    url(r'^organize/$', 'organize', name='organize'),

    url(r'^request/$', 'request_index', name='requests'),

    url(r'^li/(?P<cid>\d+)/', 'last_image_url', name='last_image_url'),
    url(r'^hi/(?P<hid>\d+)/', 'history_image_url', name='history_url'),
    
    (r'^ajax/', include(ajax_patterns, namespace="ajax")),
    (r'^admin/', include(admin_patterns, namespace="admin")),
)



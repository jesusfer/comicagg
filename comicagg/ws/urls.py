from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('comicagg.ws.views',
  url(r'^(?P<user>.*)/unread$', 'unread_user', name='ws_unread_user'),
)
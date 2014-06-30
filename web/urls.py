from django.conf.urls import url, patterns


urlpatterns = patterns('',
    url(r'^$', 'web.views.readability'),
)
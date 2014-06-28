from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^get-user-type$', 'web.views.fake_get_user_type'),
    url(r'^get-browse-datetime$', 'web.views.fake_get_browse_datetime'),
    # url(r'^$', 'xtimr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

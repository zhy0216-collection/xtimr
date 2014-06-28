from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r"^browse$", "web.views.user_post_data"),
    url(r'^get-user-type$', 'web.views.fake_get_user_type'),
    url(r'^get-browse-datetime$', 'web.views.get_browse_datetime'),
    url(r'^label-management$', 'web.views.label_manage'),
    url(r'^create-label$', 'web.views.create_label'),
    # url(r'^$', 'xtimr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r"^test$", "web.views.readability"),
    url(r'^admin/', include(admin.site.urls)),
)

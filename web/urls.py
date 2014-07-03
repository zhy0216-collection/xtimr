from django.conf.urls import url, patterns


urlpatterns = patterns('',
    url(r'^$', 'web.views.readability'),
    url(r"^browse$", "web.views.user_post_data"),
)
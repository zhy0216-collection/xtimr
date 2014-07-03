from django.conf.urls import url, patterns


urlpatterns = patterns('',
    url(r'^$', 'web.views.readability'),
    url(r"^browse$", "web.views.user_post_data"),
    url(r"^show_data_by_category", "web.views.get_browse_datetime_by_category_label"),


)
from django.contrib import admin
from web.models import UrlTime
# Register your models here.

class UrlTimeAdmin(admin.ModelAdmin):
    list_display = ('userid', 'start_time', 
                    'milli_seconds', 'end_time',
                    'web_url', 'domain')


admin.site.register(UrlTime, UrlTimeAdmin)

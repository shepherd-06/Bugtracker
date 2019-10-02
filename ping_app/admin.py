from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput

from ping_app.models import WebStatus


class WebAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }
    search_fields = ["url"]
    show_full_result_count = True
    list_display = ("url", "request_type", "verbose_status",
                    "status", "last_checked")
    list_filter = ("request_type", "status")
    list_display_links = None
    list_per_page = 20


admin.site.register(WebStatus, WebAdmin)

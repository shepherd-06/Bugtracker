from django.forms import TextInput, Textarea
from django.contrib import admin
from error_logger.models import ErrorLog, VerboseLog
from django.db import models

# Register your models here.
# TODO: Add resolved_by name and email in a list to display
# 


class ErrorLogAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }
    search_fields = ['error_name', 'point_of_origin',
                     'resolved_by__email', 'reference_project__project_name']
    show_full_result_count = True
    list_display = ("identifier", "error_name", "error_description",
                    "point_of_origin", "project_name", "is_resolved", "logged_on",)
    list_editable = ("is_resolved", )
    list_filter = ("point_of_origin", "logged_on", "is_resolved",
                   "reference_project__project_name")
    list_display_links = None
    list_max_show_all = 100
    list_per_page = 10


admin.site.register(ErrorLog, ErrorLogAdmin)


class VerboseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }
    search_fields = ['point_of_origin', 'reference_project__project_name']
    show_full_result_count = True
    list_display = ("identifier", "project_name", "log_description",
                    "point_of_origin", "logged_on")
    list_filter = ("point_of_origin", "logged_on",
                   "reference_project__project_name")
    list_display_links = None
    list_max_show_all = 100
    list_per_page = 10


admin.site.register(VerboseLog, VerboseAdmin)

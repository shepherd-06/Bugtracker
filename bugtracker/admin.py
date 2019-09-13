from django.contrib import admin

# Register your models here
from bugtracker.models import *

admin.site.register(User)
admin.site.register(Projects)
admin.site.register(ProjectUpdate)
admin.site.register(Errors)
admin.site.register(ErrorStatus)
admin.site.register(Logs)
admin.site.register(ProjectToken)
admin.site.register(UserToken)
admin.site.register(Organisation)
admin.site.register(UserToOrg)

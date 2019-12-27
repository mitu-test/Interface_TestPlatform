from django.contrib import admin
from .models import Projects, Modules


# Register your models here.
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['id','name','describe','status','create_time']


class ModulesAdmin(admin.ModelAdmin):
    list_display = ['id','name','describe','create_time','project','tester']


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Modules, ModulesAdmin)

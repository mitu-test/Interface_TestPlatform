from django.contrib import admin
from .models import InterfaceCase,TestTask


# Register your models here.

class InterfaceCaseAdmin(admin.ModelAdmin):
    list_display = ['id','module', 'name', 'api', 'describe', 'status', 'method', 'header', 'param_type', 'param_body',
                    'assert_type', 'assert_body', 'maker', 'create_time']


class TestTaskAdmin(admin.ModelAdmin):
    list_display = ['id','name','describe', 'status','cases','create_time']


admin.site.register(InterfaceCase, InterfaceCaseAdmin)
admin.site.register(TestTask, TestTaskAdmin)

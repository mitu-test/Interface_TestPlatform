from django.urls import path

from apitest import views
app_name = "apitest"
urlpatterns = [
     path('case-list/', views.case_list,name='case_list'),
     path('get_modules_name/', views.get_modules_name,name='get_modules_name'),
     path('get_case_message/', views.get_case_message, name='get_case_message'),
     path('case-add/', views.case_add,name='case_add'),
     path('case-edit/', views.case_edit, name='case_edit'),
     path('case-search/', views.case_search, name='case_search'),
     path('case-delete/', views.case_delete, name='case_delete'),
     path('case-run/', views.case_run, name='case_run'),
     path('case-batch-delete/', views.case_batch_delete, name='case_batch_delete'),
     path('task-list/', views.task_list, name='task_list'),
     path('task-add/', views.task_add, name='task_add'),
     path('task-search/', views.task_search, name='task_search'),
     path('task-delete/', views.task_delete, name='task_delete'),
     path('task-batch-delete/', views.task_batch_delete, name='task_batch_delete'),
     path('task-edit/', views.task_edit, name='task_edit'),
     path('get_case_tree/', views.get_case_tree, name='get_case_tree'),
     path('task-run/', views.task_run, name='task_run'),
     path('show-case-report/<int:case_id>/', views.show_case_report, name='show_case_report'),
     path('show-task-report/<int:task_id>/', views.show_task_report, name='show_task_report'),






]

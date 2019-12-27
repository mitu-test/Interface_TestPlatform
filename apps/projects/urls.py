from django.urls import path

from projects import views
app_name = "projects"
urlpatterns = [
    path('list/', views.project_list,name='project_list'),
    path('add/', views.project_add,name='project_add'),
    path('edit/', views.project_edit,name='project_edit'),
    path('search/', views.project_search, name='project_search'),
    path('delete/', views.project_delete,name='project_delete'),
    path('batch-delete/', views.project_batch_delete,name='project_batch_delete'),
    path('module-list/', views.module_list,name='module_list'),
    path('module-search/', views.module_search,name='module_search'),
    path('module-add/', views.module_add,name='module_add'),
    path('module-edit/', views.module_edit,name='module_edit'),
    path('module-delete/', views.module_delete,name='module_delete'),
    path('module-batch-delete/', views.module_batch_delete,name='module_batch_delete'),




]
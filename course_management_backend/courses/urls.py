from django.urls import path
from . import views

urlpatterns = [
    path('courses', views.course_management, name='course_management'),
    path('courses/<str:course_id>', views.view_or_delete_course, name='view_or_delete_course'),
    
    path('instances', views.create_instance, name='create_instance'),
    path('instances/<int:year>/<int:semester>', views.list_instances, name='list_instances'),
    path('instances/<int:year>/<int:semester>/<int:course_id>', views.view_or_delete_instance, name='view_or_delete_instance'),
]

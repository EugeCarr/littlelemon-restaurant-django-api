from django.urls import path, include
from . import views

urlpatterns = [
    path(route='groups/manager/users', 
        view=views.GroupsManagerViewSet.as_view({
           'get': 'list',            
        }),
        name="manager-users"),
]
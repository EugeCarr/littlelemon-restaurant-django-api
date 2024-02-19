from django.urls import path, include
from . import views

urlpatterns = [
    path(route='groups/manager/users', view=views.GroupsManagerViewSet.as_view(), name="manager-users-list"),
    path(route='groups/manager/users/<int:userId>', view=views.GroupsManagerRemoveViewSet.as_view(), name="manager-users-remove"),
    path(route='groups/delivery-crew/users', view=views.GroupsDeliveryViewSet.as_view(), name="manager-users-list"),
    path(route='groups/delivery-crew/users/<int:userId>', view=views.GroupsDeliveryRemoveViewSet.as_view(), name="manager-users-remove"),    
    path(route='menu-items', view=views.MenuItemsListCreateView.as_view(), name="menu-items-view"),
    path(route='menu-items/<int:pk>', view=views.MenuItemSingleView.as_view(), name="menu-items-single-view"),
]
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from . import models
from . import serializers
from .permissions import IsDeliveryCrew, IsManager
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
    
class GroupsManagerViewSet(generics.ListCreateAPIView):   
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
    serializer_class = serializers.GroupsManagerSerializer
    queryset = User.objects.filter(groups__name="Manager")
        
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data.get("username"))
        Group.objects.get(name="Manager").user_set.add(user)
        return Response(data={"message": "User successfully added to managers"},status=201)

class GroupsManagerRemoveViewSet(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = serializers.GroupsManagerSerializer
    queryset = User.objects.filter(groups__name="Manager")
    
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
        return super().get_permissions()
    
    def delete(self,request, userId, *args, **kwargs):
        user = get_object_or_404(User, id=userId)
        Group.objects.get(name="Manager").user_set.remove(user)
        return Response(data={"message": "User successfully removed from Managers group"}, status=200)
    
class GroupsDeliveryViewSet(generics.ListCreateAPIView):   
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
    serializer_class = serializers.GroupsManagerSerializer
    queryset = User.objects.filter(groups__name="Delivery Crew")
        
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data.get("username"))
        Group.objects.get(name="Delivery Crew").user_set.add(user)
        return Response(data={"message": "User successfully added to managers"},status=201)

class GroupsDeliveryRemoveViewSet(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
    serializer_class = serializers.GroupsManagerSerializer
    queryset = User.objects.filter(groups__name="Delivery Crew")
    
    def delete(self,request, userId, *args, **kwargs):
        user = get_object_or_404(User, id=userId)
        Group.objects.get(name="Delivery Crew").user_set.remove(user)
        return Response(data={"message": "User successfully removed from Managers group"}, status=200)
        
class MenuItemsListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.select_related('category').all()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManager| IsAdminUser]
        return[permission() for permission in self.permission_classes]
    
class MenuItemSingleView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.select_related('category').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManager| IsAdminUser]
        return[permission() for permission in self.permission_classes]
    
    
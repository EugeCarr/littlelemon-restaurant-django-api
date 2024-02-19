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
        
    def post(self, request, *args, **kwargs):
        # newUser = request.data
        # print(newUser)
        # serialized_user = serializers.GroupsManagerSerializer(data=newUser, many=False)
        # serialized_user.is_valid(raise_exception=True)
        
        # print(serialized_user.validated_data)
        user = get_object_or_404(User, username=request.data.get("username"))
        Group.objects.get(name="Manager").user_set.add(user)
        return Response(data={"message": "User successfully added to managers"},status=201)

        

from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from typing import Any, List
from . import models
from . import serializers
from rest_framework import viewsets, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from rest_framework.authentication import TokenAuthentication


class AuthGroupMixin(UserPassesTestMixin, AccessMixin):
    raise_exception = True
    groups =[]
    
    def get_permission_denied_message(self) -> str:
        return "You must be a member of the {} group(s)".format(str(self.groups))   

    def test_func(self):
        print("function tested")
        print(self.request)
        print(Group.objects.get(name="Manager").user_set.filter(id=self.request.user.id).exists())
        # return self.request.user.groups.filter(name__in= self.groups ).exists()
        return True
    
class GroupsManagerViewSet(UserPassesTestMixin, AccessMixin, viewsets.ViewSet):   
    groups = ["Manager"]
    raise_exception = True
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]    
    
    def get_permission_denied_message(self) -> str:
        return "You must be a member of the {} group(s)".format(str(self.groups))   

    def test_func(self):
        print(self.request.user)
        return Group.objects.get(name="Manager").user_set.filter(id=self.request.user.id).exists()
    
    def dispatch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        
        return super().dispatch(request, *args, **kwargs)
    
    def list(self):
        queryset = User.objects.filter(groups__name__in=["Manager"])
        serializer = serializers.GroupsManagerSerializer(queryset, many=True)     
        return Response(serializer.data)
        
    def create(self):
        newUser = self.request.body
        print(newUser)
        return Response(data="Calling create api",status=200)

        

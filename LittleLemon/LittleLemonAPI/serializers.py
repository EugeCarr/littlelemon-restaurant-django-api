from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class GroupsManagerSerializer(serializers.ModelSerializer):
    class Meta():
        model= User
        fields = ['username', 'email', 'id']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Category
        fields = "__all__"
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta():
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        depth = 1
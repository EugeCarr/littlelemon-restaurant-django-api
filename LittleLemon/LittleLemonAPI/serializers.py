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
        fields = ["id", "title"]
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta():
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        depth = 1
        extra_kwargs = {
            'price': {'min_value': 0},
        }
 
 
class MenuItemHelperSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.MenuItem
        fields = ['id', 'title', 'category_id']
        depth = 1
               
        
class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'username', 'first_name']

class CartReadSerializer(serializers.ModelSerializer):
    menuItem = MenuItemSerializer(read_only=True)
    menuItem_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta():
        model = models.Cart
        fields = ['id', 'user', 'user_id', 'menuItem', 'menuItem_id', 'price', 'quantity', 'unit_price']
        depth = 1
        extra_kwargs = {
            'price': {'min_value': 0},
            'unit_price': {'min_value': 0},
            'quantity': {'min_value': 0},
        }
        

class OrderItemViewCreateSerializer(serializers.ModelSerializer):
    menuItem = MenuItemHelperSerializer(read_only=True)
    menuItem_id = serializers.IntegerField(write_only=True)
    
    class Meta():
        model = models.OrderItem
        fields = ['menuItem', 'menuItem_id', 'quantity', 'unit_price', 'price']    
        depth   = 2
        extra_kwargs = {
            'price': {'min_value': 0},
            'unit_price': {'min_value': 0},
            'quantity': {'min_value': 0},
        }

class OrderCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)    
    delivery_crew = UserSerializer(read_only=True)
    items = OrderItemViewCreateSerializer(many=True, read_only=True)
    class Meta():
        model = models.Order
        fields = ['id', 'user', 'user_id', 'delivery_crew', 'date', 'total', 'status', 'items',  ]
        extra_kwargs = {
            'total': {'min_value': 0},
        }
        
class OrderUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True, required=False)
    items = OrderItemViewCreateSerializer(many=True, read_only=True)
    
    class Meta():
        model = models.Order
        fields = ['id', 'user', 'delivery_crew_id', 'delivery_crew', 'status', 'items',  ]
        extra_kwargs = {
            'total': {'min_value': 0},
        }
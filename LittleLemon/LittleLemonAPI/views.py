from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from . import models
from . import serializers
from .permissions import IsDeliveryCrew, IsManager, IsCustomer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
    
class GroupsManagerViewSet(generics.ListCreateAPIView):   
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
    serializer_class = serializers.GroupsManagerSerializer
    queryset = User.objects.filter(groups__name="Manager")
        
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data.get("username"))
        Group.objects.get(name="Manager").user_set.add(user)
        return Response(data={"message": "User successfully added to managers"},status=status.HTTP_201_CREATED)

class GroupsManagerRemoveViewSet(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = serializers.GroupsManagerSerializer
    queryset = User.objects.filter(groups__name="Manager")
    
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
        return super().get_permissions()
    
    def delete(self,request, userId, *args, **kwargs):
        user = get_object_or_404(User, id=userId)
        if not user.groups.filter(name="Manager").exists():
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "User is not in Manager Group"})
        Group.objects.get(name="Manager").user_set.remove(user)
        return Response(data={"message": "User successfully removed from Managers group"}, status=status.HTTP_200_OK)
    
class GroupsDeliveryViewSet(generics.ListCreateAPIView):   
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
    serializer_class = serializers.GroupsManagerSerializer
    queryset = User.objects.filter(groups__name="Delivery Crew")
    ordering_fields = ['username']
    search_fields= ['firstName']
        
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data.get("username"))
        Group.objects.get(name="Delivery Crew").user_set.add(user)
        return Response(data={"message": "User successfully added to managers"},status=status.HTTP_201_CREATED)

class GroupsDeliveryRemoveViewSet(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
    serializer_class = serializers.GroupsManagerSerializer
    queryset = User.objects.filter(groups__name="Delivery Crew")
    ordering_fields = ['username']
    search_fields= ['first_name']
    
    def delete(self,request, userId, *args, **kwargs):
        user = get_object_or_404(User, id=userId)
        if not user.groups.filter(name="Delivery Crew").exists():
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "User is not in Delivery Crew Group"})
        Group.objects.get(name="Delivery Crew").user_set.remove(user)
        return Response(data={"message": "User successfully removed from Managers group"}, status=status.HTTP_200_OK)
        
class MenuItemsListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.select_related('category').all()
    ordering_fields = ['category__title', 'title']
    search_fields= ['title']
    
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
    ordering_fields = ['category__title', 'title']
    search_fields= ['title']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManager| IsAdminUser]
        return[permission() for permission in self.permission_classes]
    
class CartManageView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = serializers.CartReadSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['menuItem__title', 'price']
    search_fields= ['menuItem__title']
    
    def get_queryset(self):
        return models.Cart.objects.select_related('menuItem').filter(user_id=self.request.user.id)
    
    def delete(self):
        cartItems = get_object_or_404(models.Cart, user_id=self.request.user.id)
        cartItems.delete()
        return Response(data={"message": "Your cart items were successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    
    def post(self, request, *args, **kwargs):
        existingMenuItem = get_object_or_404(models.MenuItem, id=self.request.data["menuItem_id"])
        cart = {
            "menuItem": existingMenuItem,
            "menuItem_id": self.request.data["menuItem_id"],
            "user_id": self.request.user.id,
            "unit_price": existingMenuItem.price,
            "quantity": self.request.data["quantity"],
            "price":  int(self.request.data["quantity"]) * existingMenuItem.price,
        }
        
        serializedCart = serializers.CartReadSerializer(data=cart)
        serializedCart.is_valid(raise_exception=True)           
                
        try: 
            serializedCart.save()  
        except: 
            return Response({"message": "Item already in cart"}, status=status.HTTP_409_CONFLICT)
        
        return Response(data=serializedCart.data, status=status.HTTP_201_CREATED)
    
class OrderManageView(generics.ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = serializers.OrderCreateSerializer
    ordering_fields = ['date']
    search_fields= ['date', 'user__username']
    
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, IsCustomer]
        else:
            self.permission_classes =[IsAuthenticated]
        return[permission() for permission in self.permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Delivery Crew").exists():
            return models.Order.objects.filter(delivery_crew=user)
        elif user.groups.filter(name="Manager").exists():
            return models.Order.objects.all()
        else: 
            return models.Order.objects.filter(user=user)
        
    def post(self, request, *args, **kwargs):
        userCartItems = models.Cart.objects.filter(user=request.user)  
        cartTotal = 0
        for cart in userCartItems.values():
            cartTotal += cart["price"]
        orderDetails = {
            "total": cartTotal,
            "date": datetime.now().date(),
            "status": 0,
            "user_id": request.user.id
        }        
        serialzed_order = serializers.OrderCreateSerializer(data=orderDetails)
        print(serialzed_order.initial_data)
        serialzed_order.is_valid(raise_exception=True)
        
        try:
            serialzed_order.save()
            print(serialzed_order.data)  
            new_order_id = serialzed_order.data["id"]      
            print(new_order_id)
            newOrderItems = []  
            for cartItem in userCartItems.values():
                orderItem = models.OrderItem.objects.create(
                    order_id = new_order_id,
                    menuItem_id = cartItem["menuItem_id"],
                    quantity = cartItem["quantity"],
                    price = cartItem["price"],
                    unit_price = cartItem["unit_price"]
                )
                newOrderItems.append(orderItem)
        except: 
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "An order already exists for this user"})
        userCartItems.delete()
        createdOrderItems =models.OrderItem.objects.select_related('menuItem').filter(order_id=new_order_id).values()
        return Response(status=status.HTTP_201_CREATED, data={
            "order": serialzed_order.data,
            "items": createdOrderItems
        })
        
class OrderSingleManageView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated, IsCustomer| IsDeliveryCrew| IsAdminUser]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated, IsManager]
        elif self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [IsAuthenticated, IsManager| IsDeliveryCrew| IsAdminUser]
        return[permission() for permission in self.permission_classes]        
    
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name="Delivery Crew").exists():
            return models.Order.objects.filter(delivery_crew=user).filter(id=self.kwargs['pk'])
        else:
            return models.Order.objects.filter(id=self.kwargs['pk'])
        
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            self.serializer_class = serializers.OrderUpdateSerializer
        else: 
            self.serializer_class= serializers.OrderCreateSerializer
        return self.serializer_class
    
    def put(self, request, pk, *args, **kwargs):
        self.serializer_class = serializers.OrderUpdateSerializer
        existingOrder = get_object_or_404(models.Order, pk=pk)
        print(request.data)
        serialized_order = serializers.OrderUpdateSerializer(data=request.data)
        serialized_order.is_valid(raise_exception=True)      
                 
        try:            
            if request.user.groups.filter(name="Delivery Crew").exists():
                existingOrder.status = not existingOrder.status
            else:
                existingOrder.status = serialized_order.initial_data["status"]   
                delivery_crew = User.objects.get(pk=serialized_order.initial_data["delivery_crew_id"])             
                if not delivery_crew:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Delivery crew member does not exist"})
                existingOrder.delivery_crew_id = serialized_order.initial_data["delivery_crew_id"]
            existingOrder.save()
                
        except: 
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Order data incorrect"})
        
        if int(existingOrder.status) == 1:
            orderStatus = "Delivered"
        else:
            orderStatus = "Ordered"
        return Response(status=status.HTTP_201_CREATED, data={
            "message": "Order {} for {}, on {} has been set to {}. The delivery crew member is {}".format(
                pk,
                existingOrder.user.username,
                existingOrder.date,
                orderStatus,
                existingOrder.delivery_crew.username,
            )
        })
        
    def patch(self, request, pk, *args, **kwargs):
        return self.put( request, pk, *args, **kwargs)
            
        
        
    
    
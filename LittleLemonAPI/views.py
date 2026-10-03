from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import MenuItem
from .serializers import MenuItemSerializer
from .permissions import IsManager
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import Cart, MenuItem
from .serializers import CartSerializer
from .permissions import IsCustomer
from django.utils import timezone
from .models import Order, OrderItem, Cart
from .serializers import OrderSerializer, OrderItemSerializer
from .permissions import IsCustomer, IsManager, IsDeliveryCrew

class MenuItemsView(generics.ListCreateAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    filterset_fields = ['category', 'featured']
    search_fields = ['title', 'category__title']
    ordering_fields = ['price', 'title']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]

        return [IsManager()]

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]

        return [IsManager()]    

class ManagerUsersView(generics.ListCreateAPIView):

    permission_classes = [IsManager]

    def get_queryset(self):
        manager_group = Group.objects.get(name='Manager')
        return User.objects.filter(groups=manager_group)

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()

        return Response([
            {
                'id': user.id,
                'username': user.username
            }
            for user in users
        ])

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')

        if not username:
            return Response(
                {'error': 'Username is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        manager_group = Group.objects.get(name='Manager')
        manager_group.user_set.add(user)

        return Response(
            {
                'message': f'{username} added to Manager group'
            },
            status=status.HTTP_201_CREATED
        )
class ManagerUserDetailView(generics.DestroyAPIView):

    permission_classes = [IsManager]

    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        manager_group = Group.objects.get(name='Manager')
        manager_group.user_set.remove(user)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
class DeliveryCrewUsersView(generics.ListCreateAPIView):

    permission_classes = [IsManager]

    def get_queryset(self):
        delivery_group = Group.objects.get(name='Delivery crew')
        return User.objects.filter(groups=delivery_group)

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()

        return Response([
            {
                'id': user.id,
                'username': user.username
            }
            for user in users
        ])

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')

        if not username:
            return Response(
                {'error': 'Username is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        delivery_group = Group.objects.get(name='Delivery crew')
        delivery_group.user_set.add(user)

        return Response(
            {
                'message': f'{username} added to Delivery crew group'
            },
            status=status.HTTP_201_CREATED
        )
class DeliveryCrewUserDetailView(generics.DestroyAPIView):

    permission_classes = [IsManager]

    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        delivery_group = Group.objects.get(name='Delivery crew')
        delivery_group.user_set.remove(user)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
class CartView(generics.ListCreateAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        menuitem = serializer.validated_data['menuitem']
        quantity = serializer.validated_data['quantity']

        unit_price = menuitem.price
        price = unit_price * quantity

        serializer.save(
            user=self.request.user,
            unit_price=unit_price,
            price=price
        )

    def delete(self, request, *args, **kwargs):
        Cart.objects.filter(user=request.user).delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
class OrdersView(generics.ListCreateAPIView):

    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomer()]

        return [
            IsCustomer() |
            IsManager() |
            IsDeliveryCrew()
        ]

    def get_queryset(self):

        user = self.request.user

        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()

        if user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(
                delivery_crew=user
            )

        return Order.objects.filter(
            user=user
        )

    def perform_create(self, serializer):

        cart_items = Cart.objects.filter(
            user=self.request.user
        )

        total = sum(
            item.price
            for item in cart_items
        )

        order = serializer.save(
            user=self.request.user,
            total=total,
            date=timezone.now().date()
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )

        cart_items.delete()
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):

        user = self.request.user

        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()

        if user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(
                delivery_crew=user
            )

        return Order.objects.filter(
            user=user
        )

    def get_permissions(self):

        if self.request.method == 'GET':
            return [
                IsCustomer() |
                IsManager() |
                IsDeliveryCrew()
            ]

        if self.request.method == 'DELETE':
            return [IsManager()]

        return [
            IsManager() |
            IsDeliveryCrew()
        ]

    def update(self, request, *args, **kwargs):

        order = self.get_object()

        user = request.user

        # Delivery crew can only change status
        if user.groups.filter(name='Delivery crew').exists():

            if 'status' not in request.data:
                return Response(
                    {'error': 'Delivery crew can only update status'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order.status = request.data['status']
            order.save()

            return Response(
                OrderSerializer(order).data
            )

        # Manager
        if user.groups.filter(name='Manager').exists():

            if 'delivery_crew' in request.data:

                try:
                    crew = User.objects.get(
                        id=request.data['delivery_crew']
                    )
                except User.DoesNotExist:
                    return Response(
                        {'error': 'Delivery crew not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                if not crew.groups.filter(
                    name='Delivery crew'
                ).exists():

                    return Response(
                        {'error': 'User is not delivery crew'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                order.delivery_crew = crew

            if 'status' in request.data:
                order.status = request.data['status']

            order.save()

            return Response(
                OrderSerializer(order).data
            )

        return Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN
        )
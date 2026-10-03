from django.urls import path

from .views import (
    MenuItemsView,
    MenuItemDetailView,
    ManagerUsersView,
    ManagerUserDetailView,
    DeliveryCrewUsersView,
    DeliveryCrewUserDetailView,
    CartView,
    OrdersView,
    OrderDetailView,
)


urlpatterns = [

    # Menu
    path(
        'menu-items',
        MenuItemsView.as_view()
    ),

    path(
        'menu-items/<int:pk>',
        MenuItemDetailView.as_view()
    ),

    # Manager group
    path(
        'groups/manager/users',
        ManagerUsersView.as_view()
    ),

    path(
        'groups/manager/users/<int:pk>',
        ManagerUserDetailView.as_view()
    ),

    # Delivery crew group
    path(
        'groups/delivery-crew/users',
        DeliveryCrewUsersView.as_view()
    ),

    path(
        'groups/delivery-crew/users/<int:pk>',
        DeliveryCrewUserDetailView.as_view()
    ),
    path(
    'cart/menu-items',
    CartView.as_view()
),
path(
    'orders',
    OrdersView.as_view()
),

path(
    'orders/<int:pk>',
    OrderDetailView.as_view()
),
]

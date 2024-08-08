from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path("home", HomeView.as_view(), name="chome"),
    path("prod/<str:cat>/", ProductView.as_view(), name="prod"),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='det'),
    path('cart/', cart_view, name='cart_view'),
    path('add_to_cart/<pk>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<pk>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<pk>/', update_cart_item, name='update_cart_item'),
    path('wishlist/', Wishlist_view, name='wishlist_view'),
    path('add_to_wishlist/<int:pk>/', add_to_wishlist, name='add_to_wishlist'),
    path('checkout/', checkout_view, name='checkout_view'),
    path('place_order/', place_order, name='place_order'),
    path('order_success/<int:order_id>/', order_success, name='order_success'),
    path('order_details/<pk>/', order_details, name='order_details'),

   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



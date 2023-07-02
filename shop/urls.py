from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='productdetail'),
    path('product/new/', ProductCreateView.as_view(), name='productcreate'),
    path('product/edit/<int:pk>/', ProductUpdateView.as_view(), name='productupdate'),
    path('search/', SearchView.as_view(), name='search'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name="categorydetail"),
    path('category/new/', CategoryCreateView.as_view(), name='categorycreate'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='categoryupdate'),
    path('city/', CityVeiw.as_view(), name='cities'),
    path('city/<int:pk>/', CityDetailView.as_view(), name='citydetail'),
    path('addtocart/', addToCart, name='addtocart'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('inventory/delete/<int:pk>/', InventoryDeleteView.as_view(), name='inventorydelete'),
    path('inventory/update/<int:pk>/', InventoryUpdateView.as_view(), name='inventoyupdate'),
    path('inventory/new/', InventoryCreateView.as_view(), name='inventorycreate'),
    path('inventoryproduct/', InventoryProductListView.as_view(), name='inventoryproduct'),
    path('inventoryproduct/new/', InventoryProductCreateView.as_view(), name='inventoryproductcreate'),
    path('inventoryproduct/delete/<int:pk>/', InventoryProductDeleteView.as_view(), name='inventoryproductdelete'),
    path('inventoryproduct/edit/<int:pk>', InventoryProductUpdateView.as_view(), name='inventoryproductupdate'),
    path('cart/<int:pk>/',CartDetailView.as_view(),name='cartdetail'),
    path('updatcart/<int:cartItemId>/',updateCart,name='updatcart'),
    path('deletefromcart/<int:cartItemId>/',deletFromCart,name='deletefromcart'),
    path('ordercreat/',orderCreate,name='ordercreate'),
    path('aboutus/',AboutUsView.as_view(),name='aboutus'),
    path('orders/',OrderListVeiw.as_view(),name='orders'),
    path('orders/update/<int:pk>/',OrderUpdate.as_view(),name='orderupdate')
]

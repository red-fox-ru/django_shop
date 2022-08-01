from django.urls import path

from shop import views

urlpatterns = [
    path('', views.base, name='home'),
    path('products/<str:ct_model>/<str:slug>', views.ProductDetailView.as_view(), name='product_detail'),
]

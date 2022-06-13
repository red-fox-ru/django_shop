from django.urls import path

from shop import views

urlpatterns = [
    path('', views.base, name='home'),
]

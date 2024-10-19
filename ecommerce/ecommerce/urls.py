# ecommerce/urls.py

from django.contrib import admin
from django.urls import path
from tienda import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('carrito/', views.carrito, name='carrito'),
    path('pagar/', views.pagar, name='pagar'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('menu.html', views.menu_html, name='menu_html'),
]

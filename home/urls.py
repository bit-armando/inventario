from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-product/', views.add_product, name='add_product'),
    path('registrar-entrada/', views.registrar_entrada, name='registrar_entrada'),
]

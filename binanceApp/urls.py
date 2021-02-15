from django.urls import path
from binanceApp import views
app_name = 'binanceApp'


urlpatterns = [
    path('', views.order_list, name="order_list"),
    path('ma/', views.ma, name='ma'),
    path('order/create/', views.order_create, name='order_create')
    ]
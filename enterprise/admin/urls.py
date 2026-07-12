from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.index, name='admin_index'),
    path('assets/', views.assets, name='admin_assets'),
    path('allocations/', views.allocations, name='admin_allocations'),
    path('bookings/', views.bookings, name='admin_bookings'),
    path('transfers/', views.transfers, name='admin_transfers'),
]

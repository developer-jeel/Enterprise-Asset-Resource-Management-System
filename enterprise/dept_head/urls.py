from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dh_index'),
    path('assets/', views.assets, name='dh_assets'),
    path('allocations/', views.allocations, name='dh_allocations'),
    path('transfers/', views.transfers, name='dh_transfers'),
    path('bookings/', views.bookings, name='dh_bookings'),
]

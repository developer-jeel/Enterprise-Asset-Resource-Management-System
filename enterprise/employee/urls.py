from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='emp_index'),
    path('assets/', views.assets, name='emp_assets'),
    path('allocations/', views.allocations, name='emp_allocations'),
    path('transfers/', views.transfers, name='emp_transfers'),
    path('bookings/', views.bookings, name='emp_bookings'),
]

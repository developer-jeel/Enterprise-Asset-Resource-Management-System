from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='mgr_index'),
    path('assets/', views.assets, name='mgr_assets'),
    path('allocations/', views.allocations, name='mgr_allocations'),
    path('transfers/', views.transfers, name='mgr_transfers'),
    path('bookings/', views.bookings, name='mgr_bookings'),
]

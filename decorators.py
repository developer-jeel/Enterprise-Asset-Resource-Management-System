from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='manager_index'),
    path('index.html', views.index, name='manager_index_html'),
    path('get_dashboard_data/', views.get_dashboard_data, name='manager_dashboard_data'),
    path('assets/', views.assets_view, name='manager_assets'),
    path('assets.html', views.assets_view, name='manager_assets_html'),
    path('save_asset/', views.save_asset, name='manager_save_asset'),
    path('retire_asset/', views.retire_asset, name='manager_retire_asset'),
    path('transfers/', views.transfers_view, name='manager_transfers'),
    path('transfers.html', views.transfers_view, name='manager_transfers_html'),
    path('handle_allocation/', views.handle_allocation, name='manager_handle_allocation'),
    path('handle_transfer/', views.handle_transfer, name='manager_handle_transfer'),
    path('maintenance/', views.maintenance_view, name='manager_maintenance'),
    path('maintenance.html', views.maintenance_view, name='manager_maintenance_html'),
    path('handle_maintenance/', views.handle_maintenance, name='manager_handle_maintenance'),
    path('discrepancies/', views.discrepancies_view, name='manager_discrepancies'),
    path('discrepancies.html', views.discrepancies_view, name='manager_discrepancies_html'),
    path('resolve_discrepancy/', views.resolve_discrepancy, name='manager_resolve_discrepancy'),
    path('returns/', views.returns_view, name='manager_returns'),
    path('returns.html', views.returns_view, name='manager_returns_html'),
    path('handle_return/', views.handle_return, name='manager_handle_return'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='employee_index'),
    path('index.html', views.index, name='employee_index_html'),
    path('get_dashboard_data/', views.get_dashboard_data, name='employee_dashboard_data'),
    path('assets/', views.assets_view, name='employee_assets'),
    path('assets.html', views.assets_view, name='employee_assets_html'),
    path('bookings/', views.bookings_view, name='employee_bookings'),
    path('bookings.html', views.bookings_view, name='employee_bookings_html'),
    path('create_booking/', views.create_booking, name='employee_create_booking'),
    path('cancel_booking/', views.cancel_booking, name='employee_cancel_booking'),
    path('maintenance/', views.maintenance_view, name='employee_maintenance'),
    path('maintenance.html', views.maintenance_view, name='employee_maintenance_html'),
    path('report_issue/', views.report_issue, name='employee_report_issue'),
    path('requests/', views.requests_view, name='employee_requests'),
    path('requests.html', views.requests_view, name='employee_requests_html'),
    path('submit_request/', views.submit_request, name='employee_submit_request'),

    path('profile/', views.profile_view, name='employee_profile'),
    path('profile.html', views.profile_view, name='employee_profile_html'),
    path('get_profile_data/', views.get_profile_data, name='employee_profile_data'),
    path('update_profile/', views.update_profile, name='employee_update_profile'),
    path('change_password/', views.change_password, name='employee_change_password'),

    path('notifications/', views.notifications_view, name='employee_notifications'),
    path('notifications.html', views.notifications_view, name='employee_notifications_html'),
    path('get_notifications_data/', views.get_notifications_data, name='employee_notifications_data'),
    path('mark_notification_read/', views.mark_notification_read, name='employee_mark_notification_read'),

    path('leave/', views.leave_view, name='employee_leave'),
    path('leave.html', views.leave_view, name='employee_leave_html'),
    path('get_leave_data/', views.get_leave_data, name='employee_leave_data'),
    path('submit_leave/', views.submit_leave, name='employee_submit_leave'),
    path('cancel_leave/', views.cancel_leave, name='employee_cancel_leave'),
]

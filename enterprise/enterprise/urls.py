from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Django's built-in admin
    path('admin/', include('admin.urls')),    # Custom AssetFlow admin panel
    path('dept-head/', include('dept_head.urls')),  # Department Head panel
    path('manager/', include('manager.urls')),      # Manager panel
    path('employee/', include('employee.urls')),    # Employee panel
]

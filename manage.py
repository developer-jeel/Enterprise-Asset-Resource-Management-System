from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django_admin/', admin.site.urls),  # Django's built-in admin site (django.contrib.admin)
    path('', include('admin_portal.urls')),  # Custom Admin role portal: root redirect / login / logout / admin dashboard
    path('manager/', include('manager.urls')),
    path('employee/', include('employee.urls')),
    path('dept_head/', include('dept_head.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

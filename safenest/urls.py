from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('api/', include('api.urls')),

    # Smart Home IoT Features
    path('devices/', include('devices.urls')),
    path('security/', include('security.urls')),
    path('energy/', include('energy.urls')),
    path('automation/', include('automation.urls')),

    # AI Architecture & Design Features
    path('ai/', include('ai_assistant.urls')),
    path('architecture/', include('architecture.urls')),
    path('design/', include('design.urls')),
    path('materials/', include('materials.urls')),
    path('architects/', include('architects.urls')),
    path('consultation/', include('consultation.urls')),

    # User & Profile Management
    path('accounts/', include('accounts.urls')),
    path('profile/', include('profile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# campusconnect_project/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts.views import landing_view  # import your landing view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_view, name='landing'),  # <-- simple function view (NOT .as_view())
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

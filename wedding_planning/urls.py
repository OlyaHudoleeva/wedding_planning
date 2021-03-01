from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('overview', include('main.urls')),
    path('guests', include('main.urls')),
    path('checklist', include('main.urls')),
    path('budget', include('main.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)

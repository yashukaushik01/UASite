from django.contrib import admin
from django.urls import include, path
from . import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('product.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
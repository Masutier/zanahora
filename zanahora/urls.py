from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "ZanaHora Admin"
admin.site.site_title = "ZanaHora Admin"
admin.site.index_title = "Welcome To ZanaHora Admin"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cupons.urls')),
    path('', include('mainAdmin.urls')),
    path('', include('orders.urls')),
    path('', include('products.urls')),
    path('', include('projects.urls')),
    path('', include('users.urls')),
    path('', include('zanamain.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

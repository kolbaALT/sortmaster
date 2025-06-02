from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from sortmaster import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('about/', core_views.about, name='about'),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('algorithms/', include('algorithms.urls')),
    path('challenges/', include('challenges.urls')),
    path('content/', include('content.urls')),
    path('career/', include('career.urls')),
]

# Добавляем обслуживание медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


from django.contrib import admin
from django.urls import path, include
from feed.views import home, custom_404
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("feed.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'feed.views.custom_404'
handler500 = 'feed.views.custom_404'

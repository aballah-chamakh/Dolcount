from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from object import urls
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(urls)),
]
if settings.DEBUG :
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    #urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

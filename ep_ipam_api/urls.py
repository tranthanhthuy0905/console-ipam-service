from django.conf import settings
from django.conf.urls import url
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view

from ep_ipam_api.ipam.apis import ResourceIPViewSet

router = DefaultRouter(trailing_slash=False)
router.register('ipams', ResourceIPViewSet, basename='ipams')

schema_view = get_schema_view(
    openapi.Info(
        title="Engineering Platform IPAM API",
        default_version='v1',
        description="API for interaction with Netbox",
        contact=openapi.Contact(email="sangcv@vng.com.vn"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include(router.urls)),
                  path('api-token-auth/', views.obtain_auth_token),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                      name='schema-json'),
                  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

                  # the 'api-root' from django rest-frameworks default router
                  # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
                  re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

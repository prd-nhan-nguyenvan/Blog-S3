from django.conf import settings  # new
from django.conf.urls.static import static  # new
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi  # new foe swagger
from drf_yasg.views import \
    get_schema_view as swagger_get_schema_view  # new foe swagger

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Blogs API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0),
         name="swagger-schema" ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_URL)

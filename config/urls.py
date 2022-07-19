
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('as_admin/', admin.site.urls),
    path('catalog/', include('core_apps.catalog.urls', namespace='catalog')),
    path('reader/', include('core_apps.reader.urls', namespace='reader')),
    path('', include('projects.urls', namespace='projects')),


]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

#urlpatterns += [
#    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
#]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('lms/', include('lms.urls', namespace='lms')),
                  path('users/', include('users.urls', namespace='user')),
              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)

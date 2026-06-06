from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', include('core.urls')),
    path('services/', include('services.urls')),
    path('blog/', include('blog.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('faq/', include('faq.urls')),
]

# Ensure media files are served even in production if Cloudinary is not used
from django.urls import re_path
from django.views.static import serve

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]


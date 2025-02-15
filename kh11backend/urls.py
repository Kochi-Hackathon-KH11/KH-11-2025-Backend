from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', include('temp.urls')),
    path('audio/', include('audio.urls')),
    path('auth/', include('user.urls')),
]

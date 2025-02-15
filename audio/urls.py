from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import AudioUploadView

urlpatterns = format_suffix_patterns([
    path('', AudioUploadView.as_view()),
])

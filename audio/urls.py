from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import AudioUploadView

urlpatterns = format_suffix_patterns([
    path('file/', AudioUploadView.as_view()),
    # path('stream/', AudioStreamView.as_view()),
])

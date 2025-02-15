from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views 


urlpatterns = format_suffix_patterns([
    path('', views.HelloWorld.as_view()),
])


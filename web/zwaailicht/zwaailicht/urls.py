"""
zwaailicht URL Configuration
"""
from django.conf.urls import url, include

import api.urls
from api import views

urlpatterns = [
    url(r'^status/health', views.health_check),
    url(r'^zwaailicht/', include(api.urls.router.urls)),
    url(r'^zwaailicht/docs/', include('rest_framework_swagger.urls')),
]

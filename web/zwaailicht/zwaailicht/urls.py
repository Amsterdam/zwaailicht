"""
zwaailicht URL Configuration
"""
from django.conf.urls import url, include

import api.urls

urlpatterns = [
    url(r'^zwaailicht/', include(api.urls.router.urls)),
]

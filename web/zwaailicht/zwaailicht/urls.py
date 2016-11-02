"""
zwaailicht URL Configuration
"""
from django.conf.urls import url, include
from rest_framework import renderers, schemas, response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer

import api.urls
from api import views


@api_view()
@renderer_classes(
    [SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Zwaailicht API')
    return response.Response(generator.get_schema(request=request))


urlpatterns = [
    url(r'^status/health', views.health_check),
    url(r'^zwaailicht/', include(api.urls.router.urls)),
    url('^zwaailicht/docs/api-docs/$', schema_view),
]

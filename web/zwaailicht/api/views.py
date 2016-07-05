from rest_framework import viewsets
from rest_framework.response import Response

from . import mapping


class PandStatusViewSet(viewsets.ViewSet):
    """
    De pand status geeft een overzicht van eigenschappen van het pand.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapping = mapping.Mapping()

    def list(self, request):
        return Response("Gebruik de url /status_pand/{bag_id} om gedetailleerde informatie terug te krijgen.")

    def retrieve(self, request, pk=None):
        return Response(data={
            'locatie': {
                'bag_id': pk,
            },
            'indicatoren': [
                self.mapping.beperking_to_status_pand('HS'),
            ],
        })

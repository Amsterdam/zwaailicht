from rest_framework import viewsets
from rest_framework.response import Response


class PandStatusViewSet(viewsets.ViewSet):
    """
    De pand status geeft een overzicht van eigenschappen van het pand.
    """

    def list(self, request):
        return Response("Gebruik de url /pand_status/{bag_id} om gedetailleerde informatie terug te krijgen.")

    def retrieve(self, request, pk=None):
        return Response(data={
            'locatie': {
                'bag_id': pk,
            },
            'indicatoren': [

            ],
        })

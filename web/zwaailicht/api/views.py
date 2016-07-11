import json

from django.http import HttpResponse, Http404
from rest_framework import viewsets
from rest_framework.response import Response

from . import client
from . import mapping


class MappingViewSet(viewsets.ViewSet):
    """
    Dit JSON document wordt gebruikt om verschillende codes te mappen naar indicatoren. Gebruik onderstaand
    bestand als uitgangspunt indien er wijzigingen nodig zijn.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapping = mapping.Mapping()

    def list(self, request, **kwargs):
        return Response(self.mapping.json())


class PandStatusViewSet(viewsets.ViewSet):
    """
    De pand status geeft een overzicht van eigenschappen van de panden die horen bij dit verblijfsobject.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapping = mapping.Mapping()
        self.client = client.Client()

    def list(self, request):
        return Response("Gebruik de url /status_pand/{bag_id} om gedetailleerde informatie terug te krijgen.")

    def retrieve(self, request, pk=None):
        indicatoren = []

        vbo = self.client.get_vbo(pk)
        if not vbo:
            raise Http404()

        panden = self.client.get_panden(vbo)
        pand_status = [p.pand_status for p in panden]
        for s in pand_status:
            mapped = self.mapping.pand_status_to_status_pand(s)
            if mapped:
                indicatoren.append(mapped)

        beperkingen = self.client.get_beperkingen(vbo)
        beperking_codes = [b.beperking for b in beperkingen]
        for c in beperking_codes:
            mapped = self.mapping.beperking_to_status_pand(c)
            if mapped:
                indicatoren.append(mapped)

        return Response(data={
            'locatie': {
                'bag_id': pk,
            },
            'indicatoren': indicatoren,
        })


class GebruikViewSet(viewsets.ViewSet):
    """
    Gebruik geeft informatie over het daadwerkelijk gebruik van een verblijfsobject.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapping = mapping.Mapping()
        self.client = client.Client()

    def list(self, request):
        return Response("Gebruik de url /gebruik/{bag_id} om gedetailleerde informatie terug te krijgen.")

    def retrieve(self, request, pk=None):
        return Response(data={
            'locatie': {
                'bag_id': pk,
            },
            'indicatoren': []
        })


def health_check(request):
    result = "OK"
    status = 200

    return HttpResponse(json.dumps(result),
                        status=status,
                        content_type="application/json")

import json

from django.http import HttpResponse, Http404
from rest_framework import viewsets, serializers
from rest_framework.response import Response

from . import client
from . import mapping


# Note: these serializers are NEVER ACTUALLY USED. They are here so the Swagger generator
# behaves as it should
class Locatie(serializers.Serializer):
    bag_id = serializers.CharField(min_length=16, max_length=16, help_text="Het opgevraagde BAG ID")


class Indicator(serializers.Serializer):
    indicator = serializers.ChoiceField(("pand_status", "gebruik",), help_text="Opgevraagde indicator")

    waarschuwingsniveau = serializers.IntegerField(
        help_text="1 (let op) of 2 (belangrijk). Originele indicatoren met waarde 0 worden nooit teruggegeven")

    label = serializers.CharField(help_text="Korte toelichtende tekst")
    aanvullende_informatie = serializers.CharField()


class Result(serializers.Serializer):
    locatie = Locatie(help_text="Een kopie van de originele opgevraagde locatie-gegevens")
    indicatoren = Indicator(many=True, help_text="Een lijst met eventuele indicatoren voor dit verblijfsobject")


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
        """
        ---
        parameters:
           - name: pk
             description: Landelijk BAG ID van een verblijfsobject
             required: true
             type: string
             paramType: path
        serializer: Result
        """
        indicatoren = []

        vbo = self.client.get_vbo(pk)
        if not vbo:
            raise Http404()

        panden = self.client.get_panden(vbo)
        pand_status = [p.pand_status for p in panden]
        for s in pand_status:
            mapped = self.mapping.map_pand_status(s)
            if mapped:
                indicatoren.append(mapped)

        beperkingen = self.client.get_beperkingen(vbo)
        beperking_codes = [b.beperking for b in beperkingen]
        for c in beperking_codes:
            mapped = self.mapping.map_beperking(c)
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
        """
        ---
        parameters:
           - name: pk
             description: Landelijk BAG ID van een verblijfsobject
             required: true
             type: string
             paramType: path
        serializer: Result
        """
        indicatoren = []

        vbo = self.client.get_vbo(pk)
        if not vbo:
            raise Http404()

        gebruiksdoel = vbo.gebruiksdoel
        mapped = self.mapping.map_gebruiksdoel(gebruiksdoel)
        if mapped:
            indicatoren.append(mapped)

        gebruikscode = vbo.gebruikscode
        mapped = self.mapping.map_gebruikscode(gebruikscode)
        if mapped:
            indicatoren.append(mapped)

        return Response(data={
            'locatie': {
                'bag_id': pk,
            },
            'indicatoren': indicatoren
        })


class BouwlagenViewSet(viewsets.ViewSet):
    """
    Bouwlagen geeft informatie over het aantal bouwlagen van een verblijfsobject.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapping = mapping.Mapping()
        self.client = client.Client()

    def list(self, request):
        return Response("Gebruik de url /bouwlagen/{bag_id} om gedetailleerde informatie terug te krijgen.")

    def retrieve(self, request, pk=None):
        indicatoren = []

        vbo = self.client.get_vbo(pk)
        if not vbo:
            raise Http404()

        aantal_bouwlagen = vbo.aantal_bouwlagen
        mapped = self.mapping.map_aantal_bouwlagen(aantal_bouwlagen)
        if mapped:
            indicatoren.append(mapped)

        verdieping_toegang = vbo.verdieping_toegang
        mapped = self.mapping.map_verdieping_toegang(verdieping_toegang)
        if mapped:
            indicatoren.append(mapped)

        return Response(data={
            'locatie': {
                'bag_id': pk,
            },
            'indicatoren': indicatoren,
        })


def health_check(request):
    result = "OK"
    status = 200

    return HttpResponse(json.dumps(result),
                        status=status,
                        content_type="application/json")

from rest_framework import routers

from . import views


class ZwaailichtRouter(routers.DefaultRouter):
    """
    De Zwaailicht Service biedt notificaties voor de landelijke Berichtendienst. Op basis van een BAG ID worden
    nul of meer indicatoren teruggegeven die ondersteunende informatie over het betreffende pand bieden.
    """

    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class ZwaailichtService(cls):
            pass

        ZwaailichtService.__doc__ = self.__doc__
        return ZwaailichtService.as_view()


router = ZwaailichtRouter()
router.register('mapping', views.MappingViewSet, base_name='mapping')
router.register('status_pand', views.PandStatusViewSet, base_name='status_pand')
router.register('gebruik', views.GebruikViewSet, base_name='gebruik')
router.register('bouwlagen', views.BouwlagenViewSet, base_name='bouwlagen')

from rest_framework import routers
from . import views


class ZwaailichtRouter(routers.DefaultRouter):
    """
    De Zwaailicht Service biedt notificaties voor de landelijke Berichtendienst. Op basis van een BAG ID worden
    nul of meer indicatoren teruggegeven die ondersteunende informatie over het betreffende pand bieden.
    """

    def get_api_root_view(self):
        view = super().get_api_root_view()
        cls = view.cls

        class ZwaailichtService(cls):
            pass

        ZwaailichtService.__doc__ = self.__doc__
        return ZwaailichtService.as_view()


router = ZwaailichtRouter()
router.register('pand_status', views.PandStatusViewSet, base_name='pand_status')



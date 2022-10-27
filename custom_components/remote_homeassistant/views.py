import homeassistant
from homeassistant.components.http import HomeAssistantView
from homeassistant.helpers.system_info import async_get_system_info

ATTR_INSTALLATION_TYPE = "installation_type"


class DiscoveryInfoView(HomeAssistantView):
    """Get all logged errors and warnings."""

    url = "/api/msentry_gateway/discovery"
    name = "api:msentry_gateway:discovery"

    async def get(self, request):
        """Get discovery information."""
        hass = request.app["hass"]
        system_info = await async_get_system_info(hass)
        return self.json(
            {
                "uuid": await hass.helpers.instance_id.async_get(),
                "location_name": hass.config.location_name,
                "ha_version": homeassistant.const.__version__,
                "installation_type": system_info[ATTR_INSTALLATION_TYPE],
            }
        )

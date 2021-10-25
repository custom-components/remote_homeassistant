from homeassistant.components.http import HomeAssistantView

class DiscoveryInfoView(HomeAssistantView):
    """Get all logged errors and warnings."""

    url = "/api/remote_homeassistant/discovery"
    name = "api:remote_homeassistant:discovery"

    async def get(self, request):
        """Get discovery information."""
        hass = request.app["hass"]
        return self.json(
            {
                "uuid": await hass.helpers.instance_id.async_get(),
                "location_name": hass.config.location_name,
            }
        )

"""Simple implementation to call Home Assistant REST API."""

from homeassistant import exceptions
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_VERIFY_SSL, CONF_ACCESS_TOKEN
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_SECURE

API_URL = "{proto}://{host}:{port}/api/"


class ApiProblem(exceptions.HomeAssistantError):
    """Error to indicate problem reaching API."""


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""


class BadResponse(exceptions.HomeAssistantError):
    """Error to indicate a bad response was received."""


class UnsupportedVersion(exceptions.HomeAssistantError):
    """Error to indicate an unsupported version of Home Assistant."""


async def async_get_discovery_info(hass, host, port, secure, access_token, verify_ssl):
    """Get discovery information from server."""
    url = API_URL.format(
        proto="https" if secure else "http",
        host=host,
        port=port,
    )
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    session = async_get_clientsession(hass, verify_ssl)

    # Try to reach api endpoint solely for verifying auth
    async with session.get(url, headers=headers) as resp:
        if 400 <= resp.status < 500:
            raise InvalidAuth()
        if resp.status != 200:
            raise ApiProblem()

    # Fetch discovery info location for name and unique UUID
    async with session.get(url + "discovery_info") as resp:
        if resp.status != 200:
            raise ApiProblem()
        json = await resp.json()
        if not isinstance(json, dict):
            raise BadResponse(f"Bad response data: {json}")
        if "uuid" not in json:
            raise UnsupportedVersion()
        return json

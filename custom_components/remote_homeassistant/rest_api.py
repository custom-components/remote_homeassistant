"""Simple implementation to call Home Assistant REST API."""

import logging

from homeassistant import exceptions
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

API_URL = "{proto}://{host}:{port}/api/remote_homeassistant/discovery"


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


class EndpointMissing(exceptions.HomeAssistantError):
    """Error to indicate endpoint is missing."""


async def async_get_discovery_info(hass, host, port, secure, access_token, verify_ssl):
    """Get discovery information from server."""
    url = API_URL.format(
        proto="https" if secure else "http",
        host=host,
        port=port,
    )

    access_token = str(access_token).strip()

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }

    session = async_get_clientsession(hass, verify_ssl)

    async with session.get(url, headers=headers) as resp:
        if resp.status == 404:
            raise EndpointMissing()

        if 400 <= resp.status < 500:
            body = await resp.text()
            _LOGGER.error(
                "Remote Home Assistant auth/API error: status=%s, url=%s, body=%s",
                resp.status,
                url,
                body[:500],
            )
            raise InvalidAuth()

        if resp.status != 200:
            body = await resp.text()
            _LOGGER.error(
                "Remote Home Assistant API problem: status=%s, url=%s, body=%s",
                resp.status,
                url,
                body[:500],
            )
            raise ApiProblem()

        data = await resp.json()

        if not isinstance(data, dict):
            raise BadResponse(f"Bad response data: {data}")

        if "uuid" not in data:
            raise UnsupportedVersion()

        return data

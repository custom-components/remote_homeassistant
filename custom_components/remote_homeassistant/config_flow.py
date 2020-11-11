"""Config flow for Remote Home-Assistant integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_VERIFY_SSL,
    CONF_ACCESS_TOKEN,
    CONF_INCLUDE,
    CONF_EXCLUDE,
)

from .rest_api import ApiProblem, CannotConnect, InvalidAuth, async_get_discovery_info
from .const import (
    CONF_SECURE,
    CONF_FILTER,
    CONF_SUBSCRIBE_EVENTS,
    CONF_ENTITY_PREFIX,
    DOMAIN,
)  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PORT, default=8123): int,
        vol.Required(CONF_ACCESS_TOKEN): str,
        vol.Optional(CONF_SECURE, default=True): bool,
        vol.Optional(CONF_VERIFY_SSL, default=True): bool,
    }
)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect."""
    conf = {
        CONF_EXCLUDE: {},
        CONF_INCLUDE: {},
        CONF_FILTER: [],
        CONF_SUBSCRIBE_EVENTS: [],
        CONF_ENTITY_PREFIX: "",
    }
    conf.update(data)

    try:
        info = await async_get_discovery_info(
            hass,
            conf[CONF_HOST],
            conf[CONF_PORT],
            conf[CONF_SECURE],
            conf[CONF_ACCESS_TOKEN],
            conf[CONF_VERIFY_SSL],
        )
    except OSError:
        raise CannotConnect()

    return {"title": info["location_name"], "uuid": info["uuid"], "conf": conf}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Remote Home-Assistant."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except ApiProblem:
                errors["base"] = "api_problem"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info["uuid"])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=info["conf"])

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

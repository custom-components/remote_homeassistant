"""Sensor platform for connection status.."""
import logging
from homeassistant.const import CONF_HOST, CONF_STATE, CONF_PORT, CONF_VERIFY_SSL
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import CONF_SECURE, CONF_ENTITY_PREFIX, DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensor based ok config entry."""
    async_add_entities([ConnectionStatusSensor(config_entry)])


class ConnectionStatusSensor(Entity):
    """Representation of a Tuya sensor."""

    def __init__(self, config_entry):
        """Initialize the Tuya sensor."""
        self._state = None
        self._entry = config_entry

    @property
    def name(self):
        """Return name of sensor."""
        host = self._entry.data[CONF_HOST]
        port = self._entry.data[CONF_PORT]
        return f"Remote connection to {host}:{port}"

    @property
    def state(self):
        """Return sensor state."""
        return self._state

    @property
    def unique_id(self):
        """Return unique device identifier."""
        return self._entry.unique_id

    @property
    def should_poll(self):
        """Return if entity should be polled."""
        return False

    @property
    def device_state_attributes(self):
        """Return device state attributes."""
        return {
            "host": self._entry.data[CONF_HOST],
            "port": self._entry.data[CONF_PORT],
            "secure": self._entry.data.get(CONF_SECURE, False),
            "verify_ssl": self._entry.data.get(CONF_VERIFY_SSL, False),
            "entity_prefix": self._entry.data.get(CONF_ENTITY_PREFIX, ""),
            "uuid": self.unique_id,
        }

    async def async_added_to_hass(self):
        """Subscribe to events."""
        await super().async_added_to_hass()

        def _update_handler(state):
            """Update entity state when status was updated."""
            self._state = state
            self.schedule_update_ha_state()

        signal = f"remote_homeassistant_{self._entry.unique_id}"
        self.async_on_remove(
            async_dispatcher_connect(self.hass, signal, _update_handler)
        )

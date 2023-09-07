"""Sensor platform for connection status.."""
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_VERIFY_SSL
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import CONF_ENTITY_PREFIX, CONF_SECURE, DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensor based ok config entry."""
    async_add_entities([ConnectionStatusSensor(config_entry)])


class ConnectionStatusSensor(Entity):
    """Representation of a remote_homeassistant sensor."""

    def __init__(self, config_entry):
        """Initialize the remote_homeassistant sensor."""
        self._state = None
        self._entry = config_entry

        proto = 'http' if config_entry.data.get(CONF_SECURE) else 'https'
        host = config_entry.data[CONF_HOST]
        port = config_entry.data[CONF_PORT]
        self._attr_name = f"Remote connection to {host}:{port} 2"
        self._attr_unique_id = config_entry.unique_id + "_2"
        self._attr_should_poll = False
        self._attr_device_info = DeviceInfo(
            name="Home Assistant",
            configuration_url=f"{proto}://{host}:{port}",
            identifiers={(DOMAIN, f"remote_{self._attr_unique_id}")},
        )
    
    @property
    def device_class(self):
        return BinarySensorDeviceClass.CONNECTIVITY

    @property
    def state(self):
        """Return sensor state."""
        return "on" if self._state == "connected" else "off"

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "host": self._entry.data[CONF_HOST],
            "port": self._entry.data[CONF_PORT],
            "secure": self._entry.data.get(CONF_SECURE, False),
            "verify_ssl": self._entry.data.get(CONF_VERIFY_SSL, False),
            "entity_prefix": self._entry.options.get(CONF_ENTITY_PREFIX, ""),
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

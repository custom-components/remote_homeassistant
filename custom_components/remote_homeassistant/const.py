"""Constants used by integration."""

CONF_REMOTE_CONNECTION = "remote_connection"
CONF_UNSUB_LISTENER = "unsub_listener"
CONF_OPTIONS = "options"
CONF_REMOTE_INFO = "remote_info"
CONF_LOAD_COMPONENTS = "load_components"
CONF_SERVICE_PREFIX = "service_prefix"
CONF_SERVICES = "services"

CONF_FILTER = "filter"
CONF_SECURE = "secure"
CONF_API_PASSWORD = "api_password"
CONF_SUBSCRIBE_EVENTS = "subscribe_events"
CONF_ENTITY_PREFIX = "entity_prefix"
CONF_ENTITY_FRIENDLY_NAME_PREFIX = "entity_friendly_name_prefix"
CONF_MAX_MSG_SIZE = "max_message_size"

CONF_INCLUDE_DOMAINS = "include_domains"
CONF_INCLUDE_ENTITIES = "include_entities"
CONF_EXCLUDE_DOMAINS = "exclude_domains"
CONF_EXCLUDE_ENTITIES = "exclude_entities"

# FIXME: There seems to be no way to make these strings translateable
CONF_MAIN = "Add a remote node"
CONF_REMOTE = "Setup as remote node"

DOMAIN = "remote_homeassistant"

REMOTE_ID = "remote"

# replaces 'from homeassistant.core import SERVICE_CALL_LIMIT'
SERVICE_CALL_LIMIT = 10

DEFAULT_MAX_MSG_SIZE = 16*1024*1024

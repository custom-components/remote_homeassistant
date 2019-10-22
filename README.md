[![License][license-shield]](LICENSE.md)

[![hacs][hacsbadge]](hacs)
![Project Maintenance][maintenance-shield]


_Component to link multiple Home-Assistant instances together._

**This component will set up the following platforms.**

Platform | Description
-- | --
`remote_homeassistant` | Link multiple Home-Assistant instances together .

The master instance connects to the Websocket APIs of the slaves, the connection options are specified via the `host`, `port`, and `secure` configuration parameters. An API password can also be set via `api_password`. To ignore SSL warnings in secure mode, set the `verify_ssl` parameter to false.

After the connection is completed, the remote states get populated into the master instance.
The entity ids can optionally be prefixed via the `entity_prefix` parameter.

The component keeps track which objects originate from which instance. Whenever a service is called on an object, the call gets forwarded to the particular slave instance.

When the connection to the remote instance is lost, all previously published states are removed again from the local state registry.

A possible use case for this is to be able to use different Z-Wave networks, on different Z-Wave sticks (with the second one possible running on another computer in a different location).


## Installation

If you use HACS:

1. Click install.
2. Add `remote_homeassistant:` to your HA configuration.

Otherwise:

1. To use this plugin, copy the `remote_homeassistant` folder into your [custom_components folder](https://developers.home-assistant.io/docs/en/creating_component_loading.html).
2. Add `remote_homeassistant:` to your HA configuration.

## Configuration 

To integrate `remote_homeassistant` into Home Assistant, add the following section to your `configuration.yaml` file:

Simple example:

```yaml
# Example configuration.yaml entry
remote_homeassistant:
  instances:
  - host: raspberrypi.local
```


Full example:

```yaml
# Example configuration.yaml entry
remote_homeassistant:
  instances:
  - host: localhost
    port: 8124
  - host: localhost
    port: 8125
    secure: true
    verify_ssl: false
    access_token: !secret access_token
    api_password: !secret http_password
    entity_prefix: "slave02_"
    include:
      domains:
      - sensor
      - switch
      - group
      entities:
      - zwave.controller
      - zwave.desk_light
    exclude:
      entities:
      - group.all_switches

    subscribe_events:
    - zwave.network_ready
    - zwave.node_event
```

```
host:
  host: Hostname or IP address of remote instance.
  required: true
  type: string
port:
  description: Port of remote instance.
  required: false
  type: int
secure:
  description: Use TLS (wss://) to connect to the remote instance.
  required: false
  type: bool
verify_ssl:
  description: Enables / disables verification of the SSL certificate of the remote instance.
  required: false
  type: bool
  default: true
access_token:
  description: Access token of the remote instance, if set. Mutually exclusive with api_password
  required: false
  type: string
api_password:
  description: DEPRECTAED! API password of the remote instance, if set. Mutually exclusive with access_token
  required: false
  type: string
entity_prefix:
  description: Prefix for all entities of the remote instance.
  required: false
  type: string
include:
  description: Configures what should be included from the remote instance. Values set by the exclude lists will take precedence.
  required: false
  default: include everything
  type: mapping of
    entities:
      description: The list of entity ids to be included from the remote instance
      type: list
    domains:
      description: The list of domains to be included from the remote instance
      type: list
exclude:
  description: Configures what should be excluded from the remote instance
  required: false
  default: exclude nothing
  type: mapping of
    entities:
      description: The list of entity ids to be excluded from the remote instance
      type: list
    domains:
      description: The list of domains to be excluded from the remote instance
      type: list
subscribe_events:
  description: Further list of events, which should be forwarded from the remote instance. If you override this, you probably will want to add state_changed!!
  required: false
  type: list
  default: 
  - state_changed
  - service_registered
```

## Special notes 

If you have remote domains (e.g. `switch`), that are not loaded on the master instance you need to add a dummy entry on the master, otherwise you'll get a `Call service failed` error.

E.g. on the master:

```
switch:
```

to enable all `switch` services.

---

See also the discussion on https://github.com/home-assistant/home-assistant/pull/13876 and https://github.com/home-assistant/architecture/issues/246 for this component

[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/lukas-hetzenecker/home-assistant-remote.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-lukas--hetzenecker-blue.svg?style=for-the-badge

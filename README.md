Follow the discussion on https://github.com/home-assistant/home-assistant/pull/13876

Compatible with home-assistant >= 0.80

The master instance connects to the Websocket APIs of the slaves, the connection options are specified via the `host`, `port`, and `secure` configuration parameters. An API password can also be set via `api_password`.

After the connection is completed, the remote states get populated into the master instance.
The entity ids can optionally be prefixed via the `entity_prefix` parameter.

The component keeps track which objects originate from which instance. Whenever a service is called on an object, the call gets forwarded to the particular slave instance.

When the connection to the remote instance is lost, all previously published states are removed again from the local state registry.

A possible use case for this is to be able to use different Z-Wave networks, on different Z-Wave sticks (with the second one possible running on another computer in a different location).

## Installation 

To use this plugin, copy the `remote_homeassistant.py` file into your [custom_components folder](https://developers.home-assistant.io/docs/en/creating_component_loading.html).

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
    access_token: !secret access_token
    api_password: !secret http_password
    entity_prefix: "slave02_"
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
subscribe_events:
  description: Further list of events, which should be forwarded from the remote instance. If you override this, you probably will want to add state_changed!!
  required: false
  type: list
  default: 
  - state_changed
  - service_registered
```

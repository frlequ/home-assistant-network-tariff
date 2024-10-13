import logging
from datetime import timedelta
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from .elektro_network_tariff import calculate_tariff

_LOGGER = logging.getLogger(__name__)

# Extend PLATFORM_SCHEMA with optional name and entity_id, and provide defaults
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional("name", default="Elektro Network Tariff"): cv.string,
    vol.Optional("entity_id", default="sensor.elektro_network_tariff"): cv.string,
})

SCAN_INTERVAL = timedelta(seconds=30)  # Adjust the interval as needed

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Elektro Network Tariff Sensor."""
    # Retrieve name and entity_id from configuration, with defaults
    name = config.get("name")
    entity_id = config.get("entity_id")
    async_add_entities([ElektroNetworkTariffSensor(name, entity_id)])

class ElektroNetworkTariffSensor(Entity):
    """Representation of an Elektro Network Tariff Sensor."""

    def __init__(self, name, entity_id):
        """Initialize the sensor."""
        self._name = name
        self._entity_id = entity_id
        self._state = None
        self._blocks = None
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def entity_id(self):
        """Return the entity_id."""
        return self._entity_id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def state_attributes(self):
        """Return the state attributes."""
        blocks_str = ','.join(map(str, self._blocks)) if self._blocks else ''
        return {
            "state_class": "measurement",
            "blocks": blocks_str
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:transmission-tower"

    def update(self):
        """Fetch new state data for the sensor."""
        self._state, self._blocks = calculate_tariff()  # Update both state and blocks

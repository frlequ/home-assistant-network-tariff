import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from .elektro_network_tariff import calculate_tariff

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({})

SCAN_INTERVAL = timedelta(seconds=30)  # Adjust the interval as needed

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Elektro Network Tariff Sensor."""
    async_add_entities([ElektroNetworkTariffSensor()])

class ElektroNetworkTariffSensor(Entity):
    """Representation of an Elektro Network Tariff Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Elektro Network Tariff'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def state_attributes(self):
        """Return the state attributes."""
        return {
            "state_class": "measurement"
        }
        
    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:transmission-tower"

    def update(self):
        """Fetch new state data for the sensor."""
        self._state = calculate_tariff()
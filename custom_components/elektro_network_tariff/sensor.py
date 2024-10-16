import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import timedelta
from .elektro_network_tariff import calculate_tariff
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Elektro Network Tariff Sensor from a config entry."""
    name = config_entry.data["name"]
    entity_id = config_entry.data["entity_id"]
    async_add_entities([ElektroNetworkTariffSensor(name, entity_id)])

class ElektroNetworkTariffSensor(SensorEntity):
    """Representation of an Elektro Network Tariff Sensor."""

    def __init__(self, name, entity_id):
        """Initialize the sensor."""
        self._attr_name = name
        self._attr_unique_id = entity_id  # Set a unique ID for the entity
        self._state = None
        self._blocks = None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "state_class": "measurement",
            "blocks": ','.join(map(str, self._blocks)) if self._blocks else ''
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:transmission-tower"

    async def async_update(self):
        """Fetch new state data for the sensor asynchronously."""
        try:
            self._state, self._blocks = calculate_tariff()  # Fetch data asynchronously if needed
        except Exception as e:
            _LOGGER.error(f"Error updating Elektro Network Tariff Sensor: {e}")

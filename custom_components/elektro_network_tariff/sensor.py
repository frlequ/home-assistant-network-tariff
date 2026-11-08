import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util
from .elektro_network_tariff import calculate_tariff
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Elektro Network Tariff Sensor from a config entry."""
    name = config_entry.data["name"]
    entity_id = config_entry.data["entity_id"]
    async_add_entities([ElektroNetworkTariffSensor(name, entity_id)])

class ElektroNetworkTariffSensor(SensorEntity):
    """Representation of an Elektro Network Tariff Sensor."""

    # Updated on every full hour instead of being polled
    _attr_should_poll = False

    def __init__(self, name, entity_id):
        """Initialize the sensor."""
        self._attr_name = name
        self._attr_unique_id = entity_id  # Set a unique ID for the entity
        self._state = None
        self._blocks = None
        self._is_holiday = None
        self._is_high_season = None
        self._next_tariff_block = None
        self._is_next_block_higher = None

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "state_class": "measurement",
            "blocks": ','.join(map(str, self._blocks)) if self._blocks else '',
            "holiday": self._is_holiday,
            "high_season": self._is_high_season,
            "next_tariff_block": self._next_tariff_block,
            "next_block_higher": self._is_next_block_higher
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:transmission-tower"

    async def async_added_to_hass(self):
        """Calculate the state now and refresh it on every full hour.

        The schedule follows the clock rather than the start time, so starting
        at 3:45 gives the correct block immediately and the next update at 4:00.
        """
        self.async_on_remove(
            async_track_time_change(self.hass, self._handle_full_hour, minute=0, second=0)
        )
        self._refresh(dt_util.now())

    @callback
    def _handle_full_hour(self, now):
        """Refresh the sensor when a new hour starts."""
        self._refresh(now)
        self.async_write_ha_state()

    async def async_update(self):
        """Refresh the sensor when an update is requested manually."""
        self._refresh(dt_util.now())

    def _refresh(self, now):
        """Calculate the tariff data for the given local time."""
        try:
            # Fetch all attributes from the calculate_tariff function
            tariff_data = calculate_tariff(now)
            self._state = tariff_data["current_tariff"]
            self._blocks = tariff_data["blocks"]
            self._is_holiday = tariff_data["is_holiday"]
            self._is_high_season = tariff_data["is_high_season"]
            self._next_tariff_block = tariff_data["next_tariff_block"]
            self._is_next_block_higher = tariff_data["is_next_block_higher"]
        except Exception as e:
            _LOGGER.error(f"Error updating Elektro Network Tariff Sensor: {e}")

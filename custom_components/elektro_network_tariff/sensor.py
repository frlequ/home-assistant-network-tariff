import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt
from .network_fee_api import calculate_tariff

_LOGGER = logging.getLogger(__name__)

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

    def update(self):
        """Fetch new state data for the sensor."""
        current_datetime = dt.now()
        self._state = calculate_tariff(current_datetime)

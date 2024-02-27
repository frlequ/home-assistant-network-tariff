from datetime import timedelta

def __init__(self):
    """Initialize the sensor."""
    self._state = None
    self.async_update = self.async_schedule_update_ha_state

    async_track_time_interval(hass, self.async_update, timedelta(hours=1))
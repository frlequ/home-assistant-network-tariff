import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN  # Make sure DOMAIN is defined in const.py

class ElektroNetworkTariffConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Elektro Network Tariff."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # Automatically create an entry with default values
        return self.async_create_entry(
            title="Elektro Network Tariff", 
            data={
                "name": "Elektro Network Tariff",
                "entity_id": "sensor.elektro_network_tariff"
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ElektroNetworkTariffOptionsFlowHandler(config_entry)

class ElektroNetworkTariffOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Elektro Network Tariff options."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("name", default=self.config_entry.data.get("name")): str,
                vol.Required("entity_id", default=self.config_entry.data.get("entity_id")): str,
            })
        )

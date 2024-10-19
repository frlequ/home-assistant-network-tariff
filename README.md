# Home Assistant Custom Component: Slovenian Energy Tariff Calculator (Omrežnina)

This custom component for Home Assistant calculates the current network fee tariff based on the energy distributor's rates in Slovenia. It considers various factors such as the date, whether it's a weekend, a public holiday, or a specific season of the year to calculate the tariff.

## Features

- Calculates current energy tariff based on date and time.
- Automatically identifies weekends and Slovenian public holidays.
- Adjusts tariffs for high and low seasons.

## Installation

**Method 1 _(easiest)_:**

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=frlequ&repository=home-assistant-network-tariff&category=integration)


**Method 2:**
1. **Download the Custom Component**
   - Download the files from the repository.
   
2. **Copy to Your Custom Components Directory**
   - Copy the downloaded folder `elektro_network_tariff` into the `custom_components/elektro_network_tariff` directory in your Home Assistant configuration directory.

3. **Restart Home Assistant**
   - Restart your Home Assistant instance to load the new component.

## Configuration

After installation, go to Settings -> Add Integration and search for `Elektro Network Tariff`

## Upgrading

> [!IMPORTANT]
> If you are upgrading from an older version, please **remove** platform sensor from `configuration.yaml`, you don't need it anymore.
>
>```yaml
>sensor:
>  - platform: elektro_network_tariff
>```

## Custom Card

> [!TIP]
> You can use Network Tariff Card **[Network Tariff Card](https://github.com/frlequ/network-tariff-card)**. The card is designed to work with this component.
> ![Network Tariff Card](https://github.com/frlequ/network-tariff-card/blob/main/assets/network-tariff-card.jpg)






## Report any issues

Thanks and consider giving me a 🌟 star

<a href="https://www.buymeacoffee.com/frlequ" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

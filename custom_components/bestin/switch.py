"""Switch platform for BESTIN"""

from __future__ import annotations

from homeassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SwitchEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_VERSION, NEW_SWITCH
from .device import BestinDevice, setup_platform_entry
from .hub import BestinHub

DEVICE_ICON = {
    "outlet": "mdi:power-socket",
    "outlet:standbycut": "mdi:power-sleep",
    "doorlock": "mdi:door-closed",
    "elevator": "mdi:elevator-down",
    "electric": "mdi:power-socket",
    "electric:standbycut": "mdi:power-sleep",
    "gas": "mdi:valve",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Setup switch platform."""
    setup_platform_entry(
        hass, entry, async_add_entities, SWITCH_DOMAIN, NEW_SWITCH, BestinSwitch
    )


class BestinSwitch(BestinDevice, SwitchEntity):
    """Defined the Switch."""
    TYPE = SWITCH_DOMAIN
    
    def __init__(self, device, hub: BestinHub):
        """Initialize the switch."""
        super().__init__(device, hub)
        self._attr_icon = DEVICE_ICON.get(self._device_info.device_type)
        self._version_exists = getattr(hub.api, CONF_VERSION, False)

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._device_info.state
    
    async def async_turn_on(self, **kwargs):
        """Turn on light."""
        if self._version_exists:
            if self._device_info.device_type == "gas":
                await self.enqueue_command("open")
            elif self._device_info.device_type == "electric:standbycut":
                await self.enqueue_command(switch="set")
            else:
                await self.enqueue_command(switch=STATE_ON)
        else:
            await self.enqueue_command(True)

    async def async_turn_off(self, **kwargs):
        """Turn off light."""
        if self._version_exists:
            if self._device_info.device_type == "gas":
                await self.enqueue_command("close")
            elif self._device_info.device_type == "electric:standbycut":
                await self.enqueue_command(switch="unset")
            else:
                await self.enqueue_command(switch=STATE_OFF)
        else:
            await self.enqueue_command(False)

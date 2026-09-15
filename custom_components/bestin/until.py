from typing import Any, Callable

from .const import BRAND_PREFIX, DEVICE_PLATFORM_MAP, DeviceInfo, DeviceProfile


def formatted_name(name: str) -> str:
    """Format the given name by capitalizing and removing any text after a colon."""
    if ':' in name:
        return name.split(":")[0].title()
    return name.title()


def resolve_device_platform(device_type: str, sub_id: str | None) -> tuple[str, str]:
    """Resolve the (possibly sub_id-suffixed) device_type and its DEVICE_PLATFORM_MAP domain."""
    if device_type != "energy" and sub_id and not sub_id.isdigit():
        device_type = f"{device_type}:{''.join(filter(str.isalpha, sub_id))}"
    return device_type, DEVICE_PLATFORM_MAP[device_type]


def build_device(
    device_id: str,
    sub_id: str | None,
    state: Any,
    unique_id_suffix: str,
    devices: dict[str, DeviceProfile],
    enqueue_command: Callable,
) -> DeviceProfile:
    """Build (or return the existing) DeviceProfile for device_id/sub_id."""
    device_type, device_room = device_id.split("_")

    did_suffix = f"_{sub_id}" if sub_id else ""
    full_device_id = f"{BRAND_PREFIX}_{device_id}{did_suffix}"
    if sub_id:
        sub_id_parts = sub_id.split("_")
        device_name = f"{device_type} {device_room} {' '.join(sub_id_parts)}".title()
    else:
        device_name = f"{device_type} {device_room}".title()

    device_type, domain = resolve_device_platform(device_type, sub_id)
    unique_id = f"{full_device_id}-{unique_id_suffix}"

    if full_device_id not in devices:
        device_info = DeviceInfo(
            device_type=device_type,
            name=device_name,
            room=device_room,
            state=state,
            device_id=full_device_id,
        )
        devices[full_device_id] = DeviceProfile(
            enqueue_command=enqueue_command,
            domain=domain,
            unique_id=unique_id,
            info=device_info,
        )
    return devices[full_device_id]

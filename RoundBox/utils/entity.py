#  -*- coding: utf-8 -*-

from RoundBox.utils.enum import StrEnum
from typing import TypedDict

from dataclasses import dataclass


class DeviceEntryType(StrEnum):
    """Device entry type.

    """

    SERVICE = "service"


class DeviceInfo(TypedDict, total=False):
    """Entity device information for device registry.

    """

    configuration_url: str | None
    connections: set[tuple[str, str]]
    default_manufacturer: str
    default_model: str
    default_name: str
    entry_type: DeviceEntryType | None
    identifiers: set[tuple[str, str]]
    manufacturer: str | None
    model: str | None
    name: str | None
    suggested_area: str | None
    sw_version: str | None
    hw_version: str | None
    via_device: tuple[str, str]


class EntityCategory(StrEnum):
    """Category of an entity.
    An entity with a category will:
    - Not be exposed to cloud, Alexa, or Google Assistant components
    - Not be included in indirect service calls to devices or areas
    """

    # Config: An entity which allows changing the configuration of a device
    CONFIG = "config"

    # Diagnostic: An entity exposing some configuration parameter or diagnostics of a device
    DIAGNOSTIC = "diagnostic"

    # System: An entity which is not useful for the user to interact with
    SYSTEM = "system"


@dataclass
class EntityDescription:
    """A class that describes Home Assistant entities."""

    # This is the key identifier for this entity
    key: str

    device_class: str | None = None
    entity_category: EntityCategory | None = None
    entity_registry_enabled_default: bool = True
    force_update: bool = False
    icon: str | None = None
    name: str | None = None
    unit_of_measurement: str | None = None

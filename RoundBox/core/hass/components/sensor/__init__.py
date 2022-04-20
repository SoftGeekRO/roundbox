#  -*- coding: utf-8 -*-

import logging
from dataclasses import dataclass
from datetime import date, datetime
from typing import Final, TypedDict

from RoundBox.core.hass.helpers.typing import StateType
from RoundBox.utils.backports.strenum.enum import StrEnum

logger: Final = logging.getLogger(__name__)


class ExtraOptions(TypedDict):
    """Extra options or information for creating o more customizable interface"""

    pass


class DeviceInfo(TypedDict):
    """Entity device information for device registry."""

    default_manufacturer: str
    default_model: str
    default_name: str

    name: str | None
    alias: str | None
    model: str | None
    serial_number: str | None
    manufacturer: str | None
    sw_version: str | None
    hw_version: str | None


class SensorDeviceClass(StrEnum):
    """Device class for sensors."""

    # apparent power (VA)
    APPARENT_POWER = "apparent_power"

    # Air Quality Index
    AQI = "aqi"

    # % of battery that is left
    BATTERY = "battery"

    # ppm (parts per million) Carbon Monoxide gas concentration
    CO = "carbon_monoxide"

    # ppm (parts per million) Carbon Dioxide gas concentration
    CO2 = "carbon_dioxide"

    # current (A)
    CURRENT = "current"

    # date (ISO8601)
    DATE = "date"

    # energy (Wh, kWh, MWh)
    ENERGY = "energy"

    # frequency (Hz, kHz, MHz, GHz)
    FREQUENCY = "frequency"

    # gas (m³ or ft³)
    GAS = "gas"

    # % of humidity in the air
    HUMIDITY = "humidity"

    # current light level (lx/lm)
    ILLUMINANCE = "illuminance"

    # Amount of money (currency)
    MONETARY = "monetary"

    # Amount of NO2 (µg/m³)
    NITROGEN_DIOXIDE = "nitrogen_dioxide"

    # Amount of NO (µg/m³)
    NITROGEN_MONOXIDE = "nitrogen_monoxide"

    # Amount of N2O  (µg/m³)
    NITROUS_OXIDE = "nitrous_oxide"

    # Amount of O3 (µg/m³)
    OZONE = "ozone"

    # Particulate matter <= 0.1 μm (µg/m³)
    PM1 = "pm1"

    # Particulate matter <= 10 μm (µg/m³)
    PM10 = "pm10"

    # Particulate matter <= 2.5 μm (µg/m³)
    PM25 = "pm25"

    # power factor (%)
    POWER_FACTOR = "power_factor"

    # power (W/kW)
    POWER = "power"

    # pressure (hPa/mbar)
    PRESSURE = "pressure"

    # reactive power (var)
    REACTIVE_POWER = "reactive_power"

    # signal strength (dB/dBm)
    SIGNAL_STRENGTH = "signal_strength"

    # Amount of SO2 (µg/m³)
    SULPHUR_DIOXIDE = "sulphur_dioxide"

    # temperature (C/F)
    TEMPERATURE = "temperature"

    # timestamp (ISO8601)
    TIMESTAMP = "timestamp"

    # Amount of VOC (µg/m³)
    VOLATILE_ORGANIC_COMPOUNDS = "volatile_organic_compounds"

    # voltage (V)
    VOLTAGE = "voltage"


class SensorStateClass(StrEnum):
    """State class for sensors."""

    # The state represents a measurement in present time
    MEASUREMENT = "measurement"

    # The state represents a total amount, e.g. net energy consumption
    TOTAL = "total"

    # The state represents a monotonically increasing total, e.g. an amount of consumed gas
    TOTAL_INCREASING = "total_increasing"


@dataclass
class SensorEntityDescription:
    """A class that describes sensor entities."""

    key: str

    device_class: SensorDeviceClass | str | None = None
    name: str | None = None
    native_unit_of_measurement: str | None = None
    state_class: SensorStateClass | str | None = None
    unit_of_measurement: str | None = None


class SensorEntity:
    """Base class for sensor entities."""

    entity_description: SensorEntityDescription

    # Entity Properties
    _attr_extra_options: ExtraOptions | str | None = None
    _attr_device_info: DeviceInfo | None = None
    _attr_name: str | None
    _attr_unique_id: str | None = None
    _attr_unit_of_measurement: str | None

    _attr_device_class: SensorDeviceClass | str | None
    _attr_native_unit_of_measurement: str | None
    _attr_native_value: StateType | date | datetime = None
    _attr_state_class: SensorStateClass | str | None
    _temperature_conversion_reported = False
    _sensor_option_unit_of_measurement: str | None = None

    @property
    def native_value(self) -> StateType | date | datetime:
        """Return the value reported by the sensor."""
        return self._attr_native_value

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of the sensor, if any."""
        if hasattr(self, "_attr_native_unit_of_measurement"):
            return self._attr_native_unit_of_measurement
        if hasattr(self, "entity_description"):
            return self.entity_description.native_unit_of_measurement
        return None

    @property
    def unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of this entity, if any.

        :return:
        """
        if hasattr(self, "_attr_unit_of_measurement"):
            return self._attr_unit_of_measurement
        if hasattr(self, "entity_description"):
            return self.entity_description.unit_of_measurement
        return None

    def __repr__(self) -> str:
        """Return the representation."""
        return f"<Entity {self.name}>"

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return self._attr_unique_id

    @property
    def name(self) -> str | None:
        """Return the name of the entity.

        :return:
        """
        if hasattr(self, "_attr_name"):
            return self._attr_name
        if hasattr(self, "entity_description"):
            return self.entity_description.name
        return None

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device specific attributes.
        Implemented by platform classes.

        :return:
        """
        return self._attr_device_info

    @property
    def device_class(self) -> str | None:
        """Return the class of this device, from component DEVICE_CLASSES.

        :return:
        """
        if hasattr(self, "_attr_device_class"):
            return self._attr_device_class
        if hasattr(self, "entity_description"):
            return self.entity_description.device_class
        return None

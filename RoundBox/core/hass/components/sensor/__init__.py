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

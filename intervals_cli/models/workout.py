from dataclasses import dataclass
from typing import Union, Tuple
from datetime import timedelta
from enum import Enum


class Sport(Enum):
    RUN = "Run"
    RIDE = "Ride"
    SWIM = "Swim"


class Zone(Enum):
    Z1 = "Z1"
    Z2 = "Z2"
    Z3 = "Z3"
    Z4 = "Z4"
    Z5 = "Z5"


class Units(Enum):
    METRIC = "Metric"
    IMPERIAL = "Imperial"


@dataclass
class Pace:
    min: int
    sec: int
    unit: Units


# Targets


@dataclass
class Target:
    pass


@dataclass
class Percent(Target):
    pass


@dataclass
class Absolute(Target):
    pass


@dataclass
class Zones(Target):
    pass


@dataclass
class Ftp(Percent):
    percent: Union[int, Tuple[int, int]]


@dataclass
class MaxHeartRate(Percent):
    percent: Union[int, Tuple[int, int]]


@dataclass
class ThresholdHeartRate(Percent):
    percent: Union[int, Tuple[int, int]]


@dataclass
class ThresholdPace(Percent):
    percent: Union[int, Tuple[int, int]]


@dataclass
class Watts(Absolute):
    watts: Union[int, Tuple[int, int]]


@dataclass
class AbsolutePace(Absolute):
    pace: Union[Pace, Tuple[Pace, Pace]]


@dataclass
class Power(Zones):
    zone: Zone


@dataclass
class PaceZone(Zones):
    zone: Zone


@dataclass
class HeartRate(Zones):
    zone: Zone


@dataclass
class Ramps:
    percent_range: Tuple[int, int]


@dataclass
class FreeRide:
    pass


# Structure


@dataclass
class WorkoutStep:
    repetitions: int
    duration: timedelta
    target: Target


@dataclass
class WorkoutSection:
    name: str
    repetitions: int
    steps: list[WorkoutStep]


@dataclass
class Workout:
    name: str
    sport: Sport
    steps: list[WorkoutSection]
    total_duration: timedelta

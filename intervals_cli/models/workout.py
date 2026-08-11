from dataclasses import dataclass
from typing import Union, Tuple
from datetime import timedelta
from enum import Enum


class Sport(Enum):
    RUN = "run"
    BIKE = "bike"
    SWIM = "swim"


class Zone(Enum):
    Z1 = "Z1"
    Z2 = "Z2"
    Z3 = "Z3"
    Z4 = "Z4"
    Z5 = "Z5"


class PaceUnit(Enum):
    KM = "/km"
    MI = "/mi"
    PACE_PER_100M = "/100m"
    PACE_PER_100Y = "/100y"
    PACE_PER_400M = "/400m"


class DistanceUnit(Enum):
    YD = "yd"
    METER = "meter"
    KM = "km"
    MI = "mi"


class RampType(Enum):
    PACE = "pace"
    WATTS = "watts"


@dataclass
class Pace:
    min: int
    sec: int
    unit: PaceUnit


@dataclass
class DistanceDuration:
    distance: float
    unit: DistanceUnit


@dataclass
class TimeDuration:
    duration: timedelta


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
class Ramp(Target):
    percent_range: Tuple[int, int]
    ramp_type: RampType


@dataclass
class FreeRide(Target):
    pass


# Structure


@dataclass
class WorkoutStep:
    repetitions: int
    step_duration: TimeDuration | DistanceDuration
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
    sections: list[WorkoutSection]


SPORT_TARGETS = {
    Sport.RUN: (
        ThresholdPace,
        AbsolutePace,
        PaceZone,
        HeartRate,
        MaxHeartRate,
        ThresholdHeartRate,
        Watts,
    ),
    Sport.BIKE: (
        Ftp,
        Watts,
        Power,
        HeartRate,
        MaxHeartRate,
        ThresholdHeartRate,
    ),
    Sport.SWIM: (
        ThresholdPace,
        AbsolutePace,
        PaceZone,
    ),
}

SPORT_PACE_UNIT = {
    Sport.RUN: (PaceUnit.KM, PaceUnit.MI, PaceUnit.PACE_PER_400M),
    Sport.SWIM: (PaceUnit.PACE_PER_100M, PaceUnit.PACE_PER_100Y),
}

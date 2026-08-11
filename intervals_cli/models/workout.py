from dataclasses import dataclass
from typing import Tuple
from datetime import timedelta
from enum import Enum

NumericRange = int | tuple[int, int]


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


@dataclass(order=True)
class Pace:
    min: int
    sec: int
    unit: PaceUnit

    def __post_init__(self):
        if self.min < 0:
            raise ValueError("minutes must be a positive integer")
        if not 0 <= self.sec < 60:
            raise ValueError("seconds must be between 0 and 59")


PaceRange = Pace | tuple[Pace, Pace]


@dataclass
class DistanceDuration:
    distance: float
    unit: DistanceUnit

    def __post_init__(self):
        if self.distance < 0:
            raise ValueError("distance must be a positive integer")


@dataclass
class TimeDuration:
    duration: timedelta


# Targets


@dataclass
class Target:
    pass


@dataclass
class Percent(Target):
    percent: NumericRange

    def __post_init__(self):
        if isinstance(self.percent, tuple):
            if self.percent[0] < 0 or self.percent[1] < 0:
                raise ValueError("percent must be positive integer")
        if isinstance(self.percent, int):
            if self.percent < 0:
                raise ValueError("percent must be positive integer")


@dataclass
class Absolute(Target):
    pass


@dataclass
class Zones(Target):
    zone: Zone


@dataclass
class Ftp(Percent):
    pass


@dataclass
class MaxHeartRate(Percent):
    pass


@dataclass
class ThresholdHeartRate(Percent):
    pass


@dataclass
class ThresholdPace(Percent):
    pass


@dataclass
class Watts(Absolute):
    watts: NumericRange

    def __post_init__(self):
        if isinstance(self.watts, tuple):
            if self.watts[0] < 0 or self.watts[1] < 0:
                raise ValueError("watts must be positive integer")
        if isinstance(self.watts, int):
            if self.watts < 0:
                raise ValueError("watts must be positive integer")


@dataclass
class AbsolutePace(Absolute):
    pace: PaceRange

    def __post_init__(self):
        if isinstance(self.pace, tuple):
            if self.pace[0].unit != self.pace[1].unit:
                raise ValueError("both pace units in range must be of the same type")
            if self.pace[0] > self.pace[1]:
                raise ValueError("first pace in range must be lower than second pace")
            if self.pace[1] < self.pace[0]:
                raise ValueError("second pace in range must be greater than first pace")


@dataclass
class PowerZone(Zones):
    pass


@dataclass
class PaceZone(Zones):
    pass


@dataclass
class HeartRateZone(Zones):
    pass


@dataclass
class Ramp(Target):
    percent_range: Tuple[int, int]
    ramp_type: RampType

    def __post_init__(self):
        if self.percent_range[0] < 0 or self.percent_range[1] < 0:
            raise ValueError("ramps must be positive integers")
        if self.percent_range[0] >= self.percent_range[1]:
            raise ValueError(
                "first ramp integer must be smaller than second ramp integer"
            )
        if self.percent_range[1] <= self.percent_range[0]:
            raise ValueError(
                "second ramp integer must be larger than second ramp integer"
            )


@dataclass
class FreeRide(Target):
    pass


# Structure


@dataclass
class WorkoutStep:
    step_repetition: int
    step_duration: TimeDuration | DistanceDuration
    target: Target

    def __post_init__(self):
        if self.step_repetition <= 0:
            raise ValueError("Step repetition must be at least 1")


@dataclass
class WorkoutSection:
    name: str
    section_repetition: int
    steps: list[WorkoutStep]

    def __post_init__(self):
        if self.section_repetition <= 0:
            raise ValueError("Section repetition must be at least 1")


@dataclass
class Workout:
    name: str
    sport: Sport
    sections: list[WorkoutSection]

    def validate(self):
        valid_targets = SPORT_TARGETS[self.sport]

        for section in self.sections:
            for step in section.steps:
                if not isinstance(step.target, valid_targets):
                    raise ValueError(
                        f"{type(step.target).__name__} is not valid for {self.sport.value}"
                    )


SPORT_TARGETS = {
    Sport.RUN: (
        ThresholdPace,
        AbsolutePace,
        PaceZone,
        HeartRateZone,
        MaxHeartRate,
        ThresholdHeartRate,
        Watts,
    ),
    Sport.BIKE: (
        Ftp,
        Watts,
        PowerZone,
        HeartRateZone,
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

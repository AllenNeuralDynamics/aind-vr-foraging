# Import core types
from __future__ import annotations

# Import core types
from typing import Annotated, Literal, Optional, Union

import aind_behavior_services.calibration.olfactometer as oc
import aind_behavior_services.calibration.water_valve as wvc
import aind_behavior_services.rig as rig
from aind_behavior_services.rig import AindBehaviorRigModel
from pydantic import BaseModel, Field, RootModel

__version__ = "0.3.0"

TreadmillSettings = rig.Treadmill


class TreadmillBoard(RootModel):
    root: Annotated[Union[rig.HarpTreadmill, rig.HarpBehavior], Field(discriminator="who_am_i")]


class Treadmill(BaseModel):
    harp_board: TreadmillBoard = Field(..., description="The board to be used as a treadmill input")
    settings: rig.Treadmill = Field(default=rig.Treadmill(), description="Treadmill settings")


class RigCalibration(BaseModel):
    water_valve: wvc.WaterValveCalibration = Field(default=..., description="Water valve calibration")
    olfactometer: Optional[oc.OlfactometerCalibration] = Field(default=None, description="Olfactometer calibration")


class AindVrForagingRig(AindBehaviorRigModel):
    version: Literal[__version__] = __version__
    triggered_camera_controller: rig.CameraController[rig.SpinnakerCamera] = Field(
        ..., description="Required camera controller to triggered cameras."
    )
    monitoring_camera_controller: Optional[rig.CameraController[rig.WebCamera]] = Field(
        default=None, description="Optional camera controller for monitoring cameras."
    )
    harp_behavior: rig.HarpBehavior = Field(..., description="Harp behavior")
    harp_olfactometer: rig.HarpOlfactometer = Field(..., description="Harp olfactometer")
    harp_lickometer: rig.HarpLickometer = Field(..., description="Harp lickometer")
    harp_clock_generator: rig.HarpClockGenerator = Field(..., description="Harp clock generator")
    harp_analog_input: Optional[rig.HarpAnalogInput] = Field(default=None, description="Harp analog input")
    treadmill: Treadmill = Field(..., description="Treadmill settings")
    harp_sniff_detector: Optional[rig.HarpSniffDetector] = Field(None, description="Sniff detector settings")
    screen: rig.Screen = Field(default=rig.Screen(), description="Screen settings")
    calibration: RigCalibration = Field(..., description="Calibration models")


def schema() -> BaseModel:
    return AindVrForagingRig

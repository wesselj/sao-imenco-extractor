from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class SensorData:
    Temperature: str = None
    Depth: str = None
    OxygenLevelPercent: Union[str, float] = None
    OxygenLevel: Union[str, float] = None
    internalHeading: Optional[int] = None
    topCameraHeading: Optional[int] = None
    bottomCameraHeading: Optional[int] = None

@dataclass
class ImencoCameraData:
    id: str
    CameraSensors: List[SensorData]
    connected : bool
    OxygenSensorModel: Optional[str] = None

@dataclass
class RawDatapoint:
    ext_id: Optional[str]
    timestamp: Optional[float]
    value: Optional[float]
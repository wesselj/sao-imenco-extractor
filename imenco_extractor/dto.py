from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class SensorData:
    Temperature: str
    Depth: str
    OxygenLevel: float
    OxygenLevelPercent: float
    internalHeading: int
    topCameraHeading: int
    bottomCameraHeading: int

@dataclass
class ImencoCameraData:
    id: str
    OxygenSensorModel: str
    CameraSensors: List[SensorData]
    connected : bool

@dataclass
class ImencoCameraDataResponse:
    StatusCode: int
    StatusDescription: str
    Content: ImencoCameraData
    RawContent: str
    Forms: Dict
    Headers: Dict[List[str]]
    Images: Dict
    InputFields: Dict
    Links: Dict
    ParsedHtml: str
    RawContentLength: int

@dataclass
class RawDatapoint:
    ext_id: Optional[str]
    timestamp: Optional[float]
    value: Optional[float]


# From SalMar IT
paths = [
    'http://192.168.130.12:3000/sensordata',
    'http://192.168.130.22:3000/sensordata',
    'http://192.168.130.32:3000/sensordata',
    'http://192.168.130.42:3000/sensordata',
    'http://192.168.130.52:3000/sensordata',
    'http://192.168.130.62:3000/sensordata',
    'http://192.168.130.72:3000/sensordata',
    # 'http://192.168.130.82:3000/sensordata',
    'http://192.168.130.92:3000/sensordata',
    'http://192.168.130.102:3000/sensordata',
    'http://192.168.130.112:3000/sensordata',
    'http://192.168.130.122:3000/sensordata'
]

camera_id_to_path_map = {
    'd8a24ca1-da3c-453e-9548-c9f274530ce7': 'http://192.168.130.12:3000/sensordata',
    '66810365-7e53-4155-8cc8-4b23a8ff3eb9': 'http://192.168.130.22:3000/sensordata',
    'e7c932c0-fefe-47dc-aa98-368c083d1815': 'http://192.168.130.32:3000/sensordata',
    '589f4fc2-19b9-4082-a7b8-18a354346302': 'http://192.168.130.42:3000/sensordata',
    '166ee6cf-e2ea-477e-bb92-466098ba4138': 'http://192.168.130.52:3000/sensordata',
    '179b643f-22ac-4487-9da7-e138a81033be': 'http://192.168.130.62:3000/sensordata',
    'f05173af-7849-4d64-9ddb-9604c88f855c': 'http://192.168.130.72:3000/sensordata',
    # '': 'http://192.168.130.82:3000/sensordata',
    'bb3c11e6-726a-45e2-910a-db55c772f898': 'http://192.168.130.92:3000/sensordata',
    '5a652e71-f7f5-4967-a7a9-30c2d9a43338': 'http://192.168.130.102:3000/sensordata',
    'dbe956c4-dd71-4460-93c1-d01cabf545bb': 'http://192.168.130.112:3000/sensordata',
    'ea43a967-9fc6-4010-82a5-fc95b413a606': 'http://192.168.130.122:3000/sensordata'
}

imenco_path_to_camera_name_map = {
    'http://192.168.130.12:3000/sensordata': 'Pixelite_CCU_C1-C1',
    'http://192.168.130.22:3000/sensordata': 'Pixelite_CCU_C1-C2',
    'http://192.168.130.32:3000/sensordata': 'Pixelite_CCU_C1-C3',
    'http://192.168.130.42:3000/sensordata': 'Pixelite_CCU_C4-C1',
    'http://192.168.130.52:3000/sensordata': 'Pixelite_CCU_C4-C2',
    'http://192.168.130.62:3000/sensordata': 'Pixelite_CCU_C4-C3',
    'http://192.168.130.72:3000/sensordata': 'Pixelite_CCU_C7-C1',
    # 'http://192.168.130.82:3000/sensordata': 'Pixelite_CCU_C7-C2',
    'http://192.168.130.92:3000/sensordata': 'Pixelite_CCU_C7-C3',
    'http://192.168.130.102:3000/sensordata': 'Pixelite_CCU_C10-C1',
    'http://192.168.130.112:3000/sensordata': 'Pixelite_CCU_C10-C2',
    'http://192.168.130.122:3000/sensordata': 'Pixelite_CCU_C10-C3'
}
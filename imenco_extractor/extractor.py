
from datetime import datetime
from dataclasses import fields

from cognite.extractorutils.uploader_types import InsertDatapoints
from cognite.extractorutils.rest.extractor import RestExtractor
from typing import Generator, List, Optional


from imenco_extractor import __version__
from imenco_extractor.dto import ImencoCameraData, paths, camera_id_to_path_map, imenco_path_to_camera_name_map

""" 
### How to update upload data from 12 cameras with 7 sensors into 12*7=84 time series in parallel? ###

1. We first need the 12*7=84 timeseries IDs. These should be somehow we connected to the ImencoAPI ids (either through map or identical)
    1.1 Each time series should be matched to a "camera ID + sensor" combination
2. For each camera, we make an API call to get the camera data.
    2.1 The call should either be to a specific camera ID, 
    2.2 OR - the ID that we retrieve (toghether with sensors) should be able to be traced to a specific timeseries ID.
3. With the known camera data ID and a matching timeseries ID, we create a 7 datapoints to be uploaded to the 7 corresponding timeseries.
4. Yield the list (which then gets uploaded to CDF)

# Our approach
1. We maintain a map of 'Imenco camera IDs + sensors' to timeseries IDs.
2. We make a call to all cameras in parallel, retrieving 12 responses each with a camera ID.
3. For each response, we map each camera ID to a timeseries external ID. Then we extract the sensor data from the responses, build 7 datapoints and yield them
"""

extractor = RestExtractor(
    name="imenco_extractor",
    description="Imenco sensor data to CDF datapoints",
    version=__version__
)

@extractor.get_multiple(paths=paths, response_type=ImencoCameraData, interval=1)
def imenco_response_to_datapoints_handler(imenco_camera_data: ImencoCameraData) -> Generator[InsertDatapoints, None, None]:
    """
    Receive responses of type 'ImencoCameraData' from GET request to decorated function 'paths'. 
    Transform response to yield a generator of 'InsertDatapoints', which is then uploaded to CDF.
    A response has 7 sensor values, which means we yield 7 InsertDatapoints - each with a unique
    externalId and a single Datapoint.
    
    Parameters:
    imenco_camera_data (ImencoCameraData): Response from GET request to Imenco IP.

    Returns:
    A generator of 'InsertDatapoints' that will be uploaded to CDF. 
    Constructor: InsertDatapoints(
        external_id,
        List[Datapoint], where Datapoint = Tuple[TimeStamp, float]
    )' 
    """

    camera_name = imenco_path_to_camera_name_map[camera_id_to_path_map[imenco_camera_data.id]]
    
    # list with 1 'SensorData' value
    for camera_sensors in imenco_camera_data.CameraSensors: 
        for data_field in fields(camera_sensors):
            timestamp = datetime.now()
            # ts_ext_id = f"{camera_name}.{data_field.name}"
            ts_ext_id = f"imenco.ocean_farm_1.{camera_name}.{data_field.name}"
            value =  float(getattr(camera_sensors, data_field.name))
            print(timestamp, ts_ext_id, type(value), value)

            yield InsertDatapoints(
                # id=imenco_ext_id_to_id_map[ts_ext_id],
                datapoints=[(timestamp, value)],
                external_id=ts_ext_id
                )
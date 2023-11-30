import time
import yaml
from datetime import datetime
from dataclasses import fields

from cognite.extractorutils.uploader_types import InsertDatapoints
from cognite.extractorutils.rest.extractor import RestExtractor
from typing import Generator, List, Optional

from imenco_extractor import __version__
from imenco_extractor.dto import ImencoCameraData
from cognite.extractorutils.rest.http import HttpUrl, HttpCallResult

DEPLOY = True
imenco_config_path = '/config/imenco_config.yaml' if DEPLOY else 'config/imenco_config.yaml'
imenco_config_key = 'imenco_config' if DEPLOY else 'imenco_test_config'

extractor = RestExtractor(
    name="imenco_extractor",
    description="Imenco to TS",
    version=__version__
)

# Global config
def get_imenco_config():
    with open(imenco_config_path, 'r') as file:
        config = yaml.safe_load(file)
        imenco_config = config[imenco_config_key]
    return imenco_config

imenco_config = get_imenco_config()
print("\nConfig: ", imenco_config)

imenco_interval = int(imenco_config["interval"])
imenco_paths = imenco_config['paths']
imenco_next_paths = imenco_config['next_paths']
imenco_path_to_camera_name_map = imenco_config['imenco_path_to_camera_name_map']

# Global dictionary to track last execution time for each path
next_execution_time = {path: 0 for path in imenco_paths}


call_path = imenco_paths[-1]
def get_call_path_in_intervals() -> str:
    global call_path
    next_path = imenco_next_paths[call_path]
    call_path = next_path

    current_time = time.time()
    while current_time < next_execution_time[next_path]:
        time.sleep(0.1)
        current_time = time.time()
   
    next_execution_time[next_path] = current_time + imenco_interval
    print("NEW PATH", next_path)
    return next_path

def get_next_path_in_intervals(result : HttpCallResult) -> HttpUrl:
    print("\n"*3, "CALLED PATH", str(result.url))
    return HttpUrl(get_call_path_in_intervals())


'''
# How to update upload data from 12 cameras with 7 sensors into 12*7=84 time series in parallel?
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
3. For each response, we map each camera ID to a timeseries external ID. Then we extract the sensor data from the responses and build 7 datapoints for t
'''


@extractor.get(
    path=get_call_path_in_intervals,
    response_type=ImencoCameraData,
    next_page=get_next_path_in_intervals,
    interval=imenco_interval
)
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
    camera_name = imenco_path_to_camera_name_map[call_path]
    print("Setting value", call_path, "\tCamera", camera_name)
    
    # list with 1 'SensorData' value
    for camera_sensors in imenco_camera_data.CameraSensors: 
        for data_field in fields(camera_sensors):
            timestamp = int(datetime.now().timestamp() * 1000)
            ts_ext_id = f"imenco.ocean_farm_1.{camera_name}.{data_field.name}"
            value =  getattr(camera_sensors, data_field.name)
            if value:
                yield InsertDatapoints(
                    # id=imenco_ext_id_to_id_map[ts_ext_id],
                    datapoints=[(timestamp, float(value))],
                    external_id=ts_ext_id
                    )
import logging
import requests
from app.models import MetricLogs

logger = logging.getLogger(__name__)

servers = [
    {"name": "server_1", "host": "http://45.79.180.177:19999"},
    {"name": "server_2", "host": "http://45.33.68.115:19999"},
    {"name": "server_3", "host": "http://73.118.89.1:19999"},
    {"name": "server_4", "host": "http://66.228.32.144:19999"},
    {"name": "server_5", "host": "http://172.104.12.189:19999"},
]

def get_data(host, chart, points=1):
    """
    purpose: 
        * retrieve data from the netdata api
        * check data is not empty
    args:
        * host= server ip 
        * chart= metric to collect
        * points= default to 1, gets one data point (most recent)
    returns data 
    """ 
    try:
        url = f"{host}/api/v1/data?chart={chart}&points={points}&format=json"
        response = requests.get(url, timeout=5)
        data = response.json()
    
        # get most recent data point 
        if data and 'data' in data and len(data['data']) > 0:
            return data['data'][-1][1:]  
        return None
    
    except Exception as e:
        logger.error(f"Error retrieving {chart} from {host}: {str(e)}")
        return None
    
def store_metrics():
    """ 
    purpose: 
        * call get_data to get specific server metrics
        * add data to database 
    """
    for server in servers:
        # create new metric log model for each server 
        metric_log = MetricLogs(machine_name=server['name'])

        """ finish getting metrics """
        # get cpu data
        cpu_data = get_data[server["host"], "cpu_usage"]


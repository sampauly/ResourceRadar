import logging
import requests
from app.models import MetricLogs
from app import db
from datetime import datetime 

logger = logging.getLogger(__name__)

servers = [
    {"name": "server_1", "host": "http://45.79.180.177:19999"},
    {"name": "server_2", "host": "http://73.118.89.1:19999"},
    {"name": "server_3", "host": "http://66.228.32.144:19999"},
    {"name": "server_4", "host": "http://172.104.12.189:19999"},
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
    
        # get most recent data point and strip timestamp
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
        * creates metric_log models for each server 
        * commits changes to database
    """
    for server in servers:
        # create metric log model for each server 
        metric_log = MetricLogs(machine_name=server['name'])

        try:
            # get total cpu usage 
            cpu_data = get_data(server["host"], "system.cpu")
            if cpu_data:
                metric_log.cpu_usage = sum(cpu_data) 

            # get total network usage 
            network_data = get_data(server["host"], "system.net")
            if network_data:
                received = network_data[0]
                sent = abs(network_data[1])
                metric_log.network_usage = received + sent 

            # get total memory usage, not including cached and buffers
            memory_data = get_data(server["host"], "system.ram")
            if memory_data:
                used = memory_data[1]
                cached = memory_data[2]
                buffers = memory_data[3]
                total_mem_used = used - (cached + buffers)
                metric_log.memory_usage = total_mem_used

            # get disk usage as percentage, including disk space reserved for root 
            disk_data = get_data(server["host"], "disk_space./")
            if disk_data:
                disk_total = sum(disk_data)
                disk_used = sum(disk_data[1:])
                disk_percent_used = disk_used / disk_total * 100
                metric_log.disk_usage = disk_percent_used

            # log metrics in database
            db.session.add(metric_log)
            logger.info(f"{server["name"]} metrics collected.")
            
        except Exception as e:
            db.session.add(metric_log)
            logger.error(f"Error collecting metrics for {server["name"]}: {str(e)}")


    # commit all changes
    try:
        db.session.commit()
        logger.info(f"Server metrics saved at {datetime.now()}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database Error: {str(e)}")


            

            

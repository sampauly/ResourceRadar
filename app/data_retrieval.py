import logging
import requests
from datetime import datetime
from .models import MetricLogs, db
from . import scheduler

logger = logging.getLogger(__name__)

servers = [
    {"name": "server_1", "host": "http://45.79.180.177:19999"},
    {"name": "server_2", "host": "http://66.228.32.144:19999"}
]

def get_data(host, chart, points=1):
    """ Get raw data from Netdata Api and cleans it """
    try:
        url = f"{host}/api/v1/data?chart={chart}&points={points}&format=json"
        response = requests.get(url, timeout=5)
        data = response.json()

        # get most recent data point and strip timestamp
        if data and 'data' in data and len(data['data']) > 0:
            # return most recent data from 'data' label, stripping timestamp out
            return data['data'][-1][1:]
        return None

    except Exception as e:
        logger.error(f"Error retrieving {chart} from {host}: {str(e)}")
        return None

def store_metrics():
    """ Call get_data and compute specific data for each server then store to the respective MetricLog """
    with scheduler.app.app_context():
        for server in servers:
            # create metric log model for each server
            metric_log = MetricLogs(machine_name=server['name'])
            try:
                # get total cpu usage
                cpu_data = get_data(server["host"], "system.cpu")
                if cpu_data:
                    metric_log.cpu_usage = sum(cpu_data)

                # get network usage, sent and received 
                network_data = get_data(server["host"], "system.net")
                if network_data:
                    received = network_data[0]
                    sent = abs(network_data[1])
                    metric_log.network_received = received
                    metric_log.network_sent = sent 

                # get memory usage as percentage, excluding cache and buffers 
                memory_data = get_data(server["host"], "system.ram")
                if memory_data:
                    used = memory_data[1]
                    total = sum(memory_data)
                    memory_percent_used = used / total * 100
                    metric_log.memory_usage = memory_percent_used

                # get disk usage as percentage, including disk space reserved for root
                disk_data = get_data(server["host"], "disk_space./")
                if disk_data:
                    disk_total = sum(disk_data)
                    disk_used = sum(disk_data[1:])
                    disk_percent_used = disk_used / disk_total * 100
                    metric_log.disk_usage = disk_percent_used

                # log metrics in database
                db.session.add(metric_log)
                logger.info(f"{server['name']} metrics collected.")

            except RuntimeError as e:
                db.session.add(metric_log)
                logger.error(f"Error collecting metrics for {server['name']}: {str(e)}")

        try:
            db.session.commit()
            logger.info(f"Server metrics saved at {datetime.now()}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Database Error: {str(e)}")                

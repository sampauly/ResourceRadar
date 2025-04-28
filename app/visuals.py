"""
* get data from database 
* allow customization of timeline 

* Memory Usage: Total MiB of processes/information RAM is holding (MiB - mebibytes)
* CPU Usage: Total percent of processing power being utilized (percentage)
* Network Usage: Amount of kilobits per second being sent over the network, sent and received (kbit/s)
* Disk Usage: Percent of space used on device (percentage)
"""
from models import db

class GetMetrics(db):
    def get_connection():
        conn = db.connect()
        cursor = conn.cursor
        return cursor
    
    def latest_metrics():
        """ queries most recent data for both machines then returns a dictionary containing each servers data """
        # connect db to the backend 
        cursor = db.get_connection()

        # query most recent data using cursor 
        latest_metrics = cursor.execute('''
            SELECT *
            FROM metric_logs
            ORDER BY id DESC
            LIMIT 2
            ''').fetchall()
        
        # create a dictionary for each servers data 
        server_metrics = {}

        # populate dictionary
        for metric in latest_metrics:
            name = metric['machine_name']
            # if machine not yet in server metrics, add it 
            if name not in server_metrics:
                server_metrics[name] = {
                    # need timestamp
                    'timestamp': metric['timestamp'],
                    # need cpu_usage, memory_usage, network_usage, and disk_usage
                    'cpu_usage': metric['cpu_usage'],
                    'network_usage': metric['network_usage'],
                    'disk_usage': metric['disk_usage'],
                    'memory_usage': metric['memory_usage']
                }

        cursor.close()
        return server_metrics


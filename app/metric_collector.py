"""
* get data from database 
* allow customization of timeline 

* Memory Usage: Total MiB of processes/information RAM is holding (MiB - mebibytes)
* CPU Usage: Total percent of processing power being utilized (percentage)
* Network Usage: Amount of kilobits per second being sent over the network, sent and received (kbit/s)
* Disk Usage: Percent of space used on device (percentage)
"""
from .models import db, MetricLogs
from sqlalchemy import text

def get_connection():
    conn = db.engine.connect()
    return conn

def latest_metrics():
    """ queries most recent data for both machines then returns a dictionary containing each servers data """
    conn = get_connection()
    query_result = conn.execute(text('''
        SELECT *
        FROM metric_logs
        ORDER BY id DESC
        LIMIT 2
    ''')).mappings().all()

    latest_metrics = [dict(row) for row in query_result]

    conn.close()
    # create a dictionary for each servers data 
    server_metrics = {}
    for metric in latest_metrics:
        name = metric['machine_name']
        # if machine not yet in server metrics, add it 
        if name not in server_metrics:
            server_metrics[name] = {
                # need cpu_usage, memory_usage, network_usage, and disk_usage
                'cpu_usage': round(metric['cpu_usage'], 2),
                'network_usage': round(metric['network_usage'], 2),
                'disk_usage': round(metric['disk_usage'], 2),
                'memory_usage': round(metric['memory_usage'], 2)
            }

    return server_metrics


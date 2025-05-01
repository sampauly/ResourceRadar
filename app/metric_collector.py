"""
* get data from database 
* allow customization of timeline 

* Memory Usage: Total MiB of processes/information RAM is holding (MiB - mebibytes)
* CPU Usage: Total percent of processing power being utilized (percentage)
* Network Usage: Amount of kilobits per second being sent over the network,sent and recived (kbit/s)
* Disk Usage: Percent of space used on device (percentage)
"""
from .models import db
from sqlalchemy import text
from datetime import datetime

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
                'network_received': round(metric['network_received'], 2),
                'network_sent': round(metric['network_sent'], 2),
                'disk_usage': round(metric['disk_usage'], 2),
                'memory_usage': round(metric['memory_usage'], 2)
            }

    return server_metrics

def historical_metrics(metric_type: str, server_id: str, start_time: datetime, end_time: datetime) -> dict:
    """ allow custom querying over timespans and returns dict containing the relevant values """
    conn = get_connection()
    # map corresponding metric types
    metric_map = {
        'cpu': 'cpu_usage',
        'memory': 'memory_usage',
        'disk': 'disk_usage',
        'network': ['network_received', 'network_sent']
    }

    # validate metric_type
    if metric_type not in metric_map:
        raise ValueError(f"Invalid metric type: {metric_type}")

    # now get correct SQL queries
    if metric_type == 'network':
        query = text(f'''
            SELECT timestamp, network_received, network_sent
            FROM metric_logs
            WHERE machine_name = :server_id
            AND timestamp BETWEEN :start_time AND :end_time
            ORDER BY timestamp
        ''')
    else:
        metric = metric_map[metric_type]
        query = text(f'''
            SELECT timestamp, {metric}
            FROM metric_logs
            WHERE machine_name = :server_id
            AND timestamp BETWEEN :start_time AND :end_time
            ORDER BY timestamp
        ''')

    # execute query
    result = conn.execute(query, {
        'server_id': server_id,
        'start_time': start_time,
        'end_time': end_time 
    }).mappings().all()

    conn.close()

    # structure output
    if metric_type == 'network':
        return {
            'timestamps': [row['timestamp'] for row in result],
            'sent': [row['network_sent'] if row['network_sent'] is not None else 0 for row in result],
            'received': [row['network_received'] if row['network_received'] is not None else 0 for row in result]
        }
    else:
        return {
            'timestamps': [row['timestamp']for row in result],
            'values': [round(row[metric_map[metric_type]], 2) if row[metric_map[metric_type]] is not None else 0 for row in result]
        }

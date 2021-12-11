from purpleair.network import SensorList
import pandas as pd
import numpy as np
import time
import datetime
from datetime import date
from purpleair.sensor import Sensor


def get_sensor_data(sensor_id: int):
    p = SensorList()
    df = p.to_dataframe(sensor_filter='all',
                        channel='parent')
    name = df[df.index == sensor_id]['name'].values[0]
    sensor = Sensor(sensor_id, parse_location=True)
    df_sensor = sensor.parent.get_historical(weeks_to_get=14, start_date=date(2021, 12, 7),
                                             thingspeak_field='primary')
    df_sensor.created_at = pd.DatetimeIndex(df_sensor.created_at).tz_convert('US/Central')
    df_sensor['created_at'] = df_sensor['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    df_sensor['new_date'] = df_sensor.apply(lambda time: each_fifteen(time['created_at']), axis=1)
    df_sensor_date = df_sensor.drop(columns=['created_at'])
    df_sensor_date.sort_values('new_date', ascending=True)
    df_sensor_date_group = df_sensor_date.groupby('new_date').agg('mean').reset_index()
    df_sensor_date_group['sensor_name'] = name
    return df_sensor_date_group


def each_fifteen(time_str):
    new_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    new_time = new_time.replace(second=0)
    if new_time.minute < 8:
        new_time = new_time.replace(minute=0)
    elif new_time.minute < 23:
        new_time = new_time.replace(minute=15)
    elif new_time.minute < 38:
        new_time = new_time.replace(minute=30)
    elif new_time.minute < 53:
        new_time = new_time.replace(minute=45)
    elif new_time.minute < 60:
        new_time = new_time + datetime.timedelta(hours=1)
        new_time = new_time.replace(minute=0)
    return str(new_time)
    

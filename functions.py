import aqi
import pandas as pd
import numpy as np
from purpleair.network import SensorList
import time
import datetime
from datetime import date
from purpleair.sensor import Sensor
from numba import jit


def val_to_aqi(pollutant,input_col):
    import aqi
    # Supported  by AQI library
    #pm10 (µg/m³), o3_8h (ppm), co_8h (ppm), no2_1h (ppb), o3_1h (ppm), so2_1h (ppb), pm25 (µg/m³)
    temp=[]
    for i in input_col.tolist():
        if i >=0:
            cal_aqi = int(aqi.to_aqi([(getattr(aqi, pollutant), i)]))
            temp.append(cal_aqi)
        else:
            call_aqi=0
            temp.append(cal_aqi)
    return temp


def combined_aqi(readings):
    vals= readings[1:5]
    if all(i >= 0 for i in vals):
        myaqi = aqi.to_aqi([
        (aqi.POLLUTANT_CO_8H, readings[1]),
        (aqi.POLLUTANT_NO2_1H, readings[2]),
        (aqi.POLLUTANT_O3_8H, readings[3]),
        (aqi.POLLUTANT_PM10, readings[4]),
        (aqi.POLLUTANT_PM25, readings[5])
         ])
    else:
        myaqi = aqi.to_aqi([
        (aqi.POLLUTANT_CO_8H, readings[1]),
        (aqi.POLLUTANT_O3_8H, readings[3]),
        (aqi.POLLUTANT_PM10, readings[4]),
        (aqi.POLLUTANT_PM25, readings[5])
         ])
    return int(myaqi)


@jit(nopython=True)
def get_label(val):
    if val <= 50:
        label = "Good"
    elif val >= 51 and val <= 100:
        label = 'Moderate'
    elif val >= 101 and val <= 150:
        label = 'Unhealthy for Sensitive Groups'
    elif val >= 151 and val <= 200:
        label = 'Unhealthy'
    else:
        label = "Very Unhealthy"
    return label


def get_sensor_data(sensor_id: int) -> pd.DataFrame:
    """ Use the sensor_id to get the data from purple air

    :param sensor_id: The id of the sensor from purple air
    :return: The data frame the sensor get from

    >>> get_sensor_data(10894)
    Initialized 22,445 sensors!
                     new_date  ...    sensor_name
    0     2021-08-23 19:00:00  ...  Warnow-Chacko
    1     2021-08-23 19:15:00  ...  Warnow-Chacko
    2     2021-08-23 19:30:00  ...  Warnow-Chacko
    3     2021-08-23 19:45:00  ...  Warnow-Chacko
    4     2021-08-23 20:00:00  ...  Warnow-Chacko
    ...                   ...  ...            ...
    7565  2021-12-06 17:00:00  ...  Warnow-Chacko
    7566  2021-12-06 17:15:00  ...  Warnow-Chacko
    7567  2021-12-06 17:30:00  ...  Warnow-Chacko
    7568  2021-12-06 17:45:00  ...  Warnow-Chacko
    7569  2021-12-06 18:00:00  ...  Warnow-Chacko
    <BLANKLINE>
    [7570 rows x 10 columns]

    """
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


def each_fifteen(time_str: str) -> str:
    """Calculate the data in each fifteen minutes to match the timestamp from sensor located in UIUC

    :param time_str: the time with string type
    :return: the time with string type based on each 15 minutes

    >>> each_fifteen('2021-11-29 18:01:19')
    '2021-11-29 18:00:00'

    """
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


quantile_time_dict = {}


def is_time_outlier(quantile: pd.DataFrame, time: datetime.time, PM25: int):
    """ Determine whether the PM2.5 based on time if the outlier

    :param quantile: dataframe
    :param time: time with datetime.time type
    :param PM25: the number of PM2.5
    :return: whether the PM2.5 is the outlier

    >>> quantile_time_dict = {}
    >>> quantile = get_sensor_data(10894)
    Initialized 22,445 sensors!
    >>> quantile['time'] = pd.to_datetime(quantile['new_date'],format='%Y-%m-%d %H:%M:%S').dt.time
    >>> is_time_outlier(quantile, datetime.time(4, 45), 5)
    'F'

    """
    if time not in quantile_time_dict:
        Q1 = quantile[quantile['time'] == time]['PM2.5 (CF=1) ug/m3'].quantile(0.25)
        Q3 = quantile[quantile['time'] == time]['PM2.5 (CF=1) ug/m3'].quantile(0.75)
        IQR = Q3 - Q1
        outlier = Q3 + 1.5 * IQR
        quantile_time_dict[time] = outlier
    else:
        outlier = quantile_time_dict[time]
    if PM25 > outlier:
        return 'T'
    else:
        return 'F'


quantile_dayofweek_dict = {}


def is_date_outlier(quantile, dayofweek, PM25):
    """ Determine whether the PM2.5 based on day of week if the outlier

    :param quantile: dataframe
    :param time: day of week
    :param PM25: the number of PM2.5
    :return: whether the PM2.5 is the outlier

    >>> quantile = get_sensor_data(10894)
    Initialized 22,445 sensors!
    >>> quantile['dayofweek'] = pd.to_datetime(quantile['new_date'],format='%Y-%m-%d %H:%M:%S').dt.dayofweek
    >>> is_date_outlier(quantile, 0, 5)
    'F'

    """
    if dayofweek not in quantile_dayofweek_dict:
        Q1 = quantile[quantile['dayofweek'] == dayofweek]['PM2.5 (CF=1) ug/m3'].quantile(0.25)
        Q3 = quantile[quantile['dayofweek'] == dayofweek]['PM2.5 (CF=1) ug/m3'].quantile(0.75)
        IQR = Q3 - Q1
        outlier = Q3 + 1.5 * IQR
        quantile_dayofweek_dict[dayofweek] = outlier
    else:
        outlier = quantile_dayofweek_dict[dayofweek]
    if PM25 > outlier:
        return 'T'
    else:
        return 'F'

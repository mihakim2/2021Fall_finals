import aqi
import pandas as pd
import numpy as np

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

def get_label(val):
    if val <=50:
        label = "Good"
    elif val>=51 and val<=100:
        label = 'Moderate'
    elif val>=101 and val<=150:
        label = 'Unhealthy for Sensitive Groups'
    elif val>=151 and val<=200:
        label = 'Unhealthy'
    else:
        label = "Very Unhealthy"
    return label
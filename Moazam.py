"""
597PR Fall 2021.
Assignment on NetworkX
Moazam's portion
"""
import pandas as pd
from sys import stdin
import numpy as np

total_messages = 0
callsign_messages = 0
callsigns= [np.array([],dtype = np.uint32)]
for line in stdin:
    total_messages += 1
    data = line.split(",")
    if len(data[10]) != 0:
        callsign_messages += 1
        callsigns= np.append(data[10],callsigns)
    else:
        pass
    if total_messages % 500 == 0:
        print('\nMessage counts: total {} CallSigns: {}\n'.format(total_messages, callsign_messages))
print(len(callsigns))

# col_list = ['MessageType', 'TransmissionType', 'SessionID', 'AircraftID', 'AircraftHex', 'FlightRecorderNum',
#                 'DateGenerated','TimeGenerated', 'DateLogged', 'TimeLogged', 'Callsign/FlightNum', 'Altitude',
#                 'GroundSpeed','Track/Heading','Latitude', 'Longitude', 'VerticalRate', 'SquawkCode',
#                 'Alert (Squawk Change)', 'Emergency', 'SPI','OnGround']

# def read_csv_flight(path):
#
#     data = pd.read_csv('sample_log.csv', header=None)
#     data.rename(columns={i: j for i, j in zip(list(data), col_list)}, inplace=True)
#     df = data[~data['Callsign/FlightNum'].isnull()].copy()
#     return df['Callsign/FlightNum']
#
#
# df = read_csv_flight('sample_log.csv')
# print(df.head(100))
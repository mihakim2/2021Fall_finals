"""
597PR Fall 2021.
Assignment on NetworkX
Moazam's portion
"""
import pandas as pd
from sys import stdin
import io

total_messages = 0
callsign_messages = 0

for line in stdin:
    total_messages += 1
    data = line.split(",")
    if len(data[10]) != 0:
        callsign_messages += 1
        # print("True")
    else:
        pass
    if total_messages % 500 == 0:
        print('\nMessage counts: total {} type 3: {}\n'.format(total_messages, callsign_messages))

col_list = ['MessageType', 'TransmissionType', 'SessionID', 'AircraftID', 'AircraftHex', 'FlightRecorderNum',
                'DateGenerated','TimeGenerated', 'DateLogged', 'TimeLogged', 'Callsign/FlightNum', 'Altitude',
                'GroundSpeed','Track/Heading','Latitude', 'Longitude', 'VerticalRate', 'SquawkCode',
                'Alert (Squawk Change)', 'Emergency', 'SPI','OnGround']

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
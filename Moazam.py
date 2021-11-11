"""
597PR Fall 2021.
Assignment on NetworkX
Moazam's portion
"""
import pandas as pd

def read_csv_flight(path):
    col_list = ['MessageType', 'TransmissionType', 'SessionID', 'AircraftID', 'AircraftHex', 'FlightRecorderNum',
                'DateGenerated','TimeGenerated', 'DateLogged', 'TimeLogged', 'Callsign/FlightNum', 'Altitude',
                'GroundSpeed','Track/Heading','Latitude', 'Longitude', 'VerticalRate', 'SquawkCode',
                'Alert (Squawk Change)', 'Emergency', 'SPI','OnGround']
    data = pd.read_csv('sample_log.csv', header=None)
    data.rename(columns={i: j for i, j in zip(list(data), col_list)}, inplace=True)
    df = data[~data['Callsign/FlightNum'].isnull()].copy()
    return df['Callsign/FlightNum']


df = read_csv_flight('sample_log.csv')
print(df.head(100))
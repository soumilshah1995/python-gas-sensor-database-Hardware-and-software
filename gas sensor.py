import geocoder
import datetime
import time
import serial
import sqlite3


global counter
counter = 0

global pcounter
pcounter = 0

global start_t

start_t=time.time()


def read_data():
    try:
        global counter
        arduinodata =serial.Serial('COM6',115200,timeout=0.1)
        while arduinodata.inWaiting:
            val=arduinodata.readline().decode('ascii')
            if len(val) > 9:
                counter = counter + 1
                if counter > 4:
                    if 'version = 2' not in val:
                        print(val)
                        return val

    except:
        print('error reading data')

def get_geolocations():
    try:
        g = geocoder.ip('me')
        my_string=g.latlng
        longitude=my_string[0]
        latitude=my_string[1]
        return longitude,latitude
    except:
        print('Could Not Get the  Co-ordinates!')

def get_date_time():
    try:
        mytime = datetime.datetime.now()
        tm= '{}:{}:{}'.format(mytime.hour,mytime.minute,mytime.second)
        dt= '{}/{}/{}'.format(mytime.month,mytime.day,mytime.year)
        return tm,dt
    Q:
        print('Error Cannot get Date and Time ')


def add_db(time, NH3, CO, dt, longitude, latitude):
    try:
        conn=sqlite3.connect('Gas.db')
        c=conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS data 
        (Time TEXT,NH3 TEXT,CO TEXT,Date TEXT,longitude TEXT,latitude TEXT)""")

        c.execute(""" INSERT INTO data
        (Time, NH3, CO, Date,longitude, latitude)
        VALUES (?, ?, ?, ?, ?, ?)""", (time, NH3, CO, dt,longitude,latitude))

        conn.commit()
        c.close()
        conn.close()
    except:
        print('Cannot add to Datbase!')


def raw_process_data():


    global pcounter

    NH3,CO = read_data().split(',')
    tm,dt=get_date_time()
    longitude,latitude=get_geolocations()
    pcounter= pcounter+1


    if pcounter == 12:
        add_db(tm,NH3,CO,dt,longitude,latitude)
        pcounter = 0


if __name__ == '__main__':
    while 1:
        raw_process_data()
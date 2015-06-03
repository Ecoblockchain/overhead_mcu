# test to see what azimuth and elevation look like 
# for different satellites.
# Plotting both angular position and velocity


import ephem
import requests

# plots
import numpy as np
import math
import matplotlib.pyplot as plt

import time
from datetime import date
from datetime import timedelta

from array import array

brightest100 = 'http://celestrak.com/NORAD/elements/visual.txt'

satellite_bodies = {}
TLE_array = {}

# Read in some TLE of various satellites (different types of orbits)
# from tomas' server code

resp = requests.get(brightest100).content
resp = map(str.strip, resp.split('\r\n'))

for i in xrange(0, len(resp)-1, 3):
    TLE_array[resp[i]] = resp[i:i+3] # dictionary of satellite name to full TLE info
#bodies
for sat, TLE in TLE_array.iteritems():
    satellite_bodies[sat] = ephem.readtle(TLE[0], TLE[1], TLE[2])


# define an observer in berkeley, CA
berkeley = ephem.Observer()
berkeley.lat = 37.8717
berkeley.lon = 122.2728
berkeley.date = date.today()
berkeley.horizon = '30' # 30 degrees, minimum tilt above horizon for satellite tracker # TODO: doesn;t seem to be changing rise and fall times

print (berkeley.horizon)


# find the next rise and fall time of some interesting ones

sat1 = satellite_bodies['GENESIS 1']
sat1.compute(berkeley) # bug in pyephem, next_pass uses the horizon of the last time compute was called, instead of the horizon of the observer

# get set and rise time
sat1_info = berkeley.next_pass(sat1)
sat_rise_time = sat1_info[0]
sat_set_time = sat1_info[4]


# array of 100 points to plot per rise/fall cycle
x = np.linspace(sat_rise_time, sat_set_time, 100, endpoint = True) #print type(x) # numpy.ndarray

az = np.empty([100, 1])
alt = np.empty([100, 1])
# az and alt

for i in range(0, 100):
    berkeley.date = x[i] # update the date
    sat1.compute(berkeley)

    az[i] = float(repr(sat1.az)) * 180 / math.pi

    alt[i] = float(repr(sat1.alt)) * 180 / math.pi


print sat_rise_time
print sat_set_time


# plot yo shit

# first change x to minutes

x = x/ephem.minute;
plt.plot(x, az)
plt.plot(x, alt)
plt.xlabel('time in minutes')
plt.ylabel('degrees')
plt.show()



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Aug 1 16:41:46 2024

@author: elizabeth.smith
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt


#%%


#File paths to the location of the data file on your computer
path_to_files = '/Users/elizabeth.smith/Documents/Scripts/Courses/'
data_file = 'KOUN_20200828_230247.cdf'

#netcdf4 open statement ('r' means read only). Not the only way to do this...
ncfile = Dataset('{}{}'.format(path_to_files,data_file),'r')

#reading variables from the datafile
Pressure = ncfile.variables['Pressure'][:]
Temperature = ncfile.variables['Temperature'][:]
RH = ncfile.variables['RH'][:]
Height = ncfile.variables['Height'][:]
Wspd = ncfile.variables['Wspd'][:]
Wdir = ncfile.variables['Wdir'][:]

#close the file you opened! 
ncfile.close()


#%%

# A figure setting to make fonts big enough to read
plt.rcParams['font.size'] = 20

# building a figure with
# subplots can be used to make multiple or one 'subplot' which your
# axis object can refer to. 
fig, ax = plt.subplots(figsize=(8,12))

# Plot temperature
ax.plot(Temperature, Height, 'r-', lw=3,label='Temperature (°C)')
# color the labels/ticks to match can be useful sometimes 
ax.set_xlabel('Temperature (°C)',color='r')
ax.tick_params('x', colors='r')
ax.set_ylabel('Height (m)')
# setting data ranges for the axes
ax.set_ylim(0,3000)
ax.set_xlim(0,40)

# this sets up a nice background grid for our plot
ax.grid()

# shows the figure in your console, etc.
plt.show()

# show and save often don't work well together so pick one!  

# save the figure to a location of your choice. Now using the same path as above
# always close figures that you save or your computer will eventually hate you. 

#plt.savefig('{}Figure_exampleHW1.png'.format(path_to_files))
#plt.close()


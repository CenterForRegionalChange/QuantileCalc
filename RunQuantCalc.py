'''
Created on May 29, 2015

@author: roth
'''

import arcpy
import QuantFunc as qf


# List of fields to run
fldlist = ['people_mean','place_mean','edppl_mean','hsppl_mean','moppl_mean','enppl_mean']

dataset = r"D:\Projects\crc\QuantileCalc\Quantiles.gdb\Roi_data"
qnum = 5
qdir = 'Normal'


print("Starting")
for fld in fldlist:
    try:
        print("Working on: {fld}".format(fld=fld))
        qf.Quantiles(dataset, fld, qnum, qdir)
    except:
        print("Failed on field")
print("Done")


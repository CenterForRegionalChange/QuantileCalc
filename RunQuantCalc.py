'''
Created on May 29, 2015

@author: roth
'''

"""
A Utility wrapper for assigning quantiles to many fields in a dataset.

"""



import arcpy
import QuantFunc as qf
import os

# Input Datast
dataset = r"D:\Projects\crc\QuantileCalc\testing\Quantiles.gdb\ROI_1213_Q2"

# List of fields to run
fldlist = ['people_mean','place_mean','edppl_mean','ecppl_mean','hsppl_mean','moppl_mean','enppl_mean','soppl_mean','edplc_mean','ecplc_mean','hsplc_mean','enplc_mean','soplc_mean','postsec','prof_math','prof_ela','truant','emp','above200fpl','ownhome','hsg30','vehicles','comm30','hsi_rfc','hlthwt','teenb','ypll_rate','voted10','englishwell','grad_rate','ucgrads','exp_ed','expsusp','jobs_pc5','jobgr5','hqjobrat','banks_pc5','bizgr5','occup1less','affhousing','pm25','pncare','foodaccess','hcprov_pc5','citizen','sameres']

# Setting up feature layer for queries. This line is needed regardless of whether you're filtering based on a query.
arcpy.MakeFeatureLayer_management(dataset, "quant_lyr")

qnum = 5
qdir = 'Normal'

print("Starting")
for fld in fldlist:
    try:
        print("Working on: {fld}".format(fld=fld))
        whereClause = "" # whereClause = "totpop > 3000"  # or "COUNTYFP10 = '037'"  ## Moving the whereClause inside the loop slows down the operation because it's doing the selection on each iteration, but allows for more specific handling of the layer.
        arcpy.SelectLayerByAttribute_management ("quant_lyr", "NEW_SELECTION", whereClause)
        qf.Quantiles("quant_lyr", fld, qnum, qdir)
    except Exception, e:
        print("Failed on field")
        print(str(e))
        
print("Done")


'''
Created on May 29, 2015

@author: roth
'''
import arcpy
import arcpy.da as da
import numpy as np
import numpy.lib.recfunctions as rfn
import cPickle as pickle


def Quantiles(in_features, in_field, in_quant):
    #print("converting to numpy")
    nparray = da.FeatureClassToNumPyArray(in_features,["OID@",in_field],skip_nulls = True)
     
    #print("calculating quantiles")
    n = 1.0/float(in_quant)
    qs = [n*x*100 for x in xrange(1,int(in_quant)+1)] #qs is the percentages that the data should be broken at i.e. 20, 40, 60. 80, 100%ile
    #print(qs)
     
    #print("calculating percentiles")
    flcol = np.array(nparray[[str(in_field)]], np.float)
    pso = np.percentile(flcol, qs) #pso is the the breakpoints between quantiles
    minval = flcol.min()
    #print(ps)
     
    #print("Adding new numpy field")
    newfldname = "".join(["Q",in_field])
     
    #print("Assign Quantiles")
    #quants = AssignQuant(flcol,ps,minval) #quants was previously called "out"
    # This section was previously the function AssignQuant
    ps = [x for x in pso] # converting to a list from an array for ease of use
    ps = [minval] + ps # specify the bottom end
    print(ps)
    quantList = []
    rng = range(1,len(ps)+1)
    for x in flcol:
        for i in rng: 
            if  ps[i-1] <= x <= ps[i]:
                quantList.append(i)
                break

    quants = np.array(quantList)
    # End assign quant function
    

    nparray2 = rfn.append_fields(nparray, str(newfldname), quants, usemask = False)
    nparray3 = nparray2[['OID@',str(newfldname)]] # Reduce the numpy array to just OID and the Quantile
    
    #print("Extend table to include the new values")
    da.ExtendTable(in_features,"OBJECTID" ,nparray3,"OID@")
 
    #print("Done")



# 
# def AssignQuant(a,pso,minval):
#     ps = [x for x in pso] # converting to a list from an array for ease of use
#     ps = [minval] + ps
#     print(ps)
#     out = []
#     rng = range(1,len(ps)+1)
#     #print(rng)
#     for x in a:
#     #for x in np.nditer(a,op_flags=['readwrite']):
#         for i in rng: 
#             if  ps[i-1] <= x <= ps[i]:
#                 #x = i+1
#                 out.append(i)
#                 break
# 
#     outarr = np.array(out)
#     return(outarr)
# 
# def Quantiles_old(in_features, in_field, in_quant, in_qdir):
#     #print("converting to numpy")
#     nparray = da.FeatureClassToNumPyArray(in_features,["OID@",in_field],skip_nulls = True)
#      
#     #print("calculating quantiles")
#     n = 1.0/float(in_quant)
#     qs = [n*x*100 for x in xrange(1,int(in_quant)+1)]
#     #print(qs)
#      
#     #print("calculating percentiles")
#     flcol = np.array(nparray[[str(in_field)]], np.float)
#     ps = np.percentile(flcol, qs)
#     minval = flcol.min()
#     #print(ps)
#      
#     #print("Adding new numpy field")
#     newfldname = "".join(["Q",in_field])
#      
#     #print("Assign Quantiles")
#     out = AssignQuant(flcol,ps,minval)
#     pickle.dump( out, open( "out.p", "wb" ) )
#     if in_qdir == "Reverse":
#         out = (int(in_quant) + 1) - out
#      
#     nparray2 = rfn.append_fields(nparray, str(newfldname), out, usemask = False)
#     #nparray2[newfldname] = out
#     nparray3 = nparray2[['OID@',str(newfldname)]]
#     
#     #print("Extend table to include the new values")
#     da.ExtendTable(in_features,"OBJECTID" ,nparray3,"OID@")
#  
#     #print("Done")

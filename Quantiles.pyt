import arcpy
import os
import arcpy.da as da
import numpy as np
import numpy.lib.recfunctions as rfn
import QuantFunc as qf


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


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "CRC Tools"
        self.alias = "crctools"

        # List of tool classes associated with this toolbox
        self.tools = [QuantileCalc1,QuantileCalc2,QuantileCalc3]


class QuantileCalc1(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Quantile Calculator 1: Self contained"
        self.description = "Fully Self Contained."
        self.canRunInBackground = False
        self.category = None

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        
        param1 = arcpy.Parameter(
            displayName="Input Field",
            name="in_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        param1.parameterDependencies = [param0.name]
 
        param2 = arcpy.Parameter(
            displayName="Number of Quantiles",
            name="in_quant",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
         
        
        param3 = arcpy.Parameter(
            displayName="Output Features",
            name="out_features", 
            datatype="GPFeatureLayer",
            parameterType="Derived",
            direction="Output")
        param3.parameterDependencies = [param0.name]
        param3.schema.clone = True
        
        params = [param0,param1,param2,param3] 

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        # Get the variables
        in_features = parameters[0].valueAsText
        in_field = parameters[1].valueAsText
        in_quant = parameters[2].valueAsText
        
        # Execute function above
        messages.addMessage("Starting Quantile Function")
        
        ############################################################
        # Code below is identical to that in RunQuantCalc
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
        # End Code Paste
        ##################################################
        messages.addMessage("Quantile Function Complete")
        
        return

class QuantileCalc2(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Quantile Calculator 2: Calls function internal to .pyt"
        self.description = "Calls a function within this pyt."
        self.canRunInBackground = False
        self.category = None

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        
        param1 = arcpy.Parameter(
            displayName="Input Field",
            name="in_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        param1.parameterDependencies = [param0.name]
 
        param2 = arcpy.Parameter(
            displayName="Number of Quantiles",
            name="in_quant",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
         
        
        param3 = arcpy.Parameter(
            displayName="Output Features",
            name="out_features", 
            datatype="GPFeatureLayer",
            parameterType="Derived",
            direction="Output")
        param3.parameterDependencies = [param0.name]
        param3.schema.clone = True
        
        params = [param0,param1,param2,param3] 

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        # Get the variables
        in_features = parameters[0].valueAsText
        in_field = parameters[1].valueAsText
        in_quant = parameters[2].valueAsText
        
        # Execute function above
        messages.addMessage("Starting Quantile Function")
        Quantiles(in_features,in_field,in_quant) # Calling function Quantiles from above
        messages.addMessage("Quantile Function Complete")
        
        return
    
class QuantileCalc3(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Quantile Calculator 3: Calls function from external module"
        self.description = "Calls a function from a module."
        self.canRunInBackground = False
        self.category = None

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        
        param1 = arcpy.Parameter(
            displayName="Input Field",
            name="in_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        param1.parameterDependencies = [param0.name]
 
        param2 = arcpy.Parameter(
            displayName="Number of Quantiles",
            name="in_quant",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
         
        
        param3 = arcpy.Parameter(
            displayName="Output Features",
            name="out_features", 
            datatype="GPFeatureLayer",
            parameterType="Derived",
            direction="Output")
        param3.parameterDependencies = [param0.name]
        param3.schema.clone = True
        
        params = [param0,param1,param2,param3] 

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        # Get the variables
        in_features = parameters[0].valueAsText
        in_field = parameters[1].valueAsText
        in_quant = parameters[2].valueAsText
        
        # Execute function above
        messages.addMessage("Starting Quantile Function")
        qf.Quantiles(in_features,in_field,in_quant) # Calling function Quantiles from above
        messages.addMessage("Quantile Function Complete")
        
        return


# if __name__ == "__main__":
#     in_features = r"D:\Projects\crc\QuantileCalc\Quantiles.gdb\Roi_data"
#     in_field = "people_mean"
#     in_quant = 5
#     in_qdir = "Normal"
#         
#     Quantiles(in_features, in_field, in_quant, in_qdir)
    

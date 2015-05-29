import arcpy
import arcpy.da as da
import numpy as np
import numpy.ma as ma

def AssignQuant(a,pso):
    ps = [x for x in pso]
    ps = [0.0] + ps
    print(ps)
    out = []
    rng = range(1,len(qs)+1)
    print(rng)
    for x in np.nditer(a,op_flags=['readwrite']):
        for i in rng: 
            if  ps[i-1] < x <= ps[i]:
                #x = i+1
                out.append(i)
                break
    outarr = np.array(out)
    return(outarr)

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "CRC Tools"
        self.alias = "crctools"

        # List of tool classes associated with this toolbox
        self.tools = [QuantileCalc]


class QuantileCalc(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Quantile Calculator"
        self.description = "A tool to add a new field, and calculate the quantile into it for each selected element."
        self.canRunInBackground = False
        self.category = 'Quantiles'

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
            displayName="Direction of Quantiles",
            name="in_qdir", # Normal or Reverse
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param3.filter.list = ['Normal','Reverse']
        
        param4 = arcpy.Parameter(
            displayName="Output Features",
            name="out_features", # Normal or Reverse
            datatype="GPFeatureLayer",
            parameterType="Derived",
            direction="Output")
        param4.parameterDependencies = [param0.name]
        param4.schema.clone = True
        
        params = [param0,param1,param2,param3,param4] #[param0,param1,param2,param3,param4]

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
        in_qdir = parameters[3].valueAsText
        
        # Convert to numpyarray
        
        messages.addMessage("Converting to Numpy")
        nparray = da.FeatureClassToNumPyArray(in_features,["OID@",in_field],skip_nulls = True)
        messages.addMessage("Converted to Numpy")
        
        # Set percentiles.
        n = 1.0/float(in_quant)
        qs = [n*x*100 for x in xrange(1,int(in_quant)+1)]
        
        flcol = np.array(nparray[[in_field]], np.float)
        ps = np.percentile(flcol, qs)
        
        for p in ps:
            messages.addMessage("Quantile: {q}".format(q = str(p)))
         
        # make new field name to hold quantiles 
        messages.addMessage("Adding field to numpyarray")  
        newfldname = "".join(["Q",in_field])
        fldtype = (newfldname,'<i4') # have tried '<i4', and 'integer' same result
        dtype=nparray.dtype.descr
        dtype.append(fldtype)
        dtype2 = np.dtype(dtype) # Error unrecognized data type
        nparray2 = np.empty(nparray.shape, dtype=dtype2) 
        for name in nparray.dtype.names:
            nparray2[name] = nparray[name]

        
        # Setting quantiles
        messages.addMessage("Setting quantiles")
        out = AssignQuant(flcol,ps)
        
        if in_qdir == "Reverse":
            messages.addMessage("Quantiles are in reverse order")
            out = (int(in_quant) + 1) - out
        
        nparray2[newfldname] = out
        nparray3 = nparray2[['OID@',newfldname]]
        
        messages.addMessage("Joining to table")
        arcpy.da.ExtendTable(in_features,"OBJECTID" ,nparray3,"OID@")
        
        return



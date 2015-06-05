import arcpy
import arcpy.da as da
import numpy as np
import numpy.lib.recfunctions as rfn


def AssignQuant(a,pso):
    ps = [x for x in pso]
    ps = [0.0] + ps
    print(ps)
    out = []
    rng = range(1,len(ps)+1)
    print(rng)
    for x in np.nditer(a,op_flags=['readwrite']):
        for i in rng: 
            if  ps[i-1] < x <= ps[i]:
                #x = i+1
                out.append(i)
                break
    outarr = np.array(out)
    return(outarr)

def Quantiles(in_features, in_field, in_quant, in_qdir):
    print("converting to numpy")
    nparray = da.FeatureClassToNumPyArray(in_features,["OID@",in_field],skip_nulls = True)
    
    print("calculating quantiles")
    n = 1.0/float(in_quant)
    qs = [n*x*100 for x in xrange(1,int(in_quant)+1)]
    print(qs)
    
    print("calculating percentiles")
    flcol = np.array(nparray[[in_field]], np.float)
    ps = np.percentile(flcol, qs)
    print(ps)
    
    print("Adding new numpy field")
    newfldname = "".join(["Q",in_field])
#     fldtype = (newfldname,'int32',)
#     dtype=nparray.dtype.descr
#     dtype.append(fldtype)
#     dtype2 = np.dtype(dtype)
#     nparray2 = np.empty(nparray.shape, dtype=dtype2)
#     for name in nparray.dtype.names:
#         nparray2[name] = nparray[name]
    
    print("Assign Quantiles")
    out = AssignQuant(flcol,ps)
    if in_qdir == "Reverse":
        out = (int(in_quant) + 1) - out
    
    nparray2 = rfn.append_fields(nparray, str(newfldname), out, usemask = False)
    #nparray2[newfldname] = out
    nparray3 = nparray2[['OID@',newfldname]]
   
    print("Extend table to include the new values")
    da.ExtendTable(in_features,"OBJECTID" ,nparray3,"OID@")

    print("Done")



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
            name="out_features", 
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
        
        # Execute function above
        messages.addMessage("Starting Quantile Function")
        Quantiles(in_features, in_field, in_quant, in_qdir)
        messages.addMessage("Quantile Function Complete")
        
        return

if __name__ == "__main__":
    in_features = r"D:\Projects\crc\QuantileCalc\Quantiles.gdb\Roi_data"
    in_field = "people_mean"
    in_quant = 5
    in_qdir = "Normal"
        
    Quantiles(in_features, in_field, in_quant, in_qdir)
    

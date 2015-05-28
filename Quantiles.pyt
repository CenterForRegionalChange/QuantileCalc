import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "CRC Quantiles"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [QuantileCalc]


class QuantileCalc(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Quantile Calculator"
        self.description = "A tool to add a new field, and calculate the quantile into it for each selected element."
        self.canRunInBackground = False

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
        
        param2 = arcpy.Parameter(
            displayName="Number of Quantiles",
            name="in_quant",
            datatype="Integer",
            parameterType="Required",
            direction="Input")
        
        param3 = arcpy.Parameter(
            displayName="Direction of Quantiles",
            name="in_qdir", # Normal or Reverse
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        
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
        return

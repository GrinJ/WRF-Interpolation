from src.WRFInterpolation.WRFInterpolation import WRFInterpolation
from ../CTLReader/src.CTLReader.CTLReader import CTLReader

#Read coords from CTL
coords = CTLReader("CTL data/coord_18km.ctl")

#Create interpolate class object
inter = WRFInterpolation(coords["XLAT"], coords["XLONG"])

#Read the main CTL file
forecast = CTLReader("path_to_the_ctl")

#Interpolate
result = inter.bilinear("12.34", "56.78", forecast["T2"])
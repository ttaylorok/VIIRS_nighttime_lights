import gdal
import struct
from osgeo import osr
import os
import pyproj



hdf_file = gdal.Open("DATA/MODIS/MOD13A1.A2018353.h11v10.006.2019032133245.hdf")
subDatasets = hdf_file.GetSubDatasets()

# https://modis.gsfc.nasa.gov/data/dataprod/mod13.php
# extract fire band
dataset = gdal.Open(subDatasets[0][0])
geotransform = dataset.GetGeoTransform()
band = dataset.GetRasterBand(1)

# p = pyproj.Proj("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs")
# fmttypes = {'Byte':'B', 'UInt16':'H', 'Int16':'h', 'UInt32':'I', 
#             'Int32':'i', 'Float32':'f', 'Float64':'d'}

# gtest = open("cali_2018_fires_output.csv",'w')
# gtest.write("lat,lon,class,date,X,Y\n")
# for filename in os.listdir("cali_2018_data"):
#     print(filename)

#     hdf_file = gdal.Open("cali_2018_data/"+filename)
#     subDatasets = hdf_file.GetSubDatasets()
    
#     # extract fire band
#     dataset = gdal.Open(subDatasets[0][0])
#     geotransform = dataset.GetGeoTransform()
#     band = dataset.GetRasterBand(1)
    
#     # extract coverage date from metadata
#     meta = dataset.GetMetadata_Dict()
#     date = meta["RANGEBEGINNINGDATE"]
    
#     BandType = gdal.GetDataTypeName(band.DataType)
    
#     #geotransform parameters
#     X = geotransform[0]
#     Y = geotransform[3]
    
#     for y in range(band.YSize):
    
#         scanline = band.ReadRaster(0, 
#                                    y, 
#                                    band.XSize, 
#                                    1, 
#                                    band.XSize, 
#                                    1, 
#                                    band.DataType)
    
#         values = struct.unpack(fmttypes[BandType] * band.XSize, scanline)
    
#         for value in values:
    
#             if(value == 7 or value == 8 or value == 9):
#                 lon, lat = p(X, Y, inverse=True)
#                 gtest.write("%.6f, %.6f, %.2f, %s, %d, %d\n" % (lat, lon, value, date, X, Y))
#             X += geotransform[1] #x pixel size
#         X = geotransform[0]
#         Y += geotransform[5] #y pixel size

# gtest.close()
# #dataset = None

# # proj = dataset.GetProjection()

# # from osgeo import osr
# # srs = osr.SpatialReference()
# # wkt_text = str(proj)
# # srs.ImportFromWkt(wkt_text)
# # srs.ExportToProj4()





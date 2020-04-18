import gdal
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import struct
from bitstring import BitArray


fmttypes = {'Byte':'B', 'UInt16':'H', 'Int16':'h', 'UInt32':'I', 
            'Int32':'i', 'Float32':'f', 'Float64':'d'}

path = 'DATA/VIIRS_himalayas/'
files = []
for filename in os.listdir(path):
    if filename.endswith(".h5"):
        files.append(filename)

li = []
chunk = 100
output = np.ones([2400, 2400])
rad_m = np.ones([chunk,len(files),2400])
for r in np.arange(0,2400, chunk):
    print('CHUNK: %d' % (r))
    for f in np.arange(0,len(files)):
        print(files[f])
        hdf_file = gdal.Open(path+files[f])
        subDatasets = hdf_file.GetSubDatasets()
        

        rad = gdal.Open(subDatasets[4][0])
        lum = gdal.Open(subDatasets[9][0])
        cloud = gdal.Open(subDatasets[11][0])
        
        meta = rad.GetMetadata_Dict()
        
        east = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_EastBoundingCoord'])
        west = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_WestBoundingCoord'])
        north = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_NorthBoundingCoord'])
        south = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_SouthBoundingCoord'])
        date = meta['HDFEOS_GRIDS_VNP_Grid_DNB_RangeBeginningDate']
        
        vt = int(meta['VerticalTileNumber'])
        ht = int(meta['HorizontalTileNumber'])
        
        rad_band = rad.GetRasterBand(1)
        lum_band = lum.GetRasterBand(1)
        cloud_band = cloud.GetRasterBand(1)
        
        #meta = band.GetMetadata_Dict()
        
        rad_BandType = gdal.GetDataTypeName(rad_band.DataType)
        lum_BandType = gdal.GetDataTypeName(lum_band.DataType)
        cloud_BandType = gdal.GetDataTypeName(cloud_band.DataType)
        
        #cm = np.ones([band.YSize,band.XSize])
        
        #num_rejected = 0
        
        #for y in range(band.YSize): 
        
        y = r
        for c in np.arange(chunk):
            rad_scan = rad_band.ReadRaster(0,int(y + c),rad_band.XSize,1,rad_band.XSize,1,rad_band.DataType)
            lum_scan = lum_band.ReadRaster(0,int(y + c),lum_band.XSize,1,lum_band.XSize,1,rad_band.DataType)
            cloud_scan = cloud_band.ReadRaster(0,int(y + c),cloud_band.XSize,1,cloud_band.XSize,1,cloud_band.DataType)
            
            rad_values = struct.unpack(fmttypes[rad_BandType] * rad_band.XSize, rad_scan)
            lum_values = struct.unpack(fmttypes[lum_BandType] * lum_band.XSize, lum_scan)
            cloud_values = struct.unpack(fmttypes[cloud_BandType] * cloud_band.XSize, cloud_scan)
            #print(rad_values)
            for i in np.arange(len(rad_values)):
                cm = (cloud_values[i]  >> 5) & 3
                if lum_values[i] <= 2000 and cm < 2.5 and rad_values[i] < 5000:
                    rad_m[c][f][i] = rad_values[i]
                else:
                    rad_m[c][f][i] = np.nan
            #break
    for c in np.arange(chunk):
        output[r + c] = np.nanmean(rad_m[c], axis = 0)
        
    #break
    # for j in np.arange(2400):
    #     output[r][j] = rad[:,i]
    #break

driver = gdal.GetDriverByName("GTiff")
out = driver.Create('compiled_maxlim.tif', 2400, 2400, 1, gdal.GDT_Float32)
out.SetGeoTransform((west,10/2400,0,north,0,-10/2400))
rad.SetProjection("none")
#x=dataset.ReadAsArray()
out.GetRasterBand(1).WriteArray(output)
rad.FlushCache()
            
            # break
        
            # for i in np.arange(0,len(scanline),2):
            #     try:
            #         cm[y][int(i/2)]=bin(scanline[i])[-2:]
            #     except:
            #         cm[y][int(i/2)] = 0
            
            # for i in np.arange(len(values)):
            #     mask = (values[i] >> 5) & 3
            #     cm[y][i] = mask
            #     if mask >= 2:
            #         num_rejected += 1
                    
                
                    
                    
        
        
        # li.append([num_rejected, date])
        
        #break

# driver = gdal.GetDriverByName("GTiff")
# out = driver.Create('cc_test_dnb.tif', 2400, 2400, 1, gdal.GDT_Float32)
# out.SetGeoTransform((west,10/2400,0,north,0,-10/2400))
# dataset.SetProjection("none")
# x=dataset.ReadAsArray()
# out.GetRasterBand(1).WriteArray(x)
# dataset.FlushCache()


# df = pd.DataFrame(li, columns = ['rejected', 'date'])
# df['date'] = pd.to_datetime(df['date'])

# plt.rcParams.update({'font.size': 14})
# fig, ax = plt.subplots(1, 1, figsize=(12, 5))
# locator = mdates.AutoDateLocator(minticks=20, maxticks=40)
# formatter = mdates.ConciseDateFormatter(locator)
# ax.xaxis.set_major_locator(locator)
# ax.xaxis.set_major_formatter(formatter)
# plt.ylabel('% Pixels Rejected')


# ax.plot(df['date'],df['rejected']/(2400*2400)*100)
# #plt.plot([df['date'].min(),df['date'].max()],[20,20],'--r',label='filter threshold')
# ax.legend(loc = 1)
# ax.set_xlim([np.datetime64('2019-06'), np.datetime64('2019-12')])
# ax.set_title('Rejected Cloud Pixels')


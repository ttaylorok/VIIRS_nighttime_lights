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
for f in files:
    print(f)
    hdf_file = gdal.Open(path+f)
    subDatasets = hdf_file.GetSubDatasets()
    
    # 4 = dnb radiance
    # 9 = lunar illumination
    # 11 = cloud mask
    dataset = gdal.Open(subDatasets[11][0])
    meta = dataset.GetMetadata_Dict()
    
    east = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_EastBoundingCoord'])
    west = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_WestBoundingCoord'])
    north = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_NorthBoundingCoord'])
    south = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_SouthBoundingCoord'])
    date = meta['HDFEOS_GRIDS_VNP_Grid_DNB_RangeBeginningDate']
    
    vt = int(meta['VerticalTileNumber'])
    ht = int(meta['HorizontalTileNumber'])
    
    band = dataset.GetRasterBand(1)
    meta = band.GetMetadata_Dict()
    break
    
    '''
    00 : confident clear
    01 : probably clear
    10 : probably cloudy
    11 : confident cloudy
    '''
    
    # vals = dataset.ReadAsArray()
    # cm = vals
    # for i in np.arange(len(vals)):
    #     for j in np.arange(len(vals[i])):
    #         cm[i][j] = bin(vals[i][j])[8:10]
    
    
    
    BandType = gdal.GetDataTypeName(band.DataType)
    
    cm = np.ones([band.YSize,band.XSize])
    
    num_rejected = 0
    
    for y in range(band.YSize):    
        scanline = band.ReadRaster(0, 
                                    y, 
                                    band.XSize, 
                                    1, 
                                    band.XSize, 
                                    1, 
                                    band.DataType)
        values = struct.unpack(fmttypes[BandType] * band.XSize, scanline)
        # break
    
        # for i in np.arange(0,len(scanline),2):
        #     try:
        #         cm[y][int(i/2)]=bin(scanline[i])[-2:]
        #     except:
        #         cm[y][int(i/2)] = 0
        
        for i in np.arange(len(values)):
            mask = (values[i] >> 5) & 3
            cm[y][i] = mask
            if mask >= 2:
                num_rejected += 1
                
                
    
    
    li.append([num_rejected, date])
    
    #break

# driver = gdal.GetDriverByName("GTiff")
# out = driver.Create('cc_test_dnb.tif', 2400, 2400, 1, gdal.GDT_Float32)
# out.SetGeoTransform((west,10/2400,0,north,0,-10/2400))
# dataset.SetProjection("none")
# x=dataset.ReadAsArray()
# out.GetRasterBand(1).WriteArray(x)
# dataset.FlushCache()


df = pd.DataFrame(li, columns = ['rejected', 'date'])
df['date'] = pd.to_datetime(df['date'])

plt.rcParams.update({'font.size': 14})
fig, ax = plt.subplots(1, 1, figsize=(12, 5))
locator = mdates.AutoDateLocator(minticks=20, maxticks=40)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
plt.ylabel('% Pixels Rejected')


ax.plot(df['date'],df['rejected']/(2400*2400)*100)
#plt.plot([df['date'].min(),df['date'].max()],[20,20],'--r',label='filter threshold')
ax.legend(loc = 1)
ax.set_xlim([np.datetime64('2019-06'), np.datetime64('2019-12')])
ax.set_title('Rejected Cloud Pixels')


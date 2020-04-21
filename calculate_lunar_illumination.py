import gdal
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pylunar



path = 'DATA/VIIRS_south_america_v2/'
files = []
for filename in os.listdir(path):
    if filename.endswith(".h5") and 'h10v10' in filename:
        files.append(filename)
        
#files = ['VNP46A1.A2019167.h26v06.001.2019168094348.h5']

mi = pylunar.MoonInfo((-20,0,0), (-60,0,0))

li = []
for f in files:
    print(f)
    hdf_file = gdal.Open(path+f)
    subDatasets = hdf_file.GetSubDatasets()
    
    # 4 = dnb radiance
    # 9 = lunar illumination
    # 
    dataset = gdal.Open(subDatasets[9][0])
    meta = dataset.GetMetadata_Dict()
    
    east = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_EastBoundingCoord'])
    west = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_WestBoundingCoord'])
    north = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_NorthBoundingCoord'])
    south = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_SouthBoundingCoord'])
    date = meta['HDFEOS_GRIDS_VNP_Grid_DNB_RangeBeginningDate']
    
    vt = int(meta['VerticalTileNumber'])
    ht = int(meta['HorizontalTileNumber'])
    
    band = dataset.GetRasterBand(1)
    
    vals = dataset.ReadAsArray()
    
    year = int(f[9:13])
    days= int(f[13:16])
    date_calc = datetime.datetime(year, 1, 1) + datetime.timedelta(days - 1)
    mi.update(date_calc)
    li_calc = mi.fractional_phase()*100
    
    # if np.mean(vals) > 9800:
    #     break
    
    li.append([np.mean(vals), np.std(vals), date, li_calc])
    
# write to geo-tiff image
# driver = gdal.GetDriverByName("GTiff")
# out = driver.Create('full_moon_9800.tif', 2400, 2400, 1, gdal.GDT_Float32)
# out.SetGeoTransform((west,10/2400,0,north,0,-10/2400))
# dataset.SetProjection("none")
# x=dataset.ReadAsArray()
# out.GetRasterBand(1).WriteArray(x)
# dataset.FlushCache()


df = pd.DataFrame(li, columns = ['mean', 'std', 'date','li_calc'])
df['date'] = pd.to_datetime(df['date'])

plt.rcParams.update({'font.size': 14})
fig, ax = plt.subplots(1, 1, figsize=(12, 5))
locator = mdates.AutoDateLocator(minticks=20, maxticks=40)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
plt.ylabel('Lunar Illumination (%)')


ax.plot(df['date'],df['mean']*0.01)
plt.plot([df['date'].min(),df['date'].max()],[20,20],'--r',label='filter threshold')
ax.legend(loc = 1)
ax.set_xlim([df['date'].min(), df['date'].max()])
ax.set_title('Average Lunar Illumination by Date')

plt.plot(df['date'],df['li_calc'])
plt.show()


# lums = []
# for x in df['date']:
#     mi.update(x)
#     lums.append(mi.fractional_phase()*100)
    
# plt.plot(df['date'],lums)
# plt.show()

# import datetime
# year = int(f[9:13])
# days= int(f[13:16])
# date_calc = datetime.datetime(year, 1, 1) + datetime.timedelta(days - 1)

# pylunar.MoonInfo()


import gdal
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime


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
    
    li.append([np.mean(vals), np.std(vals), date])


df = pd.DataFrame(li, columns = ['mean', 'std', 'date'])
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
ax.set_xlim([np.datetime64('2019-06'), np.datetime64('2019-12')])
ax.set_title('Average Lunar Illumination by Date')

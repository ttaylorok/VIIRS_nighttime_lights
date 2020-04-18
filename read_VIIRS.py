import gdal
import struct
from osgeo import osr
import os
import pyproj

path = 'DATA/VIIRS/'
files = []
for filename in os.listdir(path):
    if filename.endswith(".h5"):
        files.append(filename)

for f in files:
    print(f)
    hdf_file = gdal.Open(path+f)
    subDatasets = hdf_file.GetSubDatasets()
    
    # open the DNB band
    dataset = gdal.Open(subDatasets[4][0])
    meta = dataset.GetMetadata_Dict()
    
    # extract geolocation information from meta-data
    east = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_EastBoundingCoord'])
    west = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_WestBoundingCoord'])
    north = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_NorthBoundingCoord'])
    south = int(meta['HDFEOS_GRIDS_VNP_Grid_DNB_SouthBoundingCoord'])
    
    vt = int(meta['VerticalTileNumber'])
    ht = int(meta['HorizontalTileNumber'])
    
    out_name = 'DATA/VIIRS_south_america_tif/H%d_V%d.tif' % (ht,vt)
    
    # write to geo-tiff image
    driver = gdal.GetDriverByName("GTiff")
    out = driver.Create(out_name, 2400, 2400, 1, gdal.GDT_Float32)
    out.SetGeoTransform((west,10/2400,0,north,0,-10/2400))
    dataset.SetProjection("none")
    x=dataset.ReadAsArray()
    out.GetRasterBand(1).WriteArray(x)
    dataset.FlushCache()
    

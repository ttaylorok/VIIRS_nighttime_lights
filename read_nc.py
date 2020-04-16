import xarray as xr

file = 'DATA/VIIRS_v2/VNP02DNB.A2020001.0242.001.2020001093116.nc'
DS = xr.open_dataset(file, group='observation_data')



data = DS.DNB_observations.values
DS.values

DS.dims
DS.sel()
d = DS.dims

for x in d.keys():
    print(x)
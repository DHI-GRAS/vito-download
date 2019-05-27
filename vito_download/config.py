import datetime

datapool_url = 'http://land.copernicus.vgt.vito.be/PDF/datapool/'

product_base_urls = {
    'Water_Bodies_Global': 'Water/Water_Bodies/Water_Bodies_Global_V2',
    'SWI': 'Vegetation/Soil_Water_Index/Daily_SWI_12.5km_Global_V3',
    'SWI10': 'Vegetation/Soil_Water_Index/10-daily_SWI_12.5km_Global_V3',
    'SSM': 'Vegetation/Surface_Soil_Moisture/BioPar_SSM1km_V1_Global'
}

timestep_days = {
    'Water_Bodies_Global': 10,
    'SWI': 1,
    'SWI10': 10,
    'SSM': 1
}

timeseries_startdate = {
    'Water_Bodies_Global': datetime.datetime(2014, 1, 1),
    'SWI': datetime.datetime(2007, 8, 1),
    'SWI10': datetime.datetime(2007, 8, 1),
    'SSM': datetime.datetime(2015, 1, 1)
}

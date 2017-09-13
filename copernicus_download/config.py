import datetime

datapool_url = 'http://land.copernicus.vgt.vito.be/PDF/////datapool/'

product_base_urls = {
        'Water_Bodies_Global': 'Water/Water_Bodies/Water_Bodies_Global_V2',
        'SWI': 'Vegetation/Soil_Water/SWI_V3',
        'SWI10': 'Vegetation/Soil_Water/SWI10_V3'}

timestep_days = {
        'Water_Bodies_Global': 10,
        'SWI': 1,
        'SWI10': 10}

timeseries_startdate = {
        'Water_Bodies_Global': datetime.datetime(2014, 1, 1),
        'SWI': datetime.datetime(2007, 8, 1),
        'SWI10': datetime.datetime(2007, 8, 1)}

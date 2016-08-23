import datetime

datapool_url = 'http://land.copernicus.vgt.vito.be/PDF/datapool/'

product_base_urls = {
        'SWI': 'Water/Soil_Water/SWI_V3',
        'SWI_10': 'Water/Soil_Water/SWI10_V3'}

timestep_days = {
        'SWI': 1,
        'SWI10': 10}

timeseries_startdate = {
        'SWI': datetime.datetime(2007, 8, 1),
        'SWI10': datetime.datetime(2007, 8, 1)}

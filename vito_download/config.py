import datetime

product_url = {
    'Water_Bodies_Global': 'http://land.copernicus.vgt.vito.be/PDF/datapool/Water/Water_Bodies/Water_Bodies_Global_V2',
    'SWI': 'http://land.copernicus.vgt.vito.be/PDF/datapool/Vegetation/Soil_Water_Index/Daily_SWI_12.5km_Global_V3',
    'SWI10': 'http://land.copernicus.vgt.vito.be/PDF/datapool/Vegetation/Soil_Water_Index/10-daily_SWI_12.5km_Global_V3',
    'SSM': 'http://land.copernicus.vgt.vito.be/PDF/datapool/Vegetation/Surface_Soil_Moisture/BioPar_SSM1km_V1_Global',
    'Proba-V-NDVI': 'https://www.vito-eodata.be/PDF/datapool/Free_Data/PROBA-V_100m/S1_TOC_NDVI_100_m__C1',
    'Proba-V': 'https://www.vito-eodata.be/PDF/datapool/Free_Data/PROBA-V_100m/S1_TOC_100_m_C1'
}

timestep_days = {
    'Water_Bodies_Global': 10,
    'SWI': 1,
    'SWI10': 10,
    'SSM': 1,
    'Proba-V-NDVI': 1,
    'Proba-V': 1
}

timeseries_startdate = {
    'Water_Bodies_Global': datetime.datetime(2014, 1, 1),
    'SWI': datetime.datetime(2007, 8, 1),
    'SWI10': datetime.datetime(2007, 8, 1),
    'SSM': datetime.datetime(2015, 1, 1),
    'Proba-V-NDVI': datetime.datetime(2014, 3, 12),
    'Proba-V': datetime.datetime(2014, 3, 12)
}

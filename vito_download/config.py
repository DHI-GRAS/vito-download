import datetime

product_url = {
    'Water_Bodies_Global': 'https://land.copernicus.vgt.vito.be/PDF/datapool/Water/Water_Bodies/Water_Bodies_1km_Global_V2',
    'SWI': 'http://land.copernicus.vgt.vito.be/PDF/datapool/Vegetation/Soil_Water_Index/Daily_SWI_12.5km_Global_V3',
    'SWI10': 'http://land.copernicus.vgt.vito.be/PDF/datapool/Vegetation/Soil_Water_Index/10-daily_SWI_12.5km_Global_V3',
    'SSM': 'http://land.copernicus.vgt.vito.be/PDF/datapool/Vegetation/Surface_Soil_Moisture/BioPar_SSM1km_V1_Global',
    'Proba-V-S1-TOC': 'http://www.vito-eodata.be/PDF/datapool/Free_Data/PROBA-V_100m/S1_TOC_100_m_C1',
    'Proba-V-S1-TOC-NDVI': 'http://www.vito-eodata.be/PDF/datapool/Free_Data/PROBA-V_100m/S1_TOC_NDVI_100_m__C1',
    'Proba-V-S5-TOC': 'http://www.vito-eodata.be/PDF/datapool/Free_Data/PROBA-V_100m/S5_TOC_100_m_C1',
    'Proba-V-S5-TOC-NDVI': 'http://www.vito-eodata.be/PDF/datapool/Free_Data/PROBA-V_100m/S5_TOC_NDVI_100_m_C1'
}

timestep_days = {
    'Water_Bodies_Global': 10,
    'SWI': 1,
    'SWI10': 10,
    'SSM': 1,
    'Proba-V-S1-TOC-NDVI': 1,
    'Proba-V-S1-TOC': 1,
    'Proba-V-S5-TOC-NDVI': 5,
    'Proba-V-S5-TOC': 5
}

timeseries_startdate = {
    'Water_Bodies_Global': datetime.datetime(2014, 1, 1),
    'SWI': datetime.datetime(2007, 8, 1),
    'SWI10': datetime.datetime(2007, 8, 1),
    'SSM': datetime.datetime(2015, 1, 1),
    'Proba-V-S1-TOC-NDVI': datetime.datetime(2014, 3, 11),
    'Proba-V-S1-TOC': datetime.datetime(2014, 3, 11),
    'Proba-V-S5-TOC-NDVI': datetime.datetime(2014, 3, 11),
    'Proba-V-S5-TOC': datetime.datetime(2014, 3, 11)
}

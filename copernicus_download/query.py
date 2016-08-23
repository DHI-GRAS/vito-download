import posixpath


datapool_url = 'http://land.copernicus.vgt.vito.be/PDF///datapool/'

product_base_urls = {
        'SWI': 'Water/Soil_Water/SWI_V3',
        'SWI_10': 'Water/Soil_Water/SWI10_V3',
                    }


def get_product_url(product):
    return posixpath.join(datapool_url, product_base_urls[product])


def build_url(product, year, month=None, day=None, extent={}):
    url = get_product_url(product)

    url += '/{}'.format(year)

    if month:
        url += '/{:02d}'.format(month)
        if day:
            url += '/{:02d}'.format(day)

    if extent:
        url += '/?coord{xmin},{ymin},{xmax},{ymax}'.format(**extent)

    return url

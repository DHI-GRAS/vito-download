import posixpath

from vito_download.config import product_url


def get_product_url(product):
    return product_url[product]


def build_url(product, year, month=None, day=None, extent={}):
    url = get_product_url(product)

    url += '/{}'.format(year)

    if month:
        url += '/{}'.format(month)
        if day:
            url += '/{}'.format(day)

    if extent:
        url += '/?coord={xmin},{ymin},{xmax},{ymax}'.format(**extent)

    return url

import posixpath

from .config import datapool_url, product_base_urls

def get_product_url(product):
    return posixpath.join(datapool_url, product_base_urls[product])


def build_url(product, year, month=None, day=None, extent={}):
    url = get_product_url(product)

    url += '/{}'.format(year)

    if month:
        url += '/{}'.format(month)
        if day:
            url += '/{}'.format(day)

    if extent:
        url += '/?coord{xmin},{ymin},{xmax},{ymax}'.format(**extent)

    return url

import datetime
import logging

from vito_download.query import build_url
from vito_download.download import download_data
from vito_download.config import timeseries_startdate, timestep_days

logger = logging.getLogger('copernicus_download.convenience')


def download_date_range(
        product, username, password, download_dir,
        startdate=None, enddate=None, extent={}):
    """Download date range of product from Copernicus

    Parameters
    ----------
    product : str
        product name (see config)
    username, password : str, str
        authentication
    download_dir : str
        download directory
    startdate, enddate : datetime.datetime, optional
        start and end date to download
        if None, the first in series, respectively today will be used
    extent : dict
        extent to include in query
    """
    if startdate is None:
        startdate = timeseries_startdate[product]

    if enddate is None:
        enddate = datetime.datetime.now()

    dt = datetime.timedelta(days=timestep_days[product])

    downloaded_files = []
    date = startdate
    while date <= enddate:
        url = build_url(
                product=product,
                year=date.year, month=date.month, day=date.day, extent=extent)
        logging.debug('Query URL is \'{}\'.'.format(url))
        files = download_data(url, username, password, download_dir=download_dir)
        downloaded_files += files

        date += dt

    return downloaded_files

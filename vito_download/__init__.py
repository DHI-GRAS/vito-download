from vito_download.query import build_url
from vito_download.download import download_data
from vito_download.convenience import download_date_range
from vito_download import config
from vito_download.extract import extract_h5
from vito_download.read import read_h5

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

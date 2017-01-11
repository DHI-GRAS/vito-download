from .query import build_url

from .download import download_data

from .convenience import download_date_range

from . import config

from .extract import extract_h5

try:
    from .read import read_h5
except ImportError:
    pass

import tempfile
import logging

from wget_provider import download_url

logger = logging.getLogger('copernicus_download.download')
download_url.logger = logger

def download_data(url, username, password, download_dir='.', data_ext='.ZIP'):
    """Download a url with login using wget"""
    download_subdir = tempfile.mkdtemp(prefix='download_', dir=download_dir)
    downloaded_files = download_url(url,
            auth=dict(username=username, password=password),
            continue_partial=True,
            recursive=True,
            cmd_extra=['--ignore-case'],
            data_ext=data_ext,
            download_dir=download_subdir)
    return downloaded_files

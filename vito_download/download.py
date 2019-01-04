import os
import time
import logging
import shutil
import fnmatch
import warnings
import concurrent.futures

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

import requests

import itsybitsy

logger = logging.getLogger(__name__)


def _download_file(url, target, session, max_retries=3, skip_existing=True):
    """Download a single file"""
    if skip_existing and os.path.isfile(target):
        logger.debug('>>> using existing file %s', target)
        return target
    target_temp = target + '.incomplete'
    response = None
    success = False
    for n in range(max_retries):
        with session.get(url, stream=True) as response:
            with open(target_temp, "wb") as target_file:
                shutil.copyfileobj(response.raw, target_file)
            data_length = response.raw.tell()
            if not data_length:
                logger.debug('Waiting 2 seconds before retry')
                time.sleep(2)
                continue
            else:
                success = True
                break
    if response is not None:
        response.raise_for_status()
    if not success:
        raise RuntimeError('Downloading {} failed after {} attempts.'.format(url, n+1))
    shutil.move(target_temp, target)
    return target


def _recursive_download(base_url, download_directory=".", username=None, password=None,
                        include=None, exclude=None, skip_existing=True,
                        download_jobs=10, download_retries=3, crawler_args=None):
    """Concurrent recursive downloader using the itsybitsy crawler

    Arguments
    ---------
    base_url : str
        Starting point for crawler
    download_directory : str
        Directory to save files to (default: current directory)
    username : str
        Username required for authentication (default: no authentication)
    password : str
        Password required for authentication (default: no authentication)
    include : list of str or str
        Download only files matching at least one of those glob patterns
        (default: download all files)
    exclude : list of str or str
        Do not download files matching at least one of those glob patterns
        (default: download all files)
    skip_existing : bool
        skip existing files
    download_jobs : int
        Number of concurrent jobs used for downloading files
    download_retries : int
        Number of retries
    crawler_args : dict
        Keyword arguments to pass to itsybitsy.crawl
    """
    logger.debug("crawling %s", base_url)

    if crawler_args is None:
        crawler_args = {}

    if username and password:
        crawler_args["auth"] = (username, password)

    crawler = itsybitsy.crawl(base_url, **crawler_args)
    base_url_normalized = next(crawler)
    base_path = urlparse.urlparse(base_url_normalized).path

    if isinstance(include, str):
        include = [include]
    if isinstance(exclude, str):
        exclude = [exclude]

    with requests.Session() as session:
        session.auth = (username, password)
        futures = set()
        with concurrent.futures.ThreadPoolExecutor(max_workers=download_jobs) as executor:
            for url in crawler:
                logger.debug("> found link: %s" % url)
                url_parts = urlparse.urlparse(url)
                file_path = url_parts.path
                if not file_path.startswith(base_path):
                    warnings.warn(
                            "File {} does not match base path {} - skipping"
                            .format(file_path, base_path))
                    continue

                target_localpath = os.path.normpath(file_path[len(base_path):])
                target_fname = os.path.basename(target_localpath)
                target_fullpath = os.path.join(download_directory, target_fname)

                if (
                        include and not
                        any(fnmatch.fnmatch(target_localpath, pattern) for pattern in include)):
                    logger.debug(">> skipping due to include pattern")
                    continue
                if (
                        exclude and
                        any(fnmatch.fnmatch(target_localpath, pattern) for pattern in exclude)):
                    logger.debug(">> skipping due to exclude pattern")
                    continue

                logger.debug(">> downloading")
                args = (url, target_fullpath, session, download_retries, skip_existing)
                future = executor.submit(_download_file, *args)
                futures.add(future)

            if futures:
                for future in concurrent.futures.as_completed(futures):
                    yield future.result()


def download_data(url, username, password, download_dir='.',
                  include='*.zip', skip_existing=True, download_jobs=10):
    """Download a URL tree recursively using itsybitsy

    Parameters
    ----------
    url : str
        Starting point for crawler
    username : str
        Username for authentication
    password  : str
        Password for authentication
    download_dir : str
        Directory to save downloaded files to (default: current directory)
    include : list of str or str
        Download only files matching at least one of those glob patterns
        (default: all .zip files)
    skip_existing : bool
        skip existing files
    download_jobs : int
        number of parallel downloads (threads)

    Returns
    -------
    generator of str
        yields paths to downloaded files
    """
    crawler_args = dict(  # passed to itsybitsy
        only_go_deeper=True,
        max_depth=None,
        max_retries=10,
        timeout=100,
        strip_fragments=True,
        max_connections=100)
    return _recursive_download(
        url,
        download_directory=download_dir,
        username=username,
        password=password,
        include=include,
        skip_existing=skip_existing,
        crawler_args=crawler_args,
        download_jobs=download_jobs
    )

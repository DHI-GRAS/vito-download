import tempfile
import logging
import os.path
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


def _download_file(url, target, session, max_retries=10):
    """Download a single file"""
    retries = 0
    while True:
        if retries >= max_retries:
            logger.warning("could not get file %s", url)
            break
        with session.get(url, stream=True) as response:
            with open(target, "wb") as target_file:
                shutil.copyfileobj(response.raw, target_file)
            data_length = response.raw.tell()
            if not data_length:
                retries += 1
                continue
            break
    return target


def _recursive_download(base_url, download_directory=".", username=None, password=None,
                        include=None, exclude=None, download_jobs=10, crawler_args=None):
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
    download_jobs : int
        Number of concurrent jobs used for downloading files (default: 10)
    crawler_args : dict
        Keyword arguments to pass to itsybitsy.crawl
    """
    logger.debug("crawling %s", base_url)

    if crawler_args is None:
        crawler_args = {}

    with requests.Session() as session:
        if username and password:
            session.auth = (username, password)

        if crawler_args.get("session") is None:
            crawler_args["session"] = session

        crawler = itsybitsy.crawl(base_url, **crawler_args)
        base_url_normalized = next(crawler)
        base_path = urlparse.urlparse(base_url_normalized).path

        if isinstance(include, str):
            include = [include]
        if isinstance(exclude, str):
            exclude = [exclude]

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
                target_fullpath = os.path.join(download_directory, target_localpath)

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

                try:
                    os.makedirs(os.path.dirname(target_fullpath))
                except OSError:
                    pass

                logger.debug(">> downloading")
                future = executor.submit(_download_file, url, target_fullpath, session)
                futures.add(future)

            if futures:
                for future in concurrent.futures.as_completed(futures):
                    yield future.result()


def download_data(url, username, password, download_dir='.', include='*.zip'):
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
    """

    crawler_args = dict(  # passed to itsybitsy
        only_go_deeper=True,
        max_depth=None,
        max_retries=10,
        timeout=100,
        strip_fragments=True,
        max_connections=100
    )

    download_subdir = tempfile.mkdtemp(prefix='download_', dir=download_dir)
    return _recursive_download(url,
                               download_directory=download_subdir,
                               username=username,
                               password=password,
                               include=include,
                               crawler_args=crawler_args)

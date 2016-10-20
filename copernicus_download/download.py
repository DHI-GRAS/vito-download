import os
import glob
import tempfile
import subprocess
import re
import logging

wget_exe = os.path.join(os.path.dirname(__file__), 'wget64.exe')
wget_exe = '"{}"'.format(wget_exe)

def download_data(url, username, password, download_dir='.', data_ext='.ZIP',
        logger=None):
    """Download a url with login using wget"""

    if logger is None:
        logger = logging.getLogger('copernicus_download')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    download_subdir = tempfile.mkdtemp(prefix='download_', dir=download_dir)

    # put together command
    cmd = [wget_exe]
    cmd += ['--user='+username, '--password='+password]
    cmd += ['--recursive']
    cmd += ['--ignore-case', '--accept="*{}"'.format(data_ext)]
    cmd += ['--continue']
    cmd += ['--no-directories', '--directory-prefix=\"{}\"'.format(download_subdir)]
    cmd += [url]

    # join cmd to string to preserve the glob pattern!
    cmd = ' '.join(cmd)

    logger.debug('Download command is \'{}\'.'.format(cmd))

    # on windows, suppress wget window
    startupinfo = None
    if os.name == 'nt':
        pass
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # execute command
    proc = subprocess.Popen(cmd,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE,
            startupinfo=startupinfo)
    n = 0
    last_percent = ''
    for line in iter(proc.stdout.readline, ''):
        n += 1
        if n <= 10:
            # print the first 10 lines
            logger.info(line.rstrip())
        elif '%' in line:
            # get and log status
            try:
                percent = re.search('(\d{1,3}\%)', line).group(0)
                if percent != last_percent:
                    logger.info(percent)
                    last_percent = percent
            except IndexError:
                pass
        if 'ERROR' in line:
            # fail on errors
            raise RuntimeError('Download of {} failed: {}'.format(url, line.rstrip()))

    pattern = os.path.join(download_subdir, '*'+data_ext)
    downloaded_files = sorted(glob.glob(pattern))
    return downloaded_files

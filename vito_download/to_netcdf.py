import tempfile
import shutil
import netCDF4

from .extract import extract_h5


def get_netcdf(zipfname, product, tempdir=None):
    """Get netCDF from zip archive"""

    raise NotImplementedError('This is a stub.')

    tempdir_zip = tempdir or tempfile.mkdtemp()

    try:
        h5fname = extract_h5(zipfname, outdir=tempdir)
    finally:
        if tempdir is None:
            shutil.rmtree(tempdir_zip)

    with netCDF4.Dataset(h5fname) as ds:
        pass

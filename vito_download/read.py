import os
import re
import datetime

import numpy as np

import netCDF4
import xarray as xr


def get_lon_lat(ds, datashape, gridkw=None):
    """Create lon and lat axes for datashape and ds

    Parameters
    ----------
    ds : open hdf dataset
        hdf input dataset
    datashape : tuple (nlat, nlon)
        data shape
    gridkw : dict
        grid specifications to override dataset info
    """
    if gridkw is None:
        gridkw = {}
    nlat, nlon = datashape

    lon0 = gridkw.get('lon0', ds.LONG)
    lat0 = gridkw.get('lat0', ds.LAT)

    try:
        res_deg = gridkw['res_deg']
    except KeyError:
        pix_str = ds.Pixel_size
        try:
            res_deg = float(re.match('(\d\.?\d?) (degree)(s?)', pix_str).group(1))
        except AttributeError:
            raise ValueError('Unable to determine resolution from \'{}\'.'.format(pix_str))

    # if latitude axis would exceed 90 degrees, use reverse
    if np.abs(lat0 + res_deg * (nlat-1)) > 90:
        lat0 = -lat0

    lon = np.arange(0, nlon) * res_deg + lon0
    lat = np.arange(0, nlat) * res_deg + lat0

    return lon, lat


def date_from_h5fname(fname):
    # g2_BIOPAR_SWI_201505020000_GLOBE_ASCAT_V3.0.1.h5
    try:
        datestr = re.findall('\d{8}', os.path.basename(fname))[0]
    except IndexError:
        raise ValueError('Unable to get date from file name \'{}\'.'.format(fname))
    return datetime.datetime.strptime(datestr, '%Y%m%d')


def read_h5(h5fname, group, varn, gridkw=None):
    """Get data from a Copernicus HDF5 file

    Parameters
    ----------
    h5fname : str
        path to HDF5 file
    group, varn : str
        group and variable in HDF file
    outfname : str
        path to output file to be created
    gridkw : dict, optional
        grid definition res_deg, lon0, lat0
        will be retrieved from HDF file if not provided

    Returns
    -------
    xarray.Dataset
    """
    if gridkw is None:
        gridkw = {}
    with netCDF4.Dataset(h5fname) as dsin:
        datavar = dsin.groups[group].variables[varn]

        # NB: the Product_time attribute is not reliable!
        # date = datetime.datetime.strptime(dsin.Product_time[:8], '%Y%m%d')
        date = date_from_h5fname(h5fname)

        # get grid
        lon, lat = get_lon_lat(dsin, datavar.shape, gridkw)
        gridshape = (len(lat), len(lon))
        if gridshape != datavar.shape:
            raise ValueError(
                    'Derived grid has different shape {} '
                    'than data {}.'.format(gridshape, datavar.shape))

        # get data (working format: f4)
        data = np.flipud(datavar[:])
        data = np.ma.masked_equal(data, datavar.Missing_value, copy=False).astype('f4')
        data -= datavar.Offset
        data *= datavar.Scaling_factor

        # get attributes
        attrs = dict(
                units=datavar.Units,
                long_name=datavar.Product)
        global_attrs = {k: dsin.getncattr(k) for k in dsin.ncattrs()}

    da = xr.DataArray(
            data[np.newaxis, ...],
            coords=dict(lon=lon, lat=lat, time=[date]),
            dims=['time', 'lat', 'lon'],
            name=varn,
            attrs=attrs)
    ds = da.to_dataset()
    ds.attrs.update(global_attrs)

    return ds

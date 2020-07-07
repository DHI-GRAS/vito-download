# vito_download
Download from the vito datapool websites http://land.copernicus.vgt.vito.be/PDF/datapool and https://www.vito-eodata.be/PDF/datapool/

## Installation

You need to have [`itsybitsy`](https://github.com/DHI-GRAS/itsybitsy) installed. Then run

    python setup.py install

To use the `read_h5` module, you also need `xarray` and `netCDF4`.


## Usage

```
import vito_download as vito
import xarray as xr

url = vito.build_url(product='SWI', year=2016, month=1, day=1)

local_files = vito.download_data(url, username='USERNAME', password='PASSWORD',
                                 download_dir='.', include='*.nc')

dataset = xr.open_dataset(list(local_files)[0])

data = dataset['SWI_010'].values.squeeze()
```

## Extent

The new downloader adds the `?coord` parameter to download URLs by default, when `build_url` is called with an `extent` dictionary ([here](https://github.com/DHI-GRAS/vito_download/blob/master/vito_download/query.py#L20)). However, coord only works for some products (e.g. not SWI), so manual cropping after the download is needed.

From the manual:

> If you want to download only a specific region, the coord parameter (in LonLat) can be added to the
> URL. The structure of this URL part is
> ?coord=XLL,YLL,XUR,YUR
> where (XLL,YLL) is the LonLat coordinates of the lower-left corner of the boundingBox and (XUR,YUR)
> is the LonLat coordinates of the upper-right corner. E.g. ?coord=-10.1,-5.1,10.0,5.0
> Note: the coord parameter is only supported for PROBA-V synthesis products.

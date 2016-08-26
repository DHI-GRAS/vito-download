# copernicus_download
Download http://land.copernicus.vgt.vito.be/PDF/datapool

## Usage

```
import copernicus_download as codo
url = codo.build_url(product='SWI', year=2016, month=1)
local_files = codo.download_data(url, username='user', password='pass', 
                                 download_dir='.', data_ext='.ZIP')
```

## Extent

The new downloader adds the `?coord` parameter to download URLs by default, when `build_url` is called with an `extent` dictionary ([here](https://github.com/DHI-GRAS/copernicus_download/blob/master/copernicus_download/query.py#L20)). However, coord only works for some products (e.g. not SWI), so manual cropping after the download is needed.

From the manual:

> If you want to download only a specific region, the coord parameter (in LonLat) can be added to the
> URL. The structure of this URL part is
> ?coord=XLL,YLL,XUR,YUR
> where (XLL,YLL) is the LonLat coordinates of the lower-left corner of the boundingBox and (XUR,YUR)
> is the LonLat coordinates of the upper-right corner. E.g. ?coord=-10.1,-5.1,10.0,5.0
> Note: the coord parameter is only supported for PROBA-V synthesis products. 

import unittest
import tempfile
import shutil

import copernicus_download as codo

class TestDownload(unittest.TestCase):

    def test_download(self):
        url = codo.build_url(product='SWI', year=2010, month=6, day=15)
        print(url)

        download_dir = tempfile.mkdtemp()
        print(download_dir)
        try:
            downloaded_files = codo.download_data(url,
                    username='floodanddrought', password='drought2015',
                    download_dir=download_dir)
            print(downloaded_files)
            self.assertTrue(bool(downloaded_files))
        finally:
            shutil.rmtree(download_dir)

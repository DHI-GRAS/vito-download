from setuptools import setup, find_packages

setup(
    name='copernicus_download',
    version='0.3.0',
    description='Download from land.copernicus.vgt.vito.be/PDF/datapool',
    author='Jonas Solvsteen',
    author_email='josl@dhigroup.com',
    url='https://www.dhi-gras.com',
    packages=find_packages(),
    install_requires=[
            'itsybitsy'
        ],
    )

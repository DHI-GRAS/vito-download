from setuptools import setup, find_packages

setup(
    name='vito_download',
    version='2.0',
    description='Download from land.copernicus.vgt.vito.be/PDF/datapool',
    author='Jonas Solvsteen',
    author_email='josl@dhigroup.com',
    url='https://www.dhigroup.com',
    packages=find_packages(),
    install_requires=[
            'itsybitsy'
        ],
    )

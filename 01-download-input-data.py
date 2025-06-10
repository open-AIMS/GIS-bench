from data_downloader import DataDownloader
from pyproj import CRS
import os
import sys


# Create an instance of the DataDownloader class
downloader = DataDownloader(download_path="data")

print("Downloading source data files. This will take a while ...")

# --------------------------------------------------------
# Keppel Island Habitat map data
direct_download_url = 'https://nextcloud.eatlas.org.au/s/8yzFHQkLxXBLM2G/download?path=%2Fdata%2Fhabitat%2F&files=habitat-raw'
downloader.download_and_unzip(direct_download_url, 'habitat', flatten_directory=True)


# These are for later development of the shallow mapping test

# --------------------------------------------------------
# Australian Coastline 50K 2024 (NESP MaC 3.17, AIMS)
# https://eatlas.org.au/geonetwork/srv/eng/catalog.search#/metadata/c5438e91-20bf-4253-a006-9e9600981c5f
# Hammerton, M., & Lawrey, E. (2024). Australian Coastline 50K 2024 (NESP MaC 3.17, AIMS) (2nd Ed.) [Data set]. eAtlas. https://doi.org/10.26274/qfy8-hj59
#direct_download_url = 'https://nextcloud.eatlas.org.au/s/DcGmpS3F5KZjgAG/download?path=%2FV1-1%2F&files=Split'
#downloader.download_and_unzip(direct_download_url, 'AU_AIMS_Coastline_50k_2024', subfolder_name='Split', flatten_directory=True)



#downloader.download_path = "in-data"
# --------------------------------------------------------
# The rough reef mask corresponds to the water estimate
# masking created for the creation of this dataset

#direct_download_url = f'https://nextcloud.eatlas.org.au/s/iMrFB9WP9EpLPC2/download?path=%2FV1-1%2Fin-data%2FAU_Rough-reef-shallow-mask'
#downloader.download_and_unzip(direct_download_url, 'AU_Rough-reef-shallow-mask', flatten_directory=True)





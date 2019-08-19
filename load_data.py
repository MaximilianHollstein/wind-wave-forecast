import bz2
import os
import time
import urllib

import requests


########################################################################

# This module contains functions that allow one to download and access
# the most recent WAM data provided by the DWD (https://www.dwd.de/,
# https://opendata.dwd.de).

########################################################################

# This function downloads the most recent data concerning a specific
# parameter 'parameter' to the directory 'localDataDirectory'.


def load_latest_wam_data(local_data_directory, parameter, limit=-1):
    # create directory to which the data is downloaded
    if not os.path.exists(local_data_directory):
        os.makedirs(local_data_directory)

    # construct the directory from which the data is downloaded
    data_directory = 'https://opendata.dwd.de/weather/maritime/wave_models/' \
                     + 'cwam/grib/00/' + parameter.lower() + '/'

    # get available files
    success = 0
    list_of_files = []
    while success == 0:
        try:
            r = requests.get(data_directory)
            for l in r.text.split('\n'):
                a = l.split('\"')
                if len(a) == 3:
                    if '.grib2.bz2' in a[1]:
                        list_of_files.append(str(a[1]))
                    if limit > -1:
                        list_of_files = list_of_files[0:limit]
            success = 1

        except Exception, e:
            print e
            print('wait 5 minutes...')
            time.sleep(300)  # wait 300 seconds

    # download files
    while len(list_of_files) > 0:
        # get file
        local_file = local_data_directory + '/' + list_of_files[-1]
        try:
            urllib.urlretrieve(os.path.join(data_directory, list_of_files[-1]),
                               local_file)
        except Exception, e:
            print e

        if os.path.isfile(local_file):
            list_of_files = [list_of_files[i] for i \
                             in range(len(list_of_files) - 1)]
        else:
            print('wait 5 minutes...')
            time.sleep(300)


# This function decompresses the files in the directory
# 'localDataDirectory'.

def decompress_data(local_data_directory):
    # create directory in which the data files will be stored
    local_data_directory_unzipped = local_data_directory + '/unzipped_data'
    if not os.path.exists(local_data_directory_unzipped):
        os.makedirs(local_data_directory_unzipped)

    # decompress files
    local_files = [f for f in os.listdir(local_data_directory)
                   if os.path.isfile(os.path.join(local_data_directory, f))
                   and f[0] != '.']

    for f in local_files:
        fi = open(local_data_directory + '/' + f, 'rb').read()
        uncompressed_f = bz2.decompress(fi)

        # save decompressed file
        file = open(local_data_directory_unzipped + '/'
                    + f.split('.')[-3] + '.grib2', 'wb')
        file.write(uncompressed_f)
        file.close()

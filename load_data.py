import bz2
import os
import time
import urllib
import urllib.request
import requests


########################################################################

# This module contains functions that are desigend to specifically  download and access
# (WAM) data provided by the DWD (https://www.dwd.de/, https://opendata.dwd.de).

########################################################################

# function for downloading data from remote directory
def load_data(remote_data_directory, local_data_directory, filename_extension, \
    limit=-1, number_of_request_trials=5,verbose=True):

    # create directory in which the downloaded data will be stored
    if not os.path.exists(local_data_directory):
        os.makedirs(local_data_directory)


    # get available files
    number_of_request_trials = 0
    success = 0
    list_of_files = []
    while success == 0:
        number_of_request_trials = number_of_request_trials + 1
        try:
            r = requests.get(remote_data_directory)
            for l in r.text.split('\n'):
                a = l.split('\"')
                if len(a) == 3:
                    if filename_extension in a[1]:
                        list_of_files.append(str(a[1]))
                    if limit > -1:
                        list_of_files = list_of_files[0:limit]
            success = 1
        except Exception as e:
            print(e)

            if number_of_request_trials <= number_of_request_trials:

                # if the server is not responsive, retry request in 5 minutes
                print('wait 5 minutes...')
                time.sleep(300)  
            else:
                print('')
                success = -1

    if success > 0:

        # download available files
        while len(list_of_files) > 0:
            # get file
            local_file = local_data_directory + '/' + list_of_files[-1]
            try:
                if verbose:
                    print("try to download:")
                    print(os.path.join(remote_data_directory, list_of_files[-1]))
                    print("")

                urllib.request.urlretrieve(os.path.join(remote_data_directory, \
                    list_of_files[-1]),local_file)
            except Exception as e:
                print(e)

            if os.path.isfile(local_file):
                 list_of_files = [list_of_files[i] for i \
                             in range(len(list_of_files) - 1)]
            else:
                print('wait 5 minutes...')
                time.sleep(300)

# This function decompresses  files in a specified directory
# 'localDataDirectory'.

def decompress_data(local_data_directory,target_directory):
    # create directory in which the data files will be stored
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # decompress files
    local_files = [f for f in os.listdir(local_data_directory)
                   if os.path.isfile(os.path.join(local_data_directory, f))
                   and f[0] != '.']

    for f in local_files:
        fi = open(local_data_directory + '/' + f, 'rb').read()
        uncompressed_f = bz2.decompress(fi)

        # save decompressed file
        file = open(target_directory + '/'
                    + f.split('.')[-3] + '.grib2', 'wb')
        file.write(uncompressed_f)
        file.close()

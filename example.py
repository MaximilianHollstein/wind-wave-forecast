import data_extraction
import serialization
import load_data
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import os


# create directory to which the swh data will be downloaded to
local_data_directory_swh ='/Volumes/UNTITLED/Data_Test/swh'
local_data_directory_swh_decompressed = os.path.join(local_data_directory_swh,
                                                     'decompressed')

if not os.path.exists(local_data_directory_swh):
    os.makedirs(local_data_directory_swh)

# get significant wave height data (swh)
remote_data_directory = \
    'https://opendata.dwd.de/weather/maritime/wave_models/ewam/grib/00/swh/'
file_extension = 'grib2.bz2'

# load_data.load_data(remote_data_directory,
#                     local_data_directory_swh,
#                     file_extension,
#                     verbose=True)
#
# load_data.decompress_data(local_data_directory_swh,
#                           os.path.join(local_data_directory_swh,
#                                        'decompressed'))

# create directory to which the swell direction data (dd_10m)
#  will be downloaded to
local_data_directory_dd_10m ='/Volumes/UNTITLED/Data_Test/dd_10m'
local_data_directory_dd_10m_decompressed = os.path.join(
    local_data_directory_dd_10m,'decompressed')

if not os.path.exists(local_data_directory_dd_10m):
    os.makedirs(local_data_directory_dd_10m)

# get swell direction data (dd_10m)
remote_data_directory = \
    'https://opendata.dwd.de/weather/maritime/wave_models/ewam/grib/00/dd_10m/'
file_extension = 'grib2.bz2'

# load_data.load_data(remote_data_directory,
#                     local_data_directory_dd_10m,
#                     file_extension,
#                     verbose=True)
#
# load_data.decompress_data(local_data_directory_dd_10m,
#                           os.path.join(local_data_directory_dd_10m,
#                                        'decompressed'))

# extract data and visualize combined swh + dd_10m data
for f_swh in os.listdir(local_data_directory_swh_decompressed):
        if f_swh[0] != '.':
            #try:
                file_name_swh = local_data_directory_swh_decompressed + "/" \
                                + f_swh

                time_swh, forecast_reference_time_swh, numeric_data_swh, \
                spatial_grid_swh = \
                    data_extraction.extract_forecast_data(file_name_swh)

                for f_dd_10m in \
                        os.listdir(local_data_directory_dd_10m_decompressed):

                    if f_swh.split('_SWH_')[1] == f_dd_10m.split('_DD_10M_')[1]:
                        file_name_dd_10m = \
                            local_data_directory_dd_10m_decompressed + "/" \
                            + f_dd_10m

                        time_dd_10m, forecast_reference_time_dd_10m, \
                        numeric_data_dd_10m, spatial_grid_dd_10m = \
                            data_extraction.extract_forecast_data(
                                file_name_dd_10m)

                        # plot data
                        maximum_value = np.max(numeric_data_swh)
                        plt.figure()
                        plt.imshow(numeric_data_swh/maximum_value)

                        step = 15
                        range_x = numeric_data_dd_10m.shape[1]
                        range_y = numeric_data_dd_10m.shape[0]

                        x = range(0, range_x, step)
                        y = range(0, range_y, step)
                        Xf, Yf = np.meshgrid(x, y)


                        U = step* np.multiply(numeric_data_swh[0:range_y:step,
                                         0:range_x:step],
                                              np.cos((2 * np.pi / 360.0)
                                                     * numeric_data_dd_10m[
                                                       0:range_y:step,
                                                       0:range_x:step])) \
                            /maximum_value

                        V = step*(np.multiply(numeric_data_swh[0:range_y:step,
                                              0:range_x:step],
                                              np.sin((2 * np.pi / 360.0)
                                                     * numeric_data_dd_10m[
                                                       0:range_y:step,
                                                       0:range_x:step]))) \
                             / maximum_value
                        plt.quiver(Xf, Yf, U, V, scale=1, units='xy')
                        plt.show()







            #except:
            #    print(f_swh)
            #    print("Could not process swh and corresponding dd_10m data "
            #          "files. Try next another pair of files.")




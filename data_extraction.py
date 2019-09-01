import iris
import numpy as np
import pandas as pd

def extract_forecast_data(file_name):
        cubes = iris.load(file_name)
        numeric_data = cubes[0].core_data()
        forecast_reference_time = cubes[0].coord('forecast_reference_time').core_points()
        time = int(cubes[0].coord('time').core_points()[0])
        latitude = cubes[0].coords()[0].points
        longitude = cubes[0].coords()[1].points

        spatial_grid = np.zeros((len(latitude),len(longitude),2))

        for ind_la in range(len(latitude)):
            for ind_lo in range(len(longitude)):

                    spatial_grid[ind_la,ind_lo,0] = latitude[ind_la]
                    spatial_grid[ind_la, ind_lo, 1] = longitude[ind_lo]

        return time, forecast_reference_time, numeric_data, spatial_grid




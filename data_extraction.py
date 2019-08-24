import iris
import numpy as np
import pandas as pd

def extract_forecast_data(file_name):
        cubes = iris.load(file_name)
        numeric_data = cubes[0].core_data()
        forecast_reference_time = cubes[0].coord('forecast_reference_time').core_points()
        time = np.round(cubes[0].coord('time').core_points()[0])
        
        return time, forecast_reference_time, numeric_data




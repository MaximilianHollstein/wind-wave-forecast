import data_extraction

import numpy as np
import matplotlib.pyplot as plt


file_name='/Volumes/UNTITLED/GitHub/wind-wave-forecast/data/unzipped_data/CWAM_SWH_2019082300_000.grib2'
time, forecast_reference_time, numeric_data  = data_extraction.extract_forecast_data(file_name)
print(type(numeric_data))

nparr = np.array(numeric_data)
plt.figure()
plt.contourf(np.flipud(nparr),[0.01,0.5,1,1.5,2,2.5,3])

plt.show()



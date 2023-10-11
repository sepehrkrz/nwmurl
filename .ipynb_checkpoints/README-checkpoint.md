# nwmurl

This library contains utility functions to generate National Water Model data URLs

Developed by CIROH 2023
## Usage

1. In the code, you can modify the input parameters, such as `start_date`, `end_date`, `fcst_cycle`, `lead_time`, `varinput`, `geoinput`, and `runinput`, to customize the NWM data retrieval.

2. The code will generate a list of JSON header URLs tailored to your specified parameters using the `generate_urls` function.

## Customize Your Data Retrieval
- `start_date`: A string representing the starting date in the format \"YYYYMMDDHHMM".
- `end_date`: A string representing the ending date in the same format.
- `fcst_cycle`: A list of integers specifying forecast cycle numbers, e.g., `[0, 1, 2, 3, 4]`. These cycles represent specific points in time for which URLs will be generated.
- `lead_time`: A list of integers indicating lead times in hours for forecasts. It determines the time ahead of the forecast start, e.g., `[1, 2, 3, 4]`.
 - `varinput`: An integer or string representing the variable of interest within the NWM data. Available options include:
   - `1` or `\"channel_rt\"` for channel routing data.
   - `2` or `\"land\"` for land data.
   - `3` or `\"reservoir\"` for reservoir data.
   - `4` or `\"terrain_rt\"` for terrain routing data.
   - `5` or `\"forcing\"` for forcing data.
   - `geoinput`: An integer or string specifying the geographic region of interest. Options include:
   - `1` or `\"conus\"` for the continental United States.
   - `2` or `\"hawaii\"` for Hawaii.
   - `3` or `\"puertorico\"` for Puerto Rico.
 - `runinput`: An integer or string representing the NWM run configuration. Available options include:
   - `1` or `\"short_range\"` for short-range forecasts.
   - `2` or `\"medium_range\"` for medium-range forecasts.
   - `3` or `\"medium_range_no_da\"` for medium-range forecasts without data assimilation.
   - `4` or `\"long_range\"` for long-range forecasts.
   - `5` or `\"analysis_assim\"` for analysis-assimilation runs.
   - `6` or `\"analysis_assim_extend\"` for extended analysis-assimilation runs.
    - `7` or `\"analysis_assim_extend_no_da\"` for extended analysis-assimilation runs without data assimilation.
   - `8` or `\"analysis_assim_long\"` for long analysis-assimilation runs.
   - `9` or `\"analysis_assim_long_no_da\"` for long analysis-assimilation runs without data assimilation.
   - `10` or `\"analysis_assim_no_da\"` for analysis-assimilation runs without data assimilation.
   - `11` or `\"short_range_no_da\"` for short-range forecasts without data assimilation.
- `urlbaseinput `:  An integer representing the NWM dataset. Available options include:
	- `1`: "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/".
    - `2`: "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/".
    - `3`: "https://storage.googleapis.com/national-water-model/".
    - `4`: "https://storage.cloud.google.com/national-water-model/".
    - `5`: "gs://national-water-model/".
    - `6`: "gcs://national-water-model/".
    - `7`: "https://noaa-nwm-pds.s3.amazonaws.com/".
    - `8`: "s3://noaa-nwm-pds/".
    - `9`: "https://ciroh-nwm-zarr-copy.s3.amazonaws.com/national-water-model/".
- `meminput `:  An integer representing the ensemble member designation ranging from 0 to 7


## Examples of how to use 



1. Clone the repository to your local machine:
```
  git clone https://github.com/CIROH-UA/data_access_example.git
```

2. Navigate to the repository folder:


3. Launch the Jupyter Notebook to execute the example

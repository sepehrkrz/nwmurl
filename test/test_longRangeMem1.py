import os
import unittest
from urlgennwm import (
    generate_urls_operational,
)  # Import the generate_urls_operational function from your script


class TestGenerateURLs(unittest.TestCase):
    def test_generate_urls_operational_for_long_range_mem1(self):
        # Define test input values
        start_date = "202201120000"
        end_date = "202201130000"
        fcst_cycle = [0, 8]
        lead_time = [1, 18]
        varinput = 1
        geoinput = 1
        runinput = 4  # Set to 4 for the long_range_mem1 folder
        urlbaseinput = 2
        meminput = 1
        write_to_file = True

        # Call the function to generate URLs
        generate_urls_operational(
            start_date,
            end_date,
            fcst_cycle,
            lead_time,
            varinput,
            geoinput,
            runinput,
            urlbaseinput,
            meminput,
            write_to_file,
        )

        # Check if the generated 'filenamelist.txt' file exists
        self.assertTrue(os.path.exists("filenamelist.txt"))

        # Define the expected URLs or patterns for the long_range_mem1 folder
        expected_urls = [
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220112/long_range_mem1/nwm.t00z.long_range.channel_rt_1.tm001.conus.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220112/long_range_mem1/nwm.t00z.long_range.channel_rt_1.tm018.conus.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220112/long_range_mem1/nwm.t08z.long_range.channel_rt_1.tm001.conus.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220112/long_range_mem1/nwm.t08z.long_range.channel_rt_1.tm018.conus.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220113/long_range_mem1/nwm.t00z.long_range.channel_rt_1.tm001.conus.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220113/long_range_mem1/nwm.t00z.long_range.channel_rt_1.tm018.conus.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220113/long_range_mem1/nwm.t08z.long_range.channel_rt_1.tm001.conus.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220113/long_range_mem1/nwm.t08z.long_range.channel_rt_1.tm018.conus.nc",
        ]

        # Read the content of the file and check for the expected content
        with open("filenamelist.txt", "r") as file:
            content = file.read()
            for url in expected_urls:
                self.assertIn(url, content)


if __name__ == "__main__":
    unittest.main()

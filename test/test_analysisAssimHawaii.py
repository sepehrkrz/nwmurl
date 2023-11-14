import os
import unittest
from urlgennwm import (
    generate_urls_operational,
)  # Import the generate_urls_operational function from your script


class TestGenerateURLs(unittest.TestCase):
    def test_generate_urls_operational_for_analysis_assim_hawaii(self):
        # Define test input values
        start_date = "202201120000"
        end_date = "202201130000"
        fcst_cycle = [0, 8]
        lead_time = [1, 18]
        varinput = 1
        geoinput = 2
        runinput = 5  # Set to 5 for the analysis_assim_hawaii folder
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

        # Define the expected URLs or patterns for the analysis_assim_hawaii folder
        expected_urls = [
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220112/analysis_assim/nwm.t00z.analysis_assim.channel_rt.tm001.hawaii.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220112/analysis_assim/nwm.t00z.analysis_assim.channel_rt.tm018.hawaii.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220112/analysis_assim/nwm.t08z.analysis_assim.channel_rt.tm001.hawaii.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220112/analysis_assim/nwm.t08z.analysis_assim.channel_rt.tm018.hawaii.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220113/analysis_assim/nwm.t00z.analysis_assim.channel_rt.tm001.hawaii.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220113/analysis_assim/nwm.t00z.analysis_assim.channel_rt.tm018.hawaii.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220113/analysis_assim/nwm.t08z.analysis_assim.channel_rt.tm001.hawaii.nc",
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/nwm.20220113/analysis_assim/nwm.t08z.analysis_assim.channel_rt.tm018.hawaii.nc",
        ]

        # Read the content of the file and check for the expected content
        with open("filenamelist.txt", "r") as file:
            content = file.read()
            for url in expected_urls:
                self.assertIn(url, content)


if __name__ == "__main__":
    unittest.main()

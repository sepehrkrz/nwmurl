#from gevent import monkey
#monkey.patch_all()
from dateutil import rrule
from datetime import datetime, timezone
from itertools import product
import time
import os

#from concurrent.futures import ThreadPoolExecutor
#import gevent
#import requests
from functools import partial
from tqdm import tqdm

# def check_valid_urls(file_list, session=None):
#     """if not session:
#         session = requests.Session()"""
#     t = tqdm(range(len(file_list)))
#     check_url_part = partial(check_url, t)
#     """with ThreadPoolExecutor(max_workers=10) as executor:
#         valid_file_list = list(executor.map(check_url_part, file_list))"""
#     valid_file_list = [gevent.spawn(check_url_part, file_name) for file_name in file_list]
#     gevent.joinall(valid_file_list)
#     return [file.get() for file in valid_file_list if file.get() is not None]


# def check_url(t, file):
#     filename = file.split("/")[-1]
#     try:
#         with requests.head(file) as response:
#             if response.status_code == 200:
#                 t.set_description(f"Found: {filename}")
#                 t.update(1)
#                 t.refresh()
#                 return file
#             else:
#                 t.set_description(f"Not Found: {filename}")
#                 t.update(1)
#                 t.refresh()
#                 return None
#         #response = session.head(file, timeout=1)
#     except requests.exceptions.RequestException:
#         t.set_description(f"Not Found: {filename}")
#         t.update(1)
#         t.refresh()
#         return None
rundict = {
    1: "short_range",
    2: "medium_range",
    3: "medium_range_no_da",
    4: "long_range",
    5: "analysis_assim",
    6: "analysis_assim_extend",
    7: "analysis_assim_extend_no_da",
    8: "analysis_assim_long",
    9: "analysis_assim_long_no_da",
    10: "analysis_assim_no_da",
    11: "short_range_no_da",
}
memdict = {
    1: "mem_1",
    2: "mem_2",
    3: "mem_3",
    4: "mem_4",
    5: "mem_5",
    6: "mem_6",
    7: "mem_7",
}
vardict = {1: "channel_rt", 2: "land", 3: "reservoir", 4: "terrain_rt", 5: "forcing"}
geodict = {1: "conus", 2: "hawaii", 3: "puertorico"}

def selectvar(vardict, varinput):
    return vardict[varinput]


def selectgeo(geodict, geoinput):
    return geodict[geoinput]


def selectrun(rundict, runinput):
    return rundict[runinput]


def makename(
    date,
    run_name,
    var_name,
    fcst_cycle,
    fcst_hour,
    geography,
    run_type,
    fhprefix="",
    runsuffix="",
    varsuffix="",
    run_typesuffix="",
    urlbase_prefix="",
):
    """This function handles preprocessed text and converts it into the applicable url to access the appropriate file."""

    datetxt = f"nwm.{date.strftime('%Y%m%d')}"
    foldertxt = f"{run_type}{run_typesuffix}"
    filetxt = f"nwm.t{fcst_cycle:02d}z.{run_name}{runsuffix}.{var_name}{varsuffix}.{fhprefix}{fcst_hour:03d}.{geography}.nc"
    return f"{urlbase_prefix}{datetxt}/{foldertxt}/{filetxt}"


# setting run_type
def run_type(runinput, varinput, geoinput, default=""):
    """This function takes the numeric command line input and converts to the text used in the url."""

    if varinput == 5:  # if forcing
        if runinput == 5 and geoinput == 2:  # if analysis_assim and hawaii
            return "forcing_analysis_assim_hawaii"
        elif runinput == 5 and geoinput == 3:  # if analysis_assim and puerto rico
            return "forcing_analysis_assim_puertorico"
        elif runinput == 1 and geoinput == 2:  # if short range and hawaii
            return "forcing_short_range_hawaii"
        elif runinput == 1 and geoinput == 3:  # if short range and puerto rico
            return "forcing_short_range_puertorico"
        elif runinput == 5:  # if analysis assim
            return "forcing_analysis_assim"
        elif runinput == 6:  # if analysis_assim_extend
            return "forcing_analysis_assim_extend"
        elif runinput == 2:  # if medium_range
            return "forcing_medium_range"
        elif runinput == 1:  # if short range
            return "forcing_short_range"

    elif runinput == 5 and geoinput == 3:  # if analysis_assim and puertorico
        return "analysis_assim_puertorico"

    elif runinput == 10 and geoinput == 3:  # if analysis_assim_no_da and puertorico
        return "analysis_assim_puertorico_no_da"

    elif runinput == 1 and geoinput == 3:  # if short_range and puerto rico
        return "short_range_puertorico"

    elif runinput == 11 and geoinput == 3:  # if short_range_no_da and puerto rico
        return "short_range_puertorico_no_da"

    else:
        return default


def fhprefix(runinput):
    if 4 <= runinput <= 10:
        return "tm"
    return "f"


def varsuffix(meminput):
    if meminput in range(1, 8):
        return f"_{meminput}"
    else:
        return ""


def run_typesuffix(meminput):
    if meminput in range(1, 8):
        return f"_mem{meminput}"
    else:
        return ""


def select_forecast_cycle(fcst_cycle=None, default=None):
    if fcst_cycle:
        return fcst_cycle
    else:
        return default


def select_lead_time(lead_time=None, default=None):
    if lead_time:
        return lead_time
    else:
        return default


urlbasedict = {
    0: "",
    1: "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/",
    2: "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/",
    3: "https://storage.googleapis.com/national-water-model/",
    4: "https://storage.cloud.google.com/national-water-model/",
    5: "gs://national-water-model/",
    6: "gcs://national-water-model/",
    7: "https://noaa-nwm-pds.s3.amazonaws.com/",
    8: "s3://noaa-nwm-pds/",
    9: "https://ciroh-nwm-zarr-copy.s3.amazonaws.com/national-water-model/",
    
}



def selecturlbase(urlbasedict, urlbaseinput, defaulturlbase=""):
    if urlbaseinput:
        return urlbasedict[urlbaseinput]
    else:
        return defaulturlbase


def create_file_list(
    runinput,
    varinput,
    geoinput,
    meminput,
    start_date=None,
    end_date=None,
    fcst_cycle=None,
    urlbaseinput=None,
    lead_time=None,  # TODO: change this order; placed here to avoid breaking change
):
    """for given date,  run, var, fcst_cycle, and geography, print file names for the valid time (the range of fcst_hours) and dates"""

    runsuff = ""

    try:
        geography = selectgeo(geodict, geoinput)
    except:
        geography = "geography_error"
    try:
        run_name = selectrun(rundict, runinput)
    except:
        run_name = "run_error"
    try:
        var_name = selectvar(vardict, varinput)
    except:
        var_name = "variable_error"
    try:
        urlbase_prefix = selecturlbase(urlbasedict, urlbaseinput)
    except:
        urlbase_prefix = "urlbase_error"

    try:
        _dtstart = datetime.strptime(start_date, "%Y%m%d%H%M")
        _until = datetime.strptime(end_date, "%Y%m%d%H%M")
    except:
        today = datetime.now(timezone.utc)
        _dtstart = today
        _until = today

    dates = rrule.rrule(
        rrule.DAILY,
        dtstart=_dtstart,
        until=_until,
    )
    run_t = run_type(runinput, varinput, geoinput, run_name)
    fhp = fhprefix(runinput)
    vsuff = varsuffix(meminput)
    rtsuff = run_typesuffix(meminput)

    if runinput == 1:  # if short_range
        if varinput == 5:  # if forcing
            if geoinput == 2:  # hawaii
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(0, 13, 12)),
                    select_lead_time(lead_time, range(1, 49)),
                )
            elif geoinput == 3:  # puertorico
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, [6]),
                    select_lead_time(lead_time, range(1, 48)),
                )
            else:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(24)),
                    select_lead_time(lead_time, range(1, 19)),
                )
        elif geoinput == 3:  # if puerto rico
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, range(6, 19, 12)),
                select_lead_time(lead_time, range(1, 48)),
            )
        else:
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, range(24)),
                select_lead_time(lead_time, range(1, 19)),
            )
    elif runinput == 2:  # if medium_range
        if varinput == 5:  # if forcing
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, range(0, 19, 6)),
                select_lead_time(lead_time, range(1, 241)),
            )
        else:
            default_fc = range(0, 19, 6)
            if meminput == 1:
                if varinput in {1, 3}:
                    prod = product(
                        dates,
                        select_forecast_cycle(fcst_cycle, default_fc),
                        select_lead_time(lead_time, range(1, 241)),
                    )
                elif varinput in {2, 4}:
                    prod = product(
                        dates,
                        select_forecast_cycle(fcst_cycle, default_fc),
                        select_lead_time(lead_time, range(3, 241, 3)),
                    )
                else:
                    raise ValueError("varinput")
            elif meminput in range(2, 8):
                if varinput in {1, 3}:
                    prod = product(
                        dates,
                        select_forecast_cycle(fcst_cycle, default_fc),
                        select_lead_time(lead_time, range(1, 205)),
                    )
                elif varinput in {2, 4}:
                    prod = product(
                        dates,
                        select_forecast_cycle(fcst_cycle, default_fc),
                        select_lead_time(lead_time, range(3, 205, 3)),
                    )
                else:
                    raise ValueError("varinput")
            else:
                raise ValueError("meminput")
    elif runinput == 3:  # if medium_range_no_da
        if varinput == 1:
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, range(0, 13, 6)),
                select_lead_time(lead_time, range(3, 240, 3)),
            )
        else:
            raise ValueError("only valid variable for a _no_da type run is channel_rt")
    elif runinput == 4:  # if long_range
        default_fc = range(0, 19, 6)
        if varinput in {1, 3}:
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, default_fc),
                select_lead_time(lead_time, range(6, 721, 6)),
            )
        elif varinput == 2:
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, default_fc),
                select_lead_time(lead_time, range(24, 721, 24)),
            )
        else:
            raise ValueError("varinput")
    elif runinput == 5:  # if analysis_assim (simplest form)
        if varinput == 5:  # if forcing
            if geoinput == 2:  # hawaii
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(19)),
                    select_lead_time(lead_time, range(3)),
                )
            else:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(20)),
                    select_lead_time(lead_time, range(3)),
                )
        else:
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, range(24)),
                select_lead_time(lead_time, range(3)),
            )
    elif runinput == 6:  # if analysis_assim_extend
        prod = product(
            dates,
            select_forecast_cycle(fcst_cycle, [16]),
            select_lead_time(lead_time, range(28)),
        )
    elif runinput == 7:  # if analysis_assim_extend_no_da
        if varinput == 1:
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, [16]),
                select_lead_time(lead_time, range(28)),
            )
        else:
            raise ValueError("only valid variable for a _no_da type run is channel_rt")
    elif runinput == 8:  # if analysis_assim_long
        prod = product(
            dates,
            select_forecast_cycle(fcst_cycle, range(0, 24, 6)),
            select_lead_time(lead_time, range(12)),
        )
    elif runinput == 9:  # if analysis_assim_long_no_da
        if varinput == 1:
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, range(0, 24, 6)),
                select_lead_time(lead_time, range(12)),
            )
        else:
            raise ValueError("only valid variable for a _no_da type run is channel_rt")

    elif runinput == 10:  # if analysis_assim_no_da
        if varinput == 1:
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, range(21)),
                select_lead_time(lead_time, range(3)),
            )
        else:
            raise ValueError("only valid variable for a _no_da type run is channel_rt")

    elif runinput == 11 and geoinput == 3:  # if short_range_puertorico_no_da
        if varinput == 1:
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, range(6, 19, 12)),
                select_lead_time(lead_time, range(1, 49)),
            )
        else:
            raise ValueError("only valid variable for a _no_da type run is channel_rt")
    else:
        raise ValueError("run error")

    r = []
    for _dt, _fc, _fh in prod:
        r.append(
            makename(
                _dt,
                run_name,
                var_name,
                _fc,
                _fh,
                geography,
                run_t,
                fhp,
                runsuff,
                vsuff,
                rtsuff,
                urlbase_prefix,
            )
        )
    return r
def generate_urls(start_date,end_date, fcst_cycle, lead_time, varinput, geoinput, runinput, urlbaseinput):

    
    start_date = start_date
    end_date   = end_date
    fcst_cycle = fcst_cycle
    # fcst_cycle = None # Retrieves a full day for each day within the range given.
    #lead_time = [1]
    lead_time = lead_time
    varinput = varinput
    #vardict = {1: "channel_rt", 2: "land", 3: "reservoir", 4: "terrain_rt", 5: "forcing"}
    geoinput = geoinput
    #geodict = {1: "conus", 2: "hawaii", 3: "puertorico"}
    meminput = 0
    urlbaseinput = urlbaseinput
    runinput = runinput
    # rundict = {
    # 1: "short_range",
    # 2: "medium_range",
    # 3: "medium_range_no_da",
    # 4: "long_range",
    # 5: "analysis_assim",
    # 6: "analysis_assim_extend",
    # 7: "analysis_assim_extend_no_da",
    # 8: "analysis_assim_long",
    # 9: "analysis_assim_long_no_da",
    # 10: "analysis_assim_no_da",
    # 11: "short_range_no_da",
    # }

    file_list = create_file_list(
        runinput,
        varinput,
        geoinput,
        meminput,
        start_date,
        end_date,
        fcst_cycle,
        urlbaseinput,
        lead_time,
    )
    if os.path.exists("filenamelist.txt"):
        os.remove("filenamelist.txt")   
    with open("filenamelist.txt", "wt") as file:
        if urlbaseinput == 9:
            for item in file_list:
                file.write(f"{item}.json\n")
        else:
            for item in file_list:
                file.write(f"{item}\n")



# start_date = "202201120000"
# end_date   = "202201130000"
# fcst_cycle = [0,8]
# lead_time = [1,18]
# varinput = 1
# geoinput = 1
# runinput = 1
# urlbaseinput = 7
# generate_urls(start_date, end_date, fcst_cycle, lead_time, varinput, geoinput, runinput, urlbaseinput)

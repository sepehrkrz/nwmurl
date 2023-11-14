from dateutil import rrule
from datetime import datetime, timezone, timedelta
from itertools import product
import time
import os


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

retrospective_var_types = {
    1: ".CHRTOUT_DOMAIN1.comp",
    2: ".GWOUT_DOMAIN1.comp",
    3: ".LAKEOUT_DOMAIN1.comp",
    4: ".LDASOUT_DOMAIN1.comp",
    5: ".RTOUT_DOMAIN1.comp",
    6: ".LDASIN_DOMAIN1.comp",
}

objecttypes = {1: "forcing/", 2: "model_output/"}

urlbasedict_retro = {
    1: "https://noaa-nwm-retrospective-2-1-pds.s3.amazonaws.com/",
    2: "s3://noaa-nwm-retrospective-2-1-pds/",
    3: "https://ciroh-nwm-zarr-retrospective-data-copy.s3.amazonaws.com/noaa-nwm-retrospective-2-1-zarr-pds/",
}


def selecturlbase(urlbasedict, urlbaseinput, defaulturlbase=""):
    if urlbaseinput in urlbasedict:
        return urlbasedict[urlbaseinput]
    else:
        return defaulturlbase


def generate_urls_retro(
    start_date=None,
    end_date=None,
    urlbaseinput=None,
    objecttype=objecttypes,
    selected_var_types=None,
    write_to_file=False,
):
    urlbase_prefix = urlbasedict_retro[urlbaseinput]
    objecttype = [objecttypes[i] for i in objecttype]
    retrospective_var_types_selected = [
        retrospective_var_types[i] for i in selected_var_types
    ]

    start_dt = datetime.strptime(start_date, "%Y%m%d%H%M")
    end_dt = datetime.strptime(end_date, "%Y%m%d%H%M")

    delta = end_dt - start_dt
    date_range = [
        start_dt + timedelta(hours=i)
        for i in range(delta.days * 24 + delta.seconds // 3600 + 1)
    ]

    file_list = []
    for date in date_range:
        for obj_type in objecttype:
            file_names = generate_url_retro(
                date, obj_type, urlbase_prefix, retrospective_var_types_selected
            )
            if file_names is not None:
                if isinstance(file_names, list):
                    file_list.extend(file_names)
                else:
                    file_list.append(file_names)
    if write_to_file == True:
        if os.path.exists("retro_filenamelist.txt"):
            os.remove("retro_filenamelist.txt")
        with open("retro_filenamelist.txt", "wt") as file:
            for item in file_list:
                file.write(f"{item}\n")
    return file_list


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
        if urlbaseinput == 9:
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
                ) + ".json"
            )
        else:
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


def generate_url_retro(date, file_type, urlbase_prefix, retrospective_var_types=None):
    year_txt = date.strftime("%Y")
    date_txt = date.strftime("%Y%m%d%H")

    if "forcing" in file_type and date.year < 2007:
        url = f"{urlbase_prefix}{file_type}{year_txt}/{date_txt}00.LDASIN_DOMAIN1"
    elif "forcing" in file_type and date.year >= 2007:
        url = f"{urlbase_prefix}{file_type}{year_txt}/{date_txt}.LDASIN_DOMAIN1"
    elif "model_output" in file_type:
        url = [
            f"{urlbase_prefix}{file_type}{year_txt}/{date_txt}00{type}"
            for type in retrospective_var_types
        ]

    return url


def generate_urls_operational(
    start_date,
    end_date,
    fcst_cycle,
    lead_time,
    varinput,
    geoinput,
    runinput,
    urlbaseinput,
    meminput,
    write_to_file=False,
):
    start_date = start_date
    end_date = end_date
    fcst_cycle = fcst_cycle
    # fcst_cycle = None # Retrieves a full day for each day within the range given.
    # lead_time = [1]
    lead_time = lead_time
    varinput = varinput
    # vardict = {1: "channel_rt", 2: "land", 3: "reservoir", 4: "terrain_rt", 5: "forcing"}
    geoinput = geoinput
    # geodict = {1: "conus", 2: "hawaii", 3: "puertorico"}
    meminput = meminput
    urlbaseinput = urlbaseinput
    runinput = runinput

    if (
        runinput == 1
        or runinput == 5
        or runinput == 6
        or runinput == 7
        or runinput == 8
        or runinput == 9
        or runinput == 10
        or runinput == 11
    ):
        meminput = None
        print(
            "no ensemble members available for the given runinput therefore, meminput set to None"
        )
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
    if write_to_file == True:
        if os.path.exists("filenamelist.txt"):
            os.remove("filenamelist.txt")
        with open("filenamelist.txt", "wt") as file:
            for item in file_list:
                file.write(f"{item}\n")
    return file_list

import re
import pandas as pd
import numpy as np

import metpy.calc as mpcalc
from metpy.units import units

# Read in the station dictionary
stations = pd.read_csv('master_location_database.csv', skiprows=1, low_memory=False)

def extract_plev_data(plev, df):
    """
    Parses the pressure level given the dataframe with data
    """

    try:
        # Subset for the pressure level
        df_sub = df[df.index == plev]

        temp = df_sub.temp.values[0]
        dewp = df_sub.dewp.values[0]
        height = df_sub.height.values[0]
        wdir = df_sub.wdir.values[0]
        wspd = df_sub.wspd.values[0]

    except:
        temp, dewp, height, wdir, wspd = np.nan, np.nan, np.nan, np.nan, np.nan

    return temp, dewp, height, wdir, wspd

def parse_ttaa_file(text_file):
    """
    Parses a text file containing TTAA messages - which include upper air data

    Input
    -----------------
    text_file = text file with data (ex. file from Unidata Thredds Test Server)

    Returns
    -----------------
    df = Pandas dataframe with data

    """

    # Read in the text file and strip the seperate lines
    with open(text_file) as f:
        text = " ".join(line.strip() for line in f)

    # Replace double spaces with single spaces
    text = text.replace("  ", " ")

    # Regular expression with format of the text
    ttaa = r'(TTAA) ([0-9]{5}) ([0-9]{5}) ([9][9][0-9]{3}) ([0-9]*) ([0-9]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([9][2][0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*) ([0-9]*|[/]*)'

    # List of all observations in the file
    list = re.findall(ttaa, text)

    df_list = []

    for text in list:
        df_list.append(parse_ttaa(text))

    df = pd.concat(df_list)

    df['u_wind'], df['v_wind'] = mpcalc.wind_components(df.speed.values * units.kts, df.direction.values * units.deg)

    return df.drop_duplicates()

def parse_ttaa(text_tuple, station_dict=stations):
    """
    Parses ttaa strings
    """

    text = []
    for item in text_tuple:
        text.append(item)

    # TTAA section
    text[0]

    # Section B - Datetime
    datetime = str(text[1])

    # Get the date
    date = int(datetime[0:2]) - 50

    # Section A - WMO identifier
    wmo_code = text[2]


    try:
        # Grab the lat and lon
        lat = station_dict[station_dict.wmo == wmo_code].lat_prp.values[0]
        lon = station_dict[station_dict.wmo == wmo_code].lon_prp.values[0]
        country = station_dict[station_dict.wmo == wmo_code].country.values[0]

    except:
        lat = np.nan
        lon = np.nan

    # Station Data - surface station pressure
    sfc_pres = float(text[3][2:])

    # Temp and Dewpoint Depression
    temp = float(text[4][0:3])/10
    dd = float(text[4][3:])

    if dd < 50:
        dd = dd/10

    else:
        dd = dd - 50

    dwpt = temp - dd

    # Wind direction and speed
    wdir = float(text[5][0:3])
    wspd = float(text[5][3:])

    df = pd.DataFrame()

    i = 6

    # Loop through pressure levels
    for entry in text[6:]:

        try:
            pressure, heights = parse_height(text[i])
            temp, dewp = parse_temp_dewp(text[i+1])
            wdir, wspd = parse_wind(text[i+2])


            if int((str(pressure)[0:2])) % 11 == 0:
                None

            else:
                df = df.append({'datetime':datetime,
                                'country':country,
                                'date':date,
                                'station_id':wmo_code,
                                'latitude':lat,
                                'longitude':lon,
                                'pressure':pressure,
                                'height': heights,
                                'temperature':temp,
                                'dewpoint':dewp,
                                'direction':wdir,
                                'speed':wspd}, ignore_index=True)

                # Make sure to only return values that are physically possible
                df = df[df.speed > 0]
        except:
            continue

        i=i+3


    return df

def parse_temp_dewp(ob):
    """
    Parses a temperature and dewpoint depression group
    """

    if ob == '/////':
        temp = np.nan
        dwpt = np.nan

    else:

        # Bring in the temperature (celsius)
        temp = int(ob[0:3])

        if temp % 2 == 0:
            temp = temp/10

        else:
            temp = -temp/10

        # Bring in the dewpoint depression (difference between temperature and dewpoint)
        dd = float(ob[3:])

        # Calculate dewpoint from temp and dewpoint depression
        if dd < 50:
            dd = dd/10

        else:
            dd = dd - 50

        dwpt = temp - dd

    return temp, dwpt

def parse_wind(ob):
    """
    Parses wind speed and direction variables
    """
    if ob == '/////':

        wdir = np.nan
        wspd = np.nan

    else:
        # Check to see if the middle digit is divisible by 5
        if (int(ob[2]) % 5) == 0:
            wdir = int(ob[0:3])
            wspd = int(ob[3:])

        else:
            wdir = int(ob[0:2] + ob[-1])
            wspd = int(ob[2:]) - 500

    return wdir, wspd

def parse_height(ob):
    """
    Extracts height in meters from string
    """


    if ob[0:2] == '00':
        pressure = 1000

    elif ob[1] == '2':
        pressure = ob[0:2] + '5'

    else:
        pressure = ob[0:2] + '0'

    # Conver into an integer
    pressure = int(pressure)

    og_height = ob[2:]

    if pressure == 850:
        height = '1' + og_height

    elif pressure == 700:
        height = '3' + og_height

    elif pressure == 500:
        height = og_height + '0'

    elif pressure == 400:
        height = og_height + '0'

    elif pressure == 300:
        height = og_height + '0'

    elif pressure == 250:
        height = '1' + og_height + '0'

    elif pressure == 200:
        height = '1' + og_height + '0'

    elif pressure == 150:
        height = '1' + og_height + '0'

    elif pressure == 100:
        height = '1' + og_height + '0'

    else:
        height = og_height

    height = int(height)

    return pressure, height

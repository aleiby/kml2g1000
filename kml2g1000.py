import os
import glob
import math
from datetime import datetime
from lxml import etree as ET

# Download path for FlightAware KML files.
srcDir = r'C:\Users\<User Name>\Downloads'

# Returns an array containing the texts of all the specified child nodes of root.
def getAll(root, node):
    return [_.text for _ in root.iterfind('.//'+node, namespaces=root.nsmap)]

# Calculates the groundspeed given two lat/long coordinates and associated start/end datetimes.
def calcSpeed(fm, to, start, end):
    dx = math.hypot(*[b - a for a, b in zip(fm, to)]) * 60.0 # nautical miles
    dt = (end - start).total_seconds() / 3600.0 # hours
    return round(dx / dt) if dt else 0

# Converts a kml tracklog exported from flightaware.com to G1000 csv format.
def export(kml):
    hdr = '  Lcl Date, Lcl Time, UTCOfst, AtvWpt,     Latitude,    Longitude,    AltB, BaroA,  AltMSL,   OAT,    IAS, GndSpd,    VSpd,  Pitch,   Roll,  LatAc, NormAc,   HDG,   TRK, volt1,  FQtyL,  FQtyR, E1 FFlow, E1 FPres, E1 OilT, E1 OilP, E1 MAP, E1 RPM, E1 CHT1, E1 CHT2, E1 CHT3, E1 CHT4, E1 EGT1, E1 EGT2, E1 EGT3, E1 EGT4,  AltGPS, TAS, HSIS,    CRS,   NAV1,   NAV2,    COM1,    COM2,   HCDI,   VCDI, WndSpd, WndDr, WptDst, WptBrg, MagVar, AfcsOn, RollM, PitchM, RollC, PichC, VSpdG, GPSfix,  HAL,   VAL, HPLwas, HPLfd, VPLwas'
    fmt = '{date}, {time},   00:00,       , {lat: >12}, {lng: >12},        ,      , {alt: >7},      ,       , {gspd: >6}'
    tail = ',        ,       ,       ,       ,       ,      ,      ,      ,       ,       ,         ,         ,        ,        ,       ,       ,        ,        ,        ,        ,        ,        ,        ,        ,        ,    ,     ,       ,       ,       ,        ,        ,       ,       ,       ,      ,       ,       ,       ,       ,      ,       ,      ,      ,      ,       ,     ,      ,       ,      ,       '
    
    tree = ET.parse(kml)
    root = tree.getroot()

    # Collect all the timestamps and breadcrumbs.
    whens = getAll(root, 'when')
    coords = getAll(root, 'gx:coord')
 
    # Export the csv header.
    csv = [hdr]

    # Export the csv data.
    fm = None
    start = None
    for when, coord in zip(whens, coords):
        # Parse data (e.g. 2022-06-09T15:42:34Z)
        date, time = when.split('T')
        time = time[:-1] # strip Z
        lng, lat, alt = coord.split(' ')

        # Calculate ground speed.
        # ForeFlight will not accept a G1000 file without valid data here.
        # This is a very rough estimate based on the reported breadcrumbs.
        # FlightAware appears to collect actual data from ADS-B, but does not include it in the kml unfortuantely.
        to = (float(lat), float(lng))
        end = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
        gspd = calcSpeed(fm, to, start, end) if fm and start else 0
        fm = to
        start = end
        
        # Append data with trailing commas for unset values.
        csv.append(fmt.format(date=date, time=time, lat=lat, lng=lng, alt=alt, gspd=gspd) + tail)

    # Write file to disk.
    base = os.path.splitext(kml)[0]
    with open(base + '.csv', 'w') as f:
        f.writelines('\n'.join(csv))

# Convert all files in source directory.    
files = glob.glob(os.path.join(srcDir, '*.kml'))
for fileName in files:
    print('Exporting ' + fileName)
    export(fileName)
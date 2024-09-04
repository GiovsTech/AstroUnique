import sys
sys.path.append('../')

from astropy.coordinates import EarthLocation, SkyCoord, AltAz, get_sun
from astropy.time import Time
from astropy.io import fits
from astropy import units as u
from astroquery.simbad import Simbad
import pickle
import requests
import os
def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url)
    data = response.json()
    if data['results'] != '0':
        elevation = data['results'][0]['elevation']
        return elevation
    else:
        return 0

def cd_to_cel(lat, lon, elevation=0, file="star_coord_obj/data.skycoord"):
    elevation = get_elevation(lat,lon) if elevation == 0 else 0
    location = EarthLocation(lat=lat, lon=lon, height=elevation)
    coord_icrs = SkyCoord(location.get_gcrs(obstime=Time.now()), frame='gcrs')
    coord_galactic = coord_icrs.galactic
    with open(file, "wb") as data_storage:
        skycoord_f = pickle.dump(coord_galactic, data_storage)
    data_storage.close()
    return "None"


def astro_search_star(skycoord, file):
    dict_map = {}
    astro_query = Simbad.query_region(skycoord, radius=20 * u.arcsec)
    if astro_query == None:
        dict_map["Object"] = "None"
    for row in astro_query:
        for i in range(len(row)):
            dict_map[f"Object {i}"] = {'Name': row['MAIN_ID'], 'RA_COORD' : row['RA'], 'DEC_COORD' : row['DEC']}
    return astro_name_for(dict_map, file)

def astro_name_for(d1, file, file1):
    for d in d1.values():
        if d == "None":
            return None
        os.rename(file, {}).format(d["Name"])
        with open(file1, "w") as data_storage:
            file.write(f"Name: {d['Name']}\n RA_COORD: {d['RA_COORD']}\n DEC_COORD: {d['DEC_COORD']}")
    file.close()

if __name__ == '__main__':
    with open("star_coord_obj/data.skycoord", "rb") as data_storage:
                    skycoord_f = pickle.load(data_storage)
                    print(astro_search_star(skycoord_f))

                
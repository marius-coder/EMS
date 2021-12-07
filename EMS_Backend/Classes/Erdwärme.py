

import urllib.request, json , urllib.parse
with urllib.request.urlopen("https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:ERDWSONDOGD") as url:
    data = json.loads(url.read().decode())
    print(data)



import requests
import urllib.parse
def from_address(address_string="Stephansplatz, Wien, Österreich"):
    parsed_address = urllib.parse.quote(address_string)
    url = 'https://nominatim.openstreetmap.org/search/' + parsed_address +'?format=json'
    response = requests.get(url).json()
    location = (response[0]["lat"], response[0]["lon"])
    return location

from_address("Giefinggasse 6, 1020 Wien, Österreich")


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#point = Point(0.5, 0.5)
#polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
#print(polygon.contains(point))
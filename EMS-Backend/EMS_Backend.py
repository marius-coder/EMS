

import urllib.request, json 



with urllib.request.urlopen("https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:ERDWSONDOGD") as url:
    data = json.loads(url.read().decode())
    print(type(data))


print(data["type"])
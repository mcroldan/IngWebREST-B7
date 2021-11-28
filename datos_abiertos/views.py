from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

from os import name
from django.shortcuts import render
import urllib.request
import json
import math

URL_APARCAMIENTOS = "https://datosabiertos.malaga.eu/recursos/aparcamientos/ocupappublicosmun/ocupappublicosmunfiware.json"
URL_ATASCOS = "https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_cortesTrafico-4326.geojson"

# Create your views here.

def get_json(request,url):
    req = urllib.request.Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
    handler = urllib.request.urlopen(req)
    data = json.loads(handler.read().decode())
    return data

def get_aparcamientos(request): 
    data = get_json(request,URL_APARCAMIENTOS)
    points = []
    locations = []
    for aparcamiento in data:
        locations.append(aparcamiento['location'])
    for location in locations:
        lon_aparcamiento = float(location.get('value').get('coordinates')[1])
        lat_aparcamiento = float(location.get('value').get('coordinates')[0])
        if lon_aparcamiento != 0.0 and lat_aparcamiento != 0.0:
            points.append([lat_aparcamiento,lon_aparcamiento])
    context = {'points' : json.dumps(points), 'datos' : 'aparcamientos'}
    return render(request, "maps.html", context)

def get_json_aparcamientos(request): 
    data = get_json(request,URL_APARCAMIENTOS)
    locations = []
    for aparcamiento in data:
        locations.append(aparcamiento['location'])
    return HttpResponse(json.dumps(locations))

def measure(lat1, lon1, lat2, lon2):  # generally used geo measurement function
    R = 6378.137; # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000; # meters


def dentro_perimetro(lon_aparcamiento,lat_aparcamiento,source,radius):
    #distancia entre coordenada y aparcamiento < radio
    dentro = False
    distancia = measure(source[0],source[1],lat_aparcamiento,lon_aparcamiento)
    if(distancia <= radius): 
        dentro = True 
    return dentro
    
def get_aparcamientos_dentro(request, lon, lat, radius): 
    data = get_json(request,URL_APARCAMIENTOS)

    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]

    locations = []
    for aparcamiento in data:
        locations.append(aparcamiento['location'])
    points = []
    for location in locations:
        lon_aparcamiento = float(location.get('value').get('coordinates')[1])
        lat_aparcamiento = float(location.get('value').get('coordinates')[0])
        if lon_aparcamiento != 0.0 and lat_aparcamiento != 0.0 and dentro_perimetro(float(lon_aparcamiento),float(lat_aparcamiento),source,radius):
            points.append([lat_aparcamiento,lon_aparcamiento])
    context = {'points' : json.dumps(points), 'source' : json.dumps(source), 'radius' : radius, 'datos' : 'aparcamientos'}
    return render(request, "maps.html", context)

def get_json_aparcamientos_dentro(request, lon, lat, radius): 
    data = get_json(request,URL_APARCAMIENTOS)

    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]

    locations = []
    for aparcamiento in data:
        locations.append(aparcamiento['location'])
    points = []
    for location in locations:
        lon_aparcamiento = float(location.get('value').get('coordinates')[1])
        lat_aparcamiento = float(location.get('value').get('coordinates')[0])
        if lon_aparcamiento != 0.0 and lat_aparcamiento != 0.0 and dentro_perimetro(float(lon_aparcamiento),float(lat_aparcamiento),source,radius):
            points.append(json.dumps(location))
    return HttpResponse(json.dumps(points))

def get_aparcamiento_cercano(request, lon, lat):
    data = get_json(request,URL_APARCAMIENTOS)
    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]
    locations = []
    for aparcamiento in data:
        locations.append(aparcamiento['location'])
    point = []
    for location in locations:
        print(location)
        lon_aparcamiento = float(location.get('value').get('coordinates')[1])
        lat_aparcamiento = float(location.get('value').get('coordinates')[0])
        if len(point) == 0  :
            point = [lat_aparcamiento, lon_aparcamiento]
        else:
            if lat_aparcamiento != 0.0 and lon_aparcamiento != 0.0 and ((abs(latF - lat_aparcamiento) + abs(lonF - lon_aparcamiento)) < (abs(latF - point[0]) + abs(lonF - point[1]))):
                point = [lat_aparcamiento, lon_aparcamiento]
    context = {'point' : json.dumps(point), 'source' : json.dumps(source), 'datos' : 'aparcamientos'}
    return render(request, "maps.html", context)

def get_json_aparcamiento_cercano(request, lon, lat):
    data = get_json(request,URL_APARCAMIENTOS)
    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]
    locations = []
    for aparcamiento in data:
        locations.append(aparcamiento['location'])
    point = []
    for location in locations:
        print(location)
        lon_aparcamiento = float(location.get('value').get('coordinates')[1])
        lat_aparcamiento = float(location.get('value').get('coordinates')[0])
        if len(point) == 0  :
            point = [lat_aparcamiento, lon_aparcamiento]
        else:
            if lat_aparcamiento != 0.0 and lon_aparcamiento != 0.0 and ((abs(latF - lat_aparcamiento) + abs(lonF - lon_aparcamiento)) < (abs(latF - point[0]) + abs(lonF - point[1]))):
                point = [lat_aparcamiento, lon_aparcamiento]
    return HttpResponse(json.dumps(point))
    

def get_atascos(request): 
    data = get_json(request,URL_ATASCOS)

    locations = []
    for x in range(data['totalFeatures']):
        locations.append(data['features'][x]['geometry'])
    points = []
    for location in locations:
        if location.get('coordinates')[0] != 0.0 and location.get('coordinates')[1] != 0.0:
            points.append(location.get('coordinates'))
    context = {'points' : json.dumps(points), 'datos' : 'atascos'}
    return render(request, "maps.html", context)

def get_json_atascos(request): 
    data = get_json(request,URL_ATASCOS)

    locations = []
    for x in range(data['totalFeatures']):
        locations.append(data['features'][x]['geometry'])
    return HttpResponse(json.dumps(locations))

def get_atasco_cercano(request, lon, lat):
    data = get_json(request,URL_ATASCOS)
    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]

    locations = []
    for x in range(data['totalFeatures']):
        locations.append(data['features'][x]['geometry'])
    point = []
    for location in locations:
        lonP = float(location.get('coordinates')[1])
        latP = float(location.get('coordinates')[0])
        if len(point) == 0  :
            point = [latP, lonP]
        else:
            if latP != 0.0 and lonP != 0.0 and ((abs(latF - latP) + abs(lonF - lonP)) < (abs(latF - point[0]) + abs(lonF - point[1]))):
                point = [latP, lonP]
    context = {'point' : json.dumps(point), 'source' : json.dumps(source), 'datos' : 'atascos'}
    return render(request, "maps.html", context)    

def get_json_atasco_cercano(request, lon, lat):
    data = get_json(request,URL_ATASCOS)
    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]

    locations = []
    for x in range(data['totalFeatures']):
        locations.append(data['features'][x]['geometry'])
    point = []
    for location in locations:
        lonP = float(location.get('coordinates')[1])
        latP = float(location.get('coordinates')[0])
        if len(point) == 0  :
            point = [latP, lonP]
        else:
            if latP != 0.0 and lonP != 0.0 and ((abs(latF - latP) + abs(lonF - lonP)) < (abs(latF - point[0]) + abs(lonF - point[1]))):
                point = [latP, lonP]

    return HttpResponse(json.dumps(point))       

def get_atascos_dentro(request, lon, lat, radius): 
    data = get_json(request,URL_ATASCOS)
    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]

    locations = []
    for x in range(data['totalFeatures']):
        locations.append(data['features'][x]['geometry'])
    points = []
    for location in locations:
        lon_aparcamiento = float(location.get('coordinates')[1])
        lat_aparcamiento = float(location.get('coordinates')[0])
        if lon_aparcamiento != 0.0 and lat_aparcamiento != 0.0 and dentro_perimetro(float(lon_aparcamiento),float(lat_aparcamiento),source,radius):
            points.append([lat_aparcamiento,lon_aparcamiento])
    context = {'points' : json.dumps(points), 'source' : json.dumps(source), 'radius' : radius, 'datos' : 'atascos'}
    return render(request, "maps.html", context)

def get_json_atascos_dentro(request, lon, lat, radius): 
    data = get_json(request,URL_ATASCOS)
    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]

    locations = []
    for x in range(data['totalFeatures']):
        locations.append(data['features'][x]['geometry'])
    points = []
    for location in locations:
        lon_aparcamiento = float(location.get('coordinates')[1])
        lat_aparcamiento = float(location.get('coordinates')[0])
        if lon_aparcamiento != 0.0 and lat_aparcamiento != 0.0 and dentro_perimetro(float(lon_aparcamiento),float(lat_aparcamiento),source,radius):
            points.append(location)
    return HttpResponse(json.dumps(points))

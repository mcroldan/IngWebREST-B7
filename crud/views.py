from os import name
from django.http.response import HttpResponse
from django.shortcuts import render
from pymongo.message import delete
from crud.utils import DBClientMongo
from IwebDjango.settings import DB_NAME, DEBUG
from crud.models import Usuario
from crud.models import Comentario
from bson.objectid import ObjectId
import ast
from django.shortcuts import redirect
from crud import templates
import urllib.request
from urllib.request import urlopen
import json

# Create your views here.

def get_all_ids_cursor(_tableName):
    atributos = {'_id'}
    if _tableName == 'Comentario':
        atributos = {'_id', 'autor'}

    bd = DBClientMongo(DB_NAME, _tableName)
    cursor = bd.find({},atributos)
    bd.close()
    return cursor

def get_all_users(request):
    """usuarios = []
    for doc in get_all_ids_cursor('Usuario'):
        usuarios.append(Usuario.crearConId(doc['_id']))
    users = []
    for user in usuarios:
        users.append(user.serialize())
    
    json = ', '.join(users)
    json = '{' + json + '}'"""
    bd = DBClientMongo(DB_NAME, 'Usuario')
    json = bd.find()
    bd.close()
    return HttpResponse(json)

def get_all_comments(request):
    """comentarios = []
    for doc in get_all_ids_cursor('Comentario'):
        comentarios.append(Comentario.crearConId(doc['_id'], Usuario.crearConId(doc['autor'])))
    comments = []
    for comment in comentarios:
        comments.append(comment.serialize())
    
    json = ', '.join(comments)
    json = '{' + json + '}'
"""
    bd = DBClientMongo(DB_NAME, 'Comentario')
    json = bd.find()
    bd.close()
    return HttpResponse(json)

def get_user(request, var):
    user = Usuario.crearConId(var)
    json = user.serialize()

    return HttpResponse(json)

def get_comment(request, var):
    comment = Comentario.crearConId(var)
    return HttpResponse(comment.serialize())

def get_user_comments(request,var):
    bd = DBClientMongo(DB_NAME, 'Comentario')
    cursor = bd.find( {'autor': ObjectId(var)})
    bd.close()
    json = []
    for doc in cursor:
        json.append(Comentario.crearConId(doc['_id']).serialize())
    return HttpResponse(json)

def create_user(request, name, surname, address):
    array = surname.split(',')
    usuario = Usuario(name, array, address) 
    response = redirect('/crud/get/users') 
    return response 

def create_comment(request, autor, comentario, fecha):
    comentario = Comentario(autor, comentario, fecha) 
    response = redirect('/crud/get/comments') 
    return response

def updt_users(request, id, attr, newAttr):
    user = Usuario.crearConId(id)

    if (attr == 'name'):
        user.setName(newAttr)
    elif (attr == 'surname'):
        array = newAttr.split(',')
        user.setSurname(array)
    elif (attr == 'address'):
        user.setAddress(newAttr)
    return HttpResponse(newAttr)

def updt_comments(request, id, attr, newAttr):
    comment = Comentario.crearConId(id)

    if (attr == 'comentario'):
        comment.setComentario(newAttr)
    return HttpResponse(comment.comentario)

def delete_user(request,id):
    user = Usuario.crearConId(id)
    user.delete()
    response = redirect('/crud/get/users')
    return response

def delete_comment(request,id):
    comment = Comentario.crearConId(id)
    comment.delete()
    response = redirect('/crud/get/comments')
    return response

def delete_all(request,id):
    if(id == 'albaricoque83'):
        bd = DBClientMongo(DB_NAME, 'Usuario')
        bd.delete()
        bd.cambiar_coleccion('Comentario')
        bd.delete()
    response = redirect('/crud/get/users')
    return response

def get_json(request):
    req = urllib.request.Request(url="https://datosabiertos.malaga.eu/recursos/aparcamientos/ocupappublicosmun/ocupappublicosmunfiware.json", headers={"User-Agent": "Mozilla/5.0"})
    handler = urllib.request.urlopen(req)
    data = json.loads(handler.read().decode())
    return data
    
def get_aparcamientos(request, lon, lat, radius): 
    #distancia entre coordenada y aparcamiento < radio
    data = get_json(request)

    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]

    locations = []
    for aparcamiento in data:
        locations.append(aparcamiento['location'])
    points = []
    for location in locations:
        if location.get('value').get('coordinates')[0] != 0.0 and location.get('value').get('coordinates')[1] != 0.0:
            points.append(location.get('value').get('coordinates'))
    context = {'points' : json.dumps(points), 'source' : json.dumps(source), 'radius' : radius}
    return render(request, "aparcamientos_radio.html", context)

def get_aparcamiento_cercano(request, lon, lat):
    data = get_json(request)
    latF = float(lat) 
    lonF = float(lon)
    source = [latF, lonF]
    locations = []
    for aparcamiento in data:
        locations.append(aparcamiento['location'])
    point = []
    for location in locations:
        print(location)
        lonP = float(location.get('value').get('coordinates')[0])
        latP = float(location.get('value').get('coordinates')[1])
        if len(point) == 0  :
            point = [lonP, latP]
        else:
            if latP != 0.0 and lonP != 0.0 and ((abs(latF - latP) + abs(lonF - lonP)) < (abs(latF - point[0]) + abs(lonF - point[1]))):
                point = [latP, lonP]
    context = {'point' : json.dumps(point), 'source' : json.dumps(source)}
    return render(request, "aparcamiento_mas_cercano.html", context)

            
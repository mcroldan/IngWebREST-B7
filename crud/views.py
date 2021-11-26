from os import name
from django.http.response import HttpResponse
from django.shortcuts import render
from crud.utils import DBClientMongo
from IwebDjango.settings import DB_NAME, DEBUG
from crud.models import Usuario
from crud.models import Comentario
from bson.objectid import ObjectId
import ast
from django.shortcuts import redirect

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
    usuario = Usuario.__init__(name, surname, address) 
    response = redirect('/crud/get/users') 
    return response 

def create_comment(request, autor, comentario, fecha):
    comentario = Comentario.__init__(autor, comentario, fecha) 
    response = redirect('/crud/get/comments') 
    return response

def updt_users(request, id, attr, newAttr):
    user = Usuario.crearConId(id)

    if (attr == 'name'):
        user.setName(newAttr)
    elif (attr == 'surname'):
        array = newAttr.split(' ')
        user.setSurname(array)
    elif (attr == 'address'):
        user.setAddress(newAttr)
    return HttpResponse(newAttr)

def updt_comments(request, id, attr, newAttr):
    comment = Comentario.crearConId(id)

    if (attr == 'comentario'):
        comment.setName(newAttr)
    return HttpResponse(comment.name)

def delete_user(request,var):
    user = Usuario.crearConId(var)
    user.delete()
    response = redirect('/crud/get/users')
    return response

def delete_comment(request,var):
    comment = Comentario.crearConId(var)
    comment.delete()
    response = redirect('/crud/get/comments')
    return response
    

def main(request):


    bd = DBClientMongo(DB_NAME, 'Usuario')
    user1 = Usuario.crearConId('619ccf0966c88532d5ed694f')
    comment1 = Comentario.crearConId('619ccf0a66c88532d5ed6954', user1)
    nombre1 = user1.surname[0]
    user1.setSurname( ['Juajua'] )
    nombre2 = user1.surname[0]
    return HttpResponse(comment1.serialize())

    """dataUsers = [
        { 'name': 'Federico', 'surname': ['Fernandez', 'Alvarez'], 'address': {'street': 'Calle La Fragua', 'number': 12, 'apartment': 311} },
        { 'name': 'Alfonso', 'surname': ['Fernandez', 'Alvarez'], 'address': {'street': 'Calle La Fragua', 'number': 12, 'apartment': 311} },
        { 'name': 'Hilda', 'surname': ['Diaz', 'De Vivar'], 'address': {'street': 'Calle La Fragua', 'number': 12, 'apartment': 312} },
        { 'name': 'Brayan', 'surname': 'Hitch', 'address': {'street': 'Avenida los Santos', 'apartment': 3} },
        { 'name': 'Jeronimo', 'address': {'street': 'Plaza la Teja', 'number': 12} }
        ]

    dataComments = []
    comments = [
        'Me ha encantado la aplicacion',
        'Menuda basura de aplicacion la verdad',
        'Me ha gustado el trayecto',
        'Grande conductor',
        'AAAAAAAAAAAAAAA'
    ]
    usuarios = []

    bd.insert(dataUsers)

    for user in dataUsers:
        usuarios.append(user['name'])

    i = 0
    for com in comments:
        id = bd.find( {'name': usuarios[i]}, { '_id' }, single=True )
        dataComments.append( {'autor': id['_id'], 'comentario': com, 'fecha': 0} )
        i = i + 1

    bd.cambiar_coleccion('Comentario')
    bd.insert(dataComments)

    personasComentarios = []
    bd.cambiar_coleccion('Usuario')
    cursorPersonas = bd.find({}, {'_id', 'name'})
    
    bd.cambiar_coleccion('Comentario')
    for doc in cursorPersonas:
        cursorComentarios = bd.find({'autor': doc['_id']}, {'comentario'})
        for docCom in cursorComentarios:
            personasComentarios.append('<pre><b> %s </b> ha escrito el comentario : <b> \"%s\" </b> \n </pre>' %
                                (doc['name'], docCom['comentario']))

    string = ''.join(personasComentarios)"""

    """bd.cambiar_coleccion('Usuario')
    bd.delete()

    bd.cambiar_coleccion('Comentario')
    bd.delete()"""

    return HttpResponse(string)
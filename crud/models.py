from crud.utils import DBClientMongo
from IwebDjango.settings import DB_NAME
from bson.objectid import ObjectId
import json

# Create your models here.

class Usuario:
    def __init__(self, _name, _surname, _address):
        self.name = _name
        self.surname = _surname
        self.address = _address
        db = DBClientMongo(DB_NAME, 'Usuario')
        db.insert( [{ 'name': self.name, 'surname': self.surname, 'address': self.address }] )
        self._id = (db.find( {'name': self.name, 'surname': self.surname, 'address': self.address}, {'_id'}, single=True ))['_id']
        db.close()

    @classmethod
    def crearConId(cls, id):
        db = DBClientMongo(DB_NAME, 'Usuario')
        doc = db.find( {'_id': ObjectId(id)}, {'name', 'surname', 'address'} , single=True)
        obj = cls.__new__(cls)
        super(Usuario, obj).__init__()
        obj._id = ObjectId(id)
        obj.name = doc['name']
        obj.surname = doc['surname']
        obj.address = doc['address']
        db.close()
        return obj

    def setName(self, _newName):
        db = DBClientMongo(DB_NAME, 'Usuario')
        self.name = _newName
        db.update( {'_id' : self._id}, { '$set': { 'name': _newName } } )
        db.close()

    def setAddress(self, **_newAddress):
        db = DBClientMongo(DB_NAME, 'Usuario')
        self.address = _newAddress
        db.update( {'_id' : self._id}, { '$set': { 'address': _newAddress } } )
        db.close()

    def setSurname(self, _newSurname):
        db = DBClientMongo(DB_NAME, 'Usuario')
        self.surname = _newSurname
        db.update( {'_id' : self._id}, { '$set': { 'surname': _newSurname } } )
        db.close()

    def delete(self):
        db = DBClientMongo(DB_NAME, 'Usuario')
        db.delete( {'_id' : self._id}, single=True)
        db.close()

    def serialize(self):
        dict = { 'name': self.name, 'surname': self.surname, 'address': self.address }
        return json.dumps(dict)

class Comentario:
    def __init__(self, _autor, _comentario, _fecha):
        """"Autor es la ID del autor en formato String"""
        self.autor = ObjectId(_autor)
        self.comentario = _comentario
        self.fecha = _fecha
        db = DBClientMongo(DB_NAME, 'Comentario')
        db.insert( [{ 'autor': self.autor, 'comentario': self.comentario, 'fecha': self.fecha }] )
        self._id = (db.find( {'autor': self.autor._id, 'comentario': self.comentario, 'fecha': self.fecha}, {'_id'}, single=True ))['_id']
        db.close()

    @classmethod
    def crearConId(cls, id):
        db = DBClientMongo(DB_NAME, 'Comentario')
        doc = db.find( {'_id': ObjectId(id)}, {'autor', 'comentario', 'fecha'} , single=True)
        obj = cls.__new__(cls)
        super(Comentario, obj).__init__()
        obj._id = ObjectId(id)
        obj.autor = doc['autor']
        obj.comentario = doc['comentario']
        obj.fecha = doc['fecha']
        db.close()
        return obj

    def setComentario(self, _newComentario):
        db = DBClientMongo(DB_NAME, 'Comentario')
        self.comentario = _newComentario
        db.update( {'_id' : self._id}, { '$set': { 'comentario': _newComentario } } )
        db.close()

    def delete(self):
        db = DBClientMongo(DB_NAME, 'Comentario')
        db.delete( {'_id' : self._id}, single=True)
        db.close()

    def serialize(self):
        dict = { 'autor': 'http://localhost:8000/crud/get/users/' + self.autor.__str__(), 'comentario': self.comentario, 'fecha': self.fecha }
        return json.dumps(dict)


    
        

    

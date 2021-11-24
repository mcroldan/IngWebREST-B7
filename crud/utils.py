from dns.resolver import query
import pymongo
import ssl
from mongosanitizer.sanitizer import sanitize
from pymongo import collection


class DBClientMongo:
    """ Clase pensada para ocultar la conexión inicial de la base de datos MongoDB y facilitar el uso de sus componentes """
    def __init__(self, _stringConexion, _coleccionInicial):
        self.cliente = pymongo.MongoClient(_stringConexion, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
        self.db = self.cliente.get_default_database()
        self.coleccion = self.db[_coleccionInicial]

    def cambiar_coleccion(self, _coleccion):
        """ Cambia la coleccion con la que estamos trabajando."""
        self.coleccion = self.db[_coleccion]


    def find(self, query=None, filter=None, single=False):
        """ Asociada una query de MongoDB, devuelve un cursor que contiene uno o todos los documentos con los atributos especificados en filter
        con el que poder trabajar. Si no se le pasa nada, devuelve todo. El atributo single controla si se quiere obtener solo un documento o todos.
        Este método controla las inyecciones NoSQL.  """
        
        if single == True:
            return self.coleccion.find_one(query, filter)
        else:
            return self.coleccion.find(query, filter)


    def insert(self, documents):
        """Inserta los elementos pasados como parametro en una lista [{}, {}] de los elementos que sean. Soporta inserción para múltiples objetos o para uno solo, con la 
        sintaxis de inserción de MongoDB.
        P. ej: 
        bd.insert([ 
        {'name': 'Jaja', 
        'surnames': ['Jo', 'Joa'], 
        'phone': '3', 
        'family': 
            {'wife': '4', 'son': '1'}} 
        ])"""
        if len(documents) == 1:
            self.coleccion.insert_one(documents[0])
        else:
            self.coleccion.insert_many(documents)

    def delete(self, filter = {}, single=False, deleteAll = False):
        """Elimina uno o varios elementos según si el atributo single sea True o False que se correspondan al filtro del otro parámetro.
        P. ej: delete( {'name': 'Alejandro'} )"""
        sanitize(filter)
        if single == True:
            self.coleccion.delete_one(filter)
        else:
            self.coleccion.delete_many(filter)

    def update(self, filter, update, single=False):
        """Modifica los documentos que cumplen con la condicion impuesta en filter con los cambios asignados en update. Si Single = True, entonces solo actualiza un documento.
        P. ej: update( {'name': 'Alejandro'}, {'$set': {'phone': '111'}} )"""
        sanitize(filter)
        if single == True:
            self.coleccion.update_one(filter, update, upsert=True)
        else:
            self.coleccion.update_many(filter, update, upsert=True)
    
    def close(self):
        self.cliente.close()

    #def load_sample_data(self):
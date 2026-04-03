from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = 'db_proyecto_final_grupos'

class MensajeEvento:
    def __init__(self, data):
        self.id = data["id"]
        self.mensaje = data["mensaje"]
        self.evento_id = data["evento_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def crear_mensaje(cls, datos):
        query = """
                INSERT INTO mensajes_evento (mensaje, evento_id) 
                VALUES (%(mensaje)s, %(evento_id)s)
        """
        return connectToMySQL(db).query_db(query, datos)

    @classmethod
    def obtener_mensajes_por_evento(cls, datos):
        query = """
                SELECT * FROM mensajes_evento
                WHERE evento_id = %(evento_id)s
                ORDER BY created_at DESC
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        mensajes = []
        if resultados:
            for mensaje in resultados:
                mensajes.append(cls(mensaje))
        return mensajes

    @classmethod
    def eliminar_mensaje(cls, datos):
        query = """
                DELETE FROM mensajes_evento WHERE id = %(id)s
        """
        return connectToMySQL(db).query_db(query, datos)

    @staticmethod
    def validar_mensaje(datos):
        es_valido = True
        if len(datos['mensaje']) < 1:
            flash('El mensaje no puede estar vacío', 'mensaje_evento')
            es_valido = False
        if len(datos['mensaje']) > 200:
            flash('El mensaje no puede tener más de 200 caracteres', 'mensaje_evento')
            es_valido = False
        return es_valido
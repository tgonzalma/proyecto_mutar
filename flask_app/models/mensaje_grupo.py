from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = 'db_proyecto_final_grupos'

class MensajeGrupo:
    def __init__(self, data):
        self.id = data["id"]
        self.mensaje = data["mensaje"]
        self.usuario_id = data["usuario_id"]
        self.grupo_id = data["grupo_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # Atributos adicionales para joins
        self.usuario_nombre = data.get("usuario_nombre")
        self.usuario_apellido = data.get("usuario_apellido")
        self.usuario_nickname = data.get("usuario_nickname")

    @classmethod
    def crear_mensaje(cls, datos):
        query = """
                INSERT INTO mensajes_grupo (mensaje, usuario_id, grupo_id) 
                VALUES (%(mensaje)s, %(usuario_id)s, %(grupo_id)s)
        """
        return connectToMySQL(db).query_db(query, datos)

    @classmethod
    def obtener_mensajes_por_grupo(cls, datos):
        query = """
                SELECT mensajes_grupo.*, usuarios.nombre as usuario_nombre, 
                usuarios.apellido as usuario_apellido, usuarios.nickname as usuario_nickname
                FROM mensajes_grupo
                LEFT JOIN usuarios ON mensajes_grupo.usuario_id = usuarios.id
                WHERE mensajes_grupo.grupo_id = %(grupo_id)s
                ORDER BY mensajes_grupo.created_at DESC
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
                DELETE FROM mensajes_grupo WHERE id = %(id)s AND usuario_id = %(usuario_id)s
        """
        return connectToMySQL(db).query_db(query, datos)

    @staticmethod
    def validar_mensaje(datos):
        es_valido = True
        if len(datos['mensaje']) < 1:
            flash('El mensaje no puede estar vacío', 'mensaje_grupo')
            es_valido = False
        if len(datos['mensaje']) > 200:
            flash('El mensaje no puede tener más de 200 caracteres', 'mensaje_grupo')
            es_valido = False
        return es_valido
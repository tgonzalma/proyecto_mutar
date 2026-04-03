from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt

db = 'db_proyecto_final_grupos'

class GrupoUsuario:
    def __init__(self, data):
        self.usuario_id = data["usuario_id"]
        self.grupo_id = data["grupo_id"]
        self.created_at = data["created_at"]
    
    @classmethod
    def agregar_usuario_a_grupo(cls, datos):
        query = """
                INSERT INTO grupos_usuarios (usuario_id, grupo_id, created_at)
                VALUES (%(usuario_id)s, %(grupo_id)s, NOW())
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def eliminar_usuario_de_grupo(cls, datos):
        query = """
                DELETE FROM grupos_usuarios 
                WHERE usuario_id = %(usuario_id)s 
                AND grupo_id = %(grupo_id)s
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def obtener_usuarios_por_grupo(cls, datos):
        query = """
                SELECT usuarios.* FROM usuarios
                JOIN grupos_usuarios ON usuarios.id = grupos_usuarios.usuario_id
                WHERE grupos_usuarios.grupo_id = %(grupo_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        usuarios = []
        for usuario in resultados:
            usuarios.append(usuario)
        return usuarios
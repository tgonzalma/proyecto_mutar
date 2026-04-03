from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt

db = 'db_proyecto_final_grupos'


class FavoritoUsuario:
    def __init__(self, data):
        self.usuario_id = data["usuario_id"]
        self.evento_id = data["evento_id"]
        self.created_at = data["created_at"]
    
    @classmethod
    def agregar_favorito(cls, datos):
        query = """
                INSERT INTO favoritos_usuario (usuario_id, evento_id, created_at)
                VALUES (%(usuario_id)s, %(evento_id)s, NOW())
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def eliminar_favorito(cls, datos):
        query = """
                DELETE FROM favoritos_usuario 
                WHERE usuario_id = %(usuario_id)s 
                AND evento_id = %(evento_id)s
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def obtener_favoritos_por_usuario(cls, datos):
        query = """
                SELECT eventos.* FROM eventos
                JOIN favoritos_usuario ON eventos.id = favoritos_usuario.evento_id
                WHERE favoritos_usuario.usuario_id = %(usuario_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        favoritos = []
        for favorito in resultados:
            favoritos.append(favorito)
        return favoritos
    
    # Verificar si un evento es favorito
    @classmethod
    def es_favorito(cls, datos):
        query = """
                SELECT * FROM favoritos_usuario 
                WHERE usuario_id = %(usuario_id)s 
                AND evento_id = %(evento_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        return len(resultados) > 0
    
    @classmethod
    def contar_favoritos(cls, datos):
        query = """
                SELECT COUNT(*) AS total_favoritos FROM favoritos_usuario 
                WHERE evento_id = %(evento_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        return resultados[0]['total_favoritos']
    
    #Obtener todos los usuarios que han marcado un evento como favorito
    @classmethod
    def obtener_usuarios_favoritos_por_evento(cls, datos):
        query = """
                SELECT usuarios.* FROM usuarios
                JOIN favoritos_usuario ON usuarios.id = favoritos_usuario.usuario_id
                WHERE favoritos_usuario.evento_id = %(evento_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        usuarios = []
        for usuario in resultados:
            usuarios.append(usuario)
        return usuarios
    
    @classmethod
    def get_favorito_by_evento_and_usuario(cls, datos):
        query = """
            SELECT * FROM favoritos_usuario
            WHERE usuario_id = %(usuario_id)s AND evento_id = %(evento_id)s
            LIMIT 1
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        if resultados:
            return resultados[0]  # Devuelve el diccionario de la fila
        return None
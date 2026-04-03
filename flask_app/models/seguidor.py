from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = 'db_proyecto_final_grupos'

class Seguidor:
    def __init__(self, data):
        self.usuario_seguidor_id = data["usuario_seguidor_id"]
        self.usuario_seguido_id = data["usuario_seguido_id"]
        self.created_at = data["created_at"]
    
    @classmethod
    def seguir(cls, datos):
        # """Crear una relación de seguidor (un usuario sigue a otro)"""
        query = """
                INSERT INTO seguidores (usuario_seguidor_id, usuario_seguido_id, created_at)
                VALUES (%(usuario_seguidor_id)s, %(usuario_seguido_id)s, NOW())
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def dejar_de_seguir(cls, datos):
        # """Eliminar una relación de seguidor"""
        query = """
                DELETE FROM seguidores 
                WHERE usuario_seguidor_id = %(usuario_seguidor_id)s 
                AND usuario_seguido_id = %(usuario_seguido_id)s
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def obtener_seguidores(cls, datos):
        # """Obtener todos los usuarios que siguen a un usuario específico"""
        query = """
                SELECT usuarios.* FROM usuarios
                JOIN seguidores ON usuarios.id = seguidores.usuario_seguidor_id
                WHERE seguidores.usuario_seguido_id = %(usuario_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        seguidores = []
        for seguidor in resultados:
            seguidores.append(seguidor)
        return seguidores
    
    @classmethod
    def obtener_seguidos(cls, datos):
        # """Obtener todos los usuarios a los que sigue un usuario específico"""
        query = """
                SELECT usuarios.* FROM usuarios
                JOIN seguidores ON usuarios.id = seguidores.usuario_seguido_id
                WHERE seguidores.usuario_seguidor_id = %(usuario_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        seguidos = []
        for seguido in resultados:
            seguidos.append(seguido)
        return seguidos
    
    @classmethod
    def contar_seguidores(cls, datos):
        # """Contar cuántos seguidores tiene un usuario"""
        query = """
                SELECT COUNT(*) AS total_seguidores FROM seguidores
                WHERE usuario_seguido_id = %(usuario_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        return resultados[0]['total_seguidores']
    
    @classmethod
    def contar_seguidos(cls, datos):
        query = """
                SELECT COUNT(*) AS total_seguidos FROM seguidores
                WHERE usuario_seguidor_id = %(usuario_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        return resultados[0]['total_seguidos']
    
    @classmethod
    def esta_siguiendo(cls, datos):
        query = """
                SELECT * FROM seguidores
                WHERE usuario_seguidor_id = %(usuario_seguidor_id)s 
                AND usuario_seguido_id = %(usuario_seguido_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        return len(resultados) > 0
    
    @classmethod
    def obtener_eventos_de_seguidos(cls, datos):
        query = """
                SELECT eventos.* FROM eventos
                JOIN seguidores ON eventos.usuario_creador_id = seguidores.usuario_seguido_id
                WHERE seguidores.usuario_seguidor_id = %(usuario_id)s
                AND eventos.visibilidad = 'seguidores'
                ORDER BY eventos.created_at DESC
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        eventos = []
        for evento in resultados:
            eventos.append(evento)
        return eventos
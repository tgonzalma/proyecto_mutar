from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt

db = 'db_proyecto_final_grupos'

class FavoritoGrupo:
    def __init__(self, data):
        self.id = data.get("id")
        self.favorito_id = data.get("favorito_id")
        self.grupo_id = data.get("grupo_id")
        self.created_at = data.get("created_at")

    @classmethod
    def agregar_favorito_a_grupo(cls, datos):
        query = """
            INSERT INTO favoritos_grupo (favorito_id, grupo_id, created_at)
            VALUES (%(favorito_id)s, %(grupo_id)s, NOW())
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def obtener_eventos_favoritos_por_grupo(cls, datos):
        query = """
            SELECT eventos.* FROM eventos
            JOIN favoritos_usuario ON eventos.id = favoritos_usuario.evento_id
            JOIN favoritos_grupo ON favoritos_usuario.id = favoritos_grupo.favorito_id
            WHERE favoritos_grupo.grupo_id = %(grupo_id)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        if not resultados:
            return []
        return resultados
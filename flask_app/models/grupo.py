from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt

db = 'db_proyecto_final_grupos'

class Grupo:
    def __init__(self,data):
        self.id=data["id"]
        self.nombre=data["nombre"]
        self.descripcion=data["descripcion"]
        self.foto_portada=data.get("foto_portada")
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.creador_grupo_id=data["creador_grupo_id"]

    @classmethod
    def save(cls, datos):
        query= """
                INSERT INTO grupos (nombre, descripcion, foto_portada, creador_grupo_id) VALUES ( %(nombre)s, %(descripcion)s, %(foto_portada)s, %(creador_grupo_id)s)
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def get_all(cls):
        query= """
                SELECT * FROM grupos;
        """
        resultados = connectToMySQL(db).query_db(query)
        grupos = []
        for grupo in resultados:
            grupos.append( cls(grupo) )
        return grupos
    
    @classmethod
    def get_by_id(cls, datos):
        query= """
                SELECT * FROM grupos WHERE id = %(id)s
            """
        resultados = connectToMySQL(db).query_db(query, datos)
        return cls(resultados[0])
    
    @staticmethod
    def validar_grupo(datos):
        es_valido = True
        if len(datos['nombre']) < 3:  # Validar que el nombre tenga al menos 3 caracteres
            flash('El nombre del grupo debe tener al menos 3 caracteres', 'grupo')
            es_valido = False
        if len(datos['descripcion']) < 10: # Validar que la descripción tenga al menos 10 caracteres
            flash('La descripción del grupo debe tener al menos 10 caracteres', 'grupo')
            es_valido = False
        return es_valido
    
    @staticmethod
    def validar_actualizacion_grupo(datos):
        es_valido = True
        if len(datos['nombre']) < 3:  # Validar que el nombre tenga al menos 3 caracteres
            flash('El nombre del grupo debe tener al menos 3 caracteres', 'actualizar_grupo')
            es_valido = False
        if len(datos['descripcion']) < 10: # Validar que la descripción tenga al menos 10 caracteres
            flash('La descripción del grupo debe tener al menos 10 caracteres', 'actualizar_grupo')
            es_valido = False
        return es_valido

    @classmethod
    def actualizar_grupo(cls, datos):
        query= """
                UPDATE grupos 
                SET nombre = %(nombre)s, descripcion = %(descripcion)s
                WHERE id = %(id)s
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def eliminar_grupo(cls, datos):
        query= """
                DELETE FROM grupos WHERE id = %(id)s
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def buscar(cls, termino):
        query= """
                SELECT * FROM grupos WHERE nombre LIKE %(termino)s OR descripcion LIKE %(termino)s;
        """
        datos = {'termino': f'%{termino}%'}
        resultados = connectToMySQL(db).query_db(query, datos)
        grupos = []
        for grupo in resultados:
            grupos.append( cls(grupo) )
        return grupos
    
    @classmethod
    def obtener_eventos_por_grupo(cls, datos):
        query= """
                SELECT eventos.* FROM eventos
                WHERE eventos.grupo_creador_id = %(grupo_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        eventos = []
        for evento in resultados:
            eventos.append( evento )
        return eventos
    
    @classmethod
    def obtener_miembros_por_grupo(cls, datos):
        query= """
                SELECT usuarios.* FROM usuarios
                JOIN grupos_usuarios ON usuarios.id = grupos_usuarios.usuario_id
                WHERE grupos_usuarios.grupo_id = %(grupo_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        miembros = []
        for miembro in resultados:
            miembros.append( miembro )
        return miembros
    
    @classmethod
    def contar_miembros(cls, datos):
        query= """
                SELECT COUNT(*) AS total_miembros FROM grupos_usuarios
                WHERE grupo_id = %(grupo_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        return resultados[0]['total_miembros']
    
    @classmethod
    def contar_eventos(cls, datos):
        query= """
                SELECT COUNT(*) AS total_eventos FROM favoritos_grupo
                WHERE grupo_id = %(grupo_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        if resultados:
            return resultados[0]['total_eventos']
        return 0
    
    @classmethod
    def obtener_grupos_por_usuario(cls, datos):
        query= """
                SELECT grupos.* FROM grupos
                JOIN grupos_usuarios ON grupos.id = grupos_usuarios.grupo_id
                WHERE grupos_usuarios.usuario_id = %(usuario_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        grupos = []
        for grupo in resultados:
            grupos.append( cls(grupo) )
        return grupos
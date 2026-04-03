from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt

db = 'db_proyecto_final_grupos'

class Evento:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.fecha_evento = data["fecha_evento"]
        self.ubicacion = data["ubicacion"]
        self.ciudad = data["ciudad"]
        self.latitud = data.get("latitud")           # Puede ser NULL
        self.longitud = data.get("longitud")         # Puede ser NULL
        self.descripcion = data["descripcion"]
        self.tipo = data["tipo"]
        self.visibilidad = data["visibilidad"]
        self.estado = data["estado"]
        self.foto_portada = data.get("foto_portada")  
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuario_creador_id = data.get("usuario_creador_id")   # Puede ser NULL
        self.grupo_creador_id = data.get("grupo_creador_id")       # Puede ser NULL

    @classmethod
    def save(cls, datos):
        query= """
                INSERT INTO eventos (nombre, fecha_evento, ubicacion, ciudad, latitud, longitud, descripcion, tipo, visibilidad, estado, foto_portada, usuario_creador_id, grupo_creador_id) 
                VALUES ( %(nombre)s, %(fecha_evento)s, %(ubicacion)s, %(ciudad)s, %(latitud)s, %(longitud)s, %(descripcion)s, %(tipo)s, %(visibilidad)s, %(estado)s, %(foto_portada)s, %(usuario_creador_id)s, %(grupo_creador_id)s)
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def get_all(cls):
        query= """
                SELECT * FROM eventos;
        """
        resultados = connectToMySQL(db).query_db(query)
        eventos = []
        for evento in resultados:
            eventos.append( cls(evento) )
        return eventos
    
    @classmethod
    def get_random_eventos(cls, cantidad):
        query= """
                SELECT * FROM eventos 
                WHERE estado = 'act'
                ORDER BY RAND() 
                LIMIT %(cantidad)s
        """
        resultados = connectToMySQL(db).query_db(query, {'cantidad': cantidad})
        eventos = []
        if resultados:
            for evento in resultados:
                eventos.append(cls(evento))
        return eventos
    
    @classmethod
    def get_by_id(cls, datos):
        query= """
                SELECT * FROM eventos WHERE id = %(id)s
            """
        resultados = connectToMySQL(db).query_db(query, datos)
        return cls(resultados[0])
    
    @classmethod
    def actualizar_evento(cls, datos):
        query= """
                UPDATE eventos 
                SET nombre=%(nombre)s, fecha_evento=%(fecha_evento)s, ubicacion=%(ubicacion)s, ciudad=%(ciudad)s, latitud=%(latitud)s, longitud=%(longitud)s, descripcion=%(descripcion)s, tipo=%(tipo)s, visibilidad=%(visibilidad)s, estado=%(estado)s, foto_portada=%(foto_portada)s
                WHERE id = %(id)s
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def obtener_eventos_por_grupo(cls, datos):
        query= """
                SELECT eventos.* FROM eventos
                WHERE eventos.grupo_creador_id = %(grupo_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        eventos = []
        for evento in resultados:
            eventos.append( cls(evento) )
        return eventos
    
    @classmethod
    def eliminar_evento(cls, datos):
        query= """
                DELETE FROM eventos WHERE id = %(id)s
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def obtener_eventos_por_usuario(cls, datos):
        query= """
                SELECT eventos.* FROM eventos
                WHERE eventos.usuario_creador_id = %(usuario_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        eventos = []
        for evento in resultados:
            eventos.append( cls(evento) )
        return eventos
    
    @classmethod
    def buscar(cls, termino):
        query= """
                SELECT * FROM eventos WHERE nombre LIKE %(termino)s OR descripcion LIKE %(termino)s;
        """
        datos = {'termino': f'%{termino}%'}
        resultados = connectToMySQL(db).query_db(query, datos)
        eventos = []
        for evento in resultados:
            eventos.append( cls(evento) )
        return eventos
    
    @classmethod
    def obtener_eventos_favoritos_por_usuario(cls, datos):
        query= """
                SELECT eventos.* FROM eventos
                JOIN favoritos_eventos ON eventos.id = favoritos_eventos.evento_id
                WHERE favoritos_eventos.usuario_id = %(usuario_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        eventos = []
        for evento in resultados:
            eventos.append( cls(evento) )
        return eventos
    
    @classmethod
    def contar_favoritos(cls, datos):
        query= """
                SELECT COUNT(*) AS total_favoritos FROM favoritos_usuario
                WHERE evento_id = %(evento_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        return resultados[0]['total_favoritos']
    
    # @classmethod
    # def contar_asistentes(cls, datos):
    #     query= """
    #             SELECT COUNT(*) AS total_asistentes FROM asistentes_eventos
    #             WHERE evento_id = %(evento_id)s;
    #     """
    #     resultados = connectToMySQL(db).query_db(query, datos)
    #     return resultados[0]['total_asistentes']
    
    @classmethod
    def es_favorito_usuario(cls, datos):
        query= """
                SELECT * FROM favoritos_usuario
                WHERE usuario_id = %(usuario_id)s AND evento_id = %(evento_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        return len(resultados) > 0  # Devuelve True si es favorito, False si no lo es
    
    @classmethod
    def es_favorito_grupo(cls, datos):
        query= """
                SELECT * FROM favoritos_grupo
                JOIN favoritos_usuario ON favoritos_grupo.favorito_id = favoritos_usuario.id
                WHERE favoritos_grupo.grupo_id = %(grupo_id)s AND favoritos_usuario.evento_id = %(evento_id)s;
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        return len(resultados) > 0  # Devuelve True si es favorito, False si no lo es

    @classmethod
    def obtener_eventos_de_seguidores(cls, datos):
        """Obtener eventos creados por los seguidores del usuario (personas que me siguen)"""
        query = """
                SELECT eventos.* FROM eventos
                JOIN seguidores ON eventos.usuario_creador_id = seguidores.usuario_seguidor_id
                WHERE seguidores.usuario_seguido_id = %(usuario_id)s
                ORDER BY eventos.created_at DESC
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        eventos = []
        for evento in resultados:
            eventos.append(cls(evento))
        return eventos
    
    @classmethod
    def obtener_eventos_de_seguidos(cls, datos):
        """Obtener eventos creados por los seguidos del usuario (personas que sigo)"""
        query = """
                SELECT eventos.* FROM eventos
                JOIN seguidores ON eventos.usuario_creador_id = seguidores.usuario_seguido_id
                WHERE seguidores.usuario_seguidor_id = %(usuario_id)s
                ORDER BY eventos.created_at DESC
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        eventos = []
        for evento in resultados:
            eventos.append(cls(evento))
        return eventos

    @staticmethod
    def validar_evento(datos):
        es_valido = True
        if len(datos['nombre']) < 3:  # Validar que el nombre tenga al menos 3 caracteres
            flash('El nombre del evento debe tener al menos 3 caracteres', 'evento')
            es_valido = False
        if len(datos['descripcion']) < 10: # Validar que la descripción tenga al menos 10 caracteres
            flash('La descripción del evento debe tener al menos 10 caracteres', 'evento')
            es_valido = False
        return es_valido
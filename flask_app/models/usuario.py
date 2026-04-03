from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
db = 'db_proyecto_final_grupos'

class Usuario:
    def __init__(self,data):
        self.id=data["id"]
        self.nombre=data["nombre"]
        self.apellido=data["apellido"]
        self.email=data["email"]
        self.password=data["password"]
        self.nickname=data.get("nickname")
        self.foto_perfil=data.get("foto_perfil")
        self.descripcion=data.get("descripcion")
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]

    @classmethod
    def save(cls, datos):
        query= """
                INSERT INTO usuarios (nombre, apellido, email, password) VALUES ( %(nombre)s, %(apellido)s, %(email)s, %(password)s)
        """
        return connectToMySQL(db).query_db(query, datos)
    
    @classmethod
    def get_by_email( cls, datos):
        query= """
                SELECT * FROM usuarios where email = %(email)s
        """
        resultados = connectToMySQL(db).query_db(query, datos)
        if len(resultados) <1:
            return False
        return cls(resultados[0])
    
    @classmethod
    def get_by_id(cls, datos):
        query= """
                SELECT * FROM usuarios WHERE id = %(id)s
            """
        resultados = connectToMySQL(db).query_db(query, datos)
        return cls(resultados[0])
    
    @classmethod
    def buscar_por_email_o_nombre(cls, termino):
        query = """
                SELECT * FROM usuarios 
                WHERE LOWER(email) LIKE LOWER(%(termino)s)
                OR LOWER(nombre) LIKE LOWER(%(termino)s)
                OR LOWER(apellido) LIKE LOWER(%(termino)s)
        """
        datos = {'termino': f'%{termino}%'}
        resultados = connectToMySQL(db).query_db(query, datos)
        if not resultados:
            return []
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios
    
    @classmethod
    def actualizar_perfil(cls, datos):
        if 'password' in datos and datos['password']:
            query = """
                    UPDATE usuarios 
                    SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s, nickname=%(nickname)s, foto_perfil=%(foto_perfil)s, descripcion=%(descripcion)s, password=%(password)s
                    WHERE id = %(id)s
            """
        else:
            query = """
                    UPDATE usuarios 
                    SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s, nickname=%(nickname)s, foto_perfil=%(foto_perfil)s, descripcion=%(descripcion)s
                    WHERE id = %(id)s
            """
        return connectToMySQL(db).query_db(query, datos)
    
    @staticmethod
    def validar_registro(datos):
        es_valido = True
        if len(datos['nombre']) < 2:  # Validar que el nombre tenga al menos 2 caracteres
            flash('El nombre debe tener al menos 2 caracteres', 'registro')
            es_valido = False
        if len(datos['apellido']) < 2: # Validar que el apellido tenga al menos 2 caracteres
            flash('El apellido debe tener al menos 2 caracteres', 'registro')
            es_valido = False
        if not EMAIL_REGEX.match(datos['email']): # Validar el formato del email
            flash('Formato de email inválido', 'registro')
            es_valido = False
        if Usuario.get_by_email({'email': datos['email']}): # Verificar si el email ya está registrado
            flash('El email ya se encuentra registrado', 'registro')
            es_valido = False
        if datos['password'] != datos['confirmacion']: # Validar que las contraseñas coincidan
            flash('Las contraseñas no coinciden', 'registro')
            es_valido = False
        if len(datos['password']) < 8: #EXTRA: Validar que la contraseña tenga al menos 8 caracteres
            flash('La contraseña debe tener al menos 8 caracteres', 'registro')
            es_valido = False
        return es_valido

    @staticmethod
    def validar_login(datos):
        usuario = Usuario.get_by_email({'email': datos['email']}) # Validar si el email existe en la base de datos
        if not usuario:
            flash('Email no registrado', 'login')
            return False
        if not bcrypt.check_password_hash(usuario.password, datos['password']): # Validar la contraseña
            flash('Contraseña incorrecta', 'login')
            return False
        return usuario
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app.models.evento import Evento
from flask_app.models.grupo import Grupo
from flask_app.models.grupo_usuario import GrupoUsuario
from flask_app.models.favorito_grupo import FavoritoGrupo
from flask_app.models.mensaje_grupo import MensajeGrupo
from flask_app import bcrypt

@app.route('/mis_grupos')
def mis_grupos():
    if 'usuario_id' not in session:
        return redirect('/')
    datos_usuario = {
        'id': session['usuario_id']
    }
    usuario = Usuario.get_by_id(datos_usuario)
    datos_grupos = {
        'usuario_id': session['usuario_id']
    }
    grupos_usuario = Grupo.obtener_grupos_por_usuario(datos_grupos)
    
    # Contador de miembros y eventos para cada grupo
    for grupo in grupos_usuario:
        grupo.total_miembros = Grupo.contar_miembros({'grupo_id': grupo.id})
        grupo.total_eventos = Grupo.contar_eventos({'grupo_id': grupo.id})
    
    return render_template('mis_grupos.html', usuario=usuario, grupos=grupos_usuario)

@app.route('/crear_grupo')
def crear_grupo():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('crear_grupo.html')

@app.route('/formulario_grupo', methods=['POST'])
def formulario_grupo():
    if 'usuario_id' not in session:
        return redirect('/')
    
    # Manejar la imagen de portada - IA
    foto_portada = None
    if 'foto_portada' in request.files:
        file = request.files['foto_portada']
        if file and file.filename != '':
            import os
            from werkzeug.utils import secure_filename
            
            # Crear directorio si no existe
            upload_folder = 'flask_app/static/img/grupos'
            os.makedirs(upload_folder, exist_ok=True)
            
            # Generar nombre único para el archivo
            filename = secure_filename(file.filename)
            timestamp = str(int(__import__('time').time()))
            foto_portada = f"{timestamp}_{filename}"
            file.save(os.path.join(upload_folder, foto_portada))
    
    datos_grupo = {
        "nombre": request.form['nombre'],
        "descripcion": request.form['descripcion'],
        "foto_portada": foto_portada,
        "creador_grupo_id": session['usuario_id']
    }
    grupo_id = Grupo.save(datos_grupo)
    # Agregar automáticamente al creador como miembro del grupo
    datos_miembro = {
        'usuario_id': session['usuario_id'],
        'grupo_id': grupo_id
    }
    GrupoUsuario.agregar_usuario_a_grupo(datos_miembro)
    return redirect('/mis_grupos')

@app.route('/salir_grupo/<int:grupo_id>')
def salir_grupo(grupo_id):
    if 'usuario_id' not in session:
        return redirect('/')
    datos_miembro = {
        'usuario_id': session['usuario_id'],
        'grupo_id': grupo_id
    }
    GrupoUsuario.eliminar_usuario_de_grupo(datos_miembro)
    return redirect('/mis_grupos')


@app.route('/editar_grupo/<int:grupo_id>')
def editar_grupo(grupo_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    grupo = Grupo.get_by_id({'id': grupo_id})
    if not grupo:
        return redirect('/mis_grupos')
    
    # Verificar que el usuario sea el creador del grupo
    if grupo.creador_grupo_id != session['usuario_id']:
        flash('No tienes permiso para editar este grupo', 'grupo')
        return redirect('/mis_grupos')
    
    return render_template('editar_grupo.html', grupo=grupo)

@app.route('/actualizar_grupo/<int:grupo_id>', methods=['POST'])
def actualizar_grupo(grupo_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    grupo = Grupo.get_by_id({'id': grupo_id})
    if not grupo:
        return redirect('/mis_grupos')
    
    # Verificar que el usuario sea el creador
    if grupo.creador_grupo_id != session['usuario_id']:
        flash('No tienes permiso para editar este grupo', 'grupo')
        return redirect('/mis_grupos')
    
    # Manejar la imagen de portada (si se actualiza) - IA
    foto_portada = grupo.foto_portada  # Mantener la imagen actual por defecto
    if 'foto_portada' in request.files:
        file = request.files['foto_portada']
        if file and file.filename != '':
            import os
            from werkzeug.utils import secure_filename
            
            upload_folder = 'flask_app/static/img/grupos'
            os.makedirs(upload_folder, exist_ok=True)
            
            filename = secure_filename(file.filename)
            timestamp = str(int(__import__('time').time()))
            foto_portada = f"{timestamp}_{filename}"
            file.save(os.path.join(upload_folder, foto_portada))
    
    datos_actualizar = {
        "id": grupo_id,
        "nombre": request.form['nombre'],
        "descripcion": request.form['descripcion']
    }
    
    Grupo.actualizar_grupo(datos_actualizar)
    
    # Actualizar la foto si cambió
    if foto_portada != grupo.foto_portada:
        datos_foto = {
            "id": grupo_id,
            "foto_portada": foto_portada
        }
        from flask_app.config.mysqlconnection import connectToMySQL
        query = "UPDATE grupos SET foto_portada = %(foto_portada)s WHERE id = %(id)s"
        connectToMySQL('db_proyecto_final_grupos').query_db(query, datos_foto)
    
    flash('Grupo actualizado exitosamente', 'grupo')
    return redirect(f'/perfil_grupo/{grupo_id}')


@app.route('/perfil_grupo/<int:grupo_id>')
def perfil_grupo(grupo_id):
    if 'usuario_id' not in session:
        return redirect('/')
    # Obtener información del grupo
    datos_grupo = {
        'id': grupo_id
    }
    grupo = Grupo.get_by_id(datos_grupo)
    # Obtener el creador del grupo
    datos_creador = {
        'id': grupo.creador_grupo_id
    }
    creador = Usuario.get_by_id(datos_creador)
    # Obtener los miembros del grupo
    datos_miembros = {
        'grupo_id': grupo_id
    }
    miembros = GrupoUsuario.obtener_usuarios_por_grupo(datos_miembros)
    # Obtener los eventos creados por el grupo
    eventos_creados = Evento.obtener_eventos_por_grupo({'grupo_id': grupo_id})
    # Obtener los eventos favoritos del grupo
    eventos_favoritos = FavoritoGrupo.obtener_eventos_favoritos_por_grupo({'grupo_id': grupo_id})
    # Contar miembros y eventos
    total_miembros = Grupo.contar_miembros(datos_miembros)
    total_eventos = Grupo.contar_eventos(datos_miembros)
    # Obtener mensajes del grupo
    mensajes = MensajeGrupo.obtener_mensajes_por_grupo({'grupo_id': grupo_id})
    # Verificar si el usuario actual es miembro del grupo
    es_miembro = any(miembro['id'] == session['usuario_id'] for miembro in miembros)
    return render_template(
        'perfil_grupo.html',grupo=grupo,creador=creador,miembros=miembros,eventos_creados=eventos_creados,eventos_favoritos=eventos_favoritos,total_miembros=total_miembros,total_eventos=total_eventos,mensajes=mensajes,es_miembro=es_miembro)

@app.route('/crear_mensaje_grupo/<int:grupo_id>', methods=['POST'])
def crear_mensaje_grupo(grupo_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    datos_mensaje = {
        'mensaje': request.form['mensaje'],
        'usuario_id': session['usuario_id'],
        'grupo_id': grupo_id
    }
    
    if not MensajeGrupo.validar_mensaje(datos_mensaje):
        return redirect(f'/perfil_grupo/{grupo_id}')
    
    MensajeGrupo.crear_mensaje(datos_mensaje)
    return redirect(f'/perfil_grupo/{grupo_id}')

@app.route('/eliminar_mensaje_grupo/<int:mensaje_id>/<int:grupo_id>')
def eliminar_mensaje_grupo(mensaje_id, grupo_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    datos_mensaje = {
        'id': mensaje_id,
        'usuario_id': session['usuario_id']
    }
    MensajeGrupo.eliminar_mensaje(datos_mensaje)
    return redirect(f'/perfil_grupo/{grupo_id}')
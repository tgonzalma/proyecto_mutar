from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.grupo import Grupo
from flask_app.models.mensaje_evento import MensajeEvento

@app.route('/crear_evento')
def crear_evento():
    if 'usuario_id' not in session:
        return redirect('/')
    mis_grupos = Grupo.obtener_grupos_por_usuario({'usuario_id': session['usuario_id']})
    return render_template('crear_evento.html', mis_grupos=mis_grupos)

@app.route('/formulario_evento', methods=['POST'])
def formulario_evento():
    if 'usuario_id' not in session:
        return redirect('/')
    
    # Manejar la imagen de portada - USO IA
    foto_portada = None
    if 'foto_portada' in request.files:
        file = request.files['foto_portada']
        if file and file.filename != '':
            import os
            from werkzeug.utils import secure_filename
            
            # Crear directorio si no existe
            upload_folder = 'flask_app/static/img/eventos'
            os.makedirs(upload_folder, exist_ok=True)
            
            # Generar nombre único para el archivo
            filename = secure_filename(file.filename)
            timestamp = str(int(__import__('time').time()))
            foto_portada = f"{timestamp}_{filename}"
            file.save(os.path.join(upload_folder, foto_portada))
    
    datos_evento = {
        "nombre": request.form['nombre'],
        "fecha_evento": request.form['fecha_evento'],
        "ubicacion": request.form['ubicacion'],
        "ciudad": request.form['ciudad'],
        "latitud": request.form['latitud'] or None,
        "longitud": request.form['longitud'] or None,
        "descripcion": request.form['descripcion'],
        "tipo": request.form['tipo'],
        "visibilidad": request.form['visibilidad'],
        "estado": request.form['estado'],
        "foto_portada": foto_portada,
        "usuario_creador_id": session['usuario_id'],
        "grupo_creador_id": request.form.get('grupo_creador_id') or None
    }
    from flask_app.models.evento import Evento
    Evento.save(datos_evento)
    return redirect('/mis_eventos')

@app.route('/mis_eventos')
def mis_eventos():
    if 'usuario_id' not in session:
        return redirect('/')
    from flask_app.models.evento import Evento
    datos_usuario = {
        "usuario_id": session['usuario_id']
    }
    eventos_usuario = Evento.obtener_eventos_por_usuario(datos_usuario)
    mis_grupos = Grupo.obtener_grupos_por_usuario({'usuario_id': session['usuario_id']})
    return render_template('mis_eventos.html', eventos_usuario=eventos_usuario, mis_grupos=mis_grupos)

@app.route('/eliminar_evento/<int:evento_id>')
def eliminar_evento(evento_id):
    if 'usuario_id' not in session:
        return redirect('/')
    from flask_app.models.evento import Evento
    datos_evento = {
        "id": evento_id,
        "usuario_id": session['usuario_id']
    }
    Evento.eliminar_evento(datos_evento)
    return redirect('/mis_eventos')

@app.route('/ver_evento/<int:evento_id>')
def ver_evento(evento_id):
    if 'usuario_id' not in session:
        return redirect('/')
    from flask_app.models.evento import Evento
    from flask_app.models.usuario import Usuario
    
    evento = Evento.get_by_id({'id': evento_id})
    if not evento:
        return redirect('/home')
    
    # Obtener información del creador
    if evento.usuario_creador_id:
        usuario = Usuario.get_by_id({'id': evento.usuario_creador_id})
        evento.creador_nombre = f"{usuario.nombre} {usuario.apellido}"
    elif evento.grupo_creador_id:
        grupo = Grupo.get_by_id({'id': evento.grupo_creador_id})
        evento.creador_nombre = f"Grupo: {grupo.nombre}"
    else:
        evento.creador_nombre = "Desconocido"
    
    # Obtener mensajes del evento
    mensajes = MensajeEvento.obtener_mensajes_por_evento({'evento_id': evento_id})
    
    # Verificar si el usuario actual es el creador
    es_creador = evento.usuario_creador_id == session['usuario_id']
    
    return render_template('evento.html', evento=evento, mensajes=mensajes, es_creador=es_creador)

@app.route('/editar_evento/<int:evento_id>')
def editar_evento(evento_id):
    if 'usuario_id' not in session:
        return redirect('/')
    from flask_app.models.evento import Evento
    
    evento = Evento.get_by_id({'id': evento_id})
    if not evento:
        return redirect('/mis_eventos')
    
    # Verificar que el usuario sea el creador del evento
    if evento.usuario_creador_id != session['usuario_id']:
        flash('No tienes permiso para editar este evento', 'evento')
        return redirect('/mis_eventos')
    
    return render_template('editar_evento.html', evento=evento)

@app.route('/actualizar_evento/<int:evento_id>', methods=['POST'])
def actualizar_evento(evento_id):
    if 'usuario_id' not in session:
        return redirect('/')
    from flask_app.models.evento import Evento
    
    evento = Evento.get_by_id({'id': evento_id})
    if not evento:
        return redirect('/mis_eventos')
    
    # Verificar que el usuario sea el creador
    if evento.usuario_creador_id != session['usuario_id']:
        flash('No tienes permiso para editar este evento', 'evento')
        return redirect('/mis_eventos')
    
    # Manejar la imagen de portada (si se sube una nueva)
    foto_portada = evento.foto_portada  # Mantener la imagen actual por defecto
    if 'foto_portada' in request.files:
        file = request.files['foto_portada']
        if file and file.filename != '':
            import os
            from werkzeug.utils import secure_filename
            
            upload_folder = 'flask_app/static/img/eventos'
            os.makedirs(upload_folder, exist_ok=True)
            
            filename = secure_filename(file.filename)
            timestamp = str(int(__import__('time').time()))
            foto_portada = f"{timestamp}_{filename}"
            file.save(os.path.join(upload_folder, foto_portada))
    
    datos_actualizar = {
        "id": evento_id,
        "nombre": request.form['nombre'],
        "fecha_evento": request.form['fecha_evento'],
        "ubicacion": request.form['ubicacion'],
        "ciudad": request.form['ciudad'],
        "latitud": request.form['latitud'] or None,
        "longitud": request.form['longitud'] or None,
        "descripcion": request.form['descripcion'],
        "tipo": request.form['tipo'],
        "visibilidad": request.form['visibilidad'],
        "estado": request.form['estado'],
        "foto_portada": foto_portada
    }
    
    Evento.actualizar_evento(datos_actualizar)
    flash('Evento actualizado exitosamente', 'evento')
    return redirect(f'/ver_evento/{evento_id}')

@app.route('/crear_mensaje_evento/<int:evento_id>', methods=['POST'])
def crear_mensaje_evento(evento_id):
    if 'usuario_id' not in session:
        return redirect('/')
    from flask_app.models.evento import Evento
    
    evento = Evento.get_by_id({'id': evento_id})
    if not evento:
        return redirect('/home')
    
    # Verificar que el usuario sea el creador del evento
    if evento.usuario_creador_id != session['usuario_id']:
        flash('Solo el creador puede publicar mensajes', 'mensaje_evento')
        return redirect(f'/ver_evento/{evento_id}')
    
    datos_mensaje = {
        'mensaje': request.form['mensaje'],
        'evento_id': evento_id
    }
    
    if not MensajeEvento.validar_mensaje(datos_mensaje):
        return redirect(f'/ver_evento/{evento_id}')
    
    MensajeEvento.crear_mensaje(datos_mensaje)
    return redirect(f'/ver_evento/{evento_id}')

@app.route('/eliminar_mensaje_evento/<int:mensaje_id>/<int:evento_id>')
def eliminar_mensaje_evento(mensaje_id, evento_id):
    if 'usuario_id' not in session:
        return redirect('/')
    from flask_app.models.evento import Evento
    
    evento = Evento.get_by_id({'id': evento_id})
    if not evento or evento.usuario_creador_id != session['usuario_id']:
        return redirect(f'/ver_evento/{evento_id}')
    
    MensajeEvento.eliminar_mensaje({'id': mensaje_id})
    return redirect(f'/ver_evento/{evento_id}')
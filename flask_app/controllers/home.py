from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app import bcrypt
from flask_app.models.evento import Evento
from flask_app.models.usuario import Usuario
from flask_app.models.grupo import Grupo
import os

@app.route('/home')
def home():
    if 'usuario_id' not in session:
        return redirect('/')
    # Obtener 4 eventos aleatorios activos - IA
    eventos = Evento.get_random_eventos(4)
    favoritos_semana = Evento.get_favoritos_proximos_aleatorios({
        'usuario_id': session['usuario_id'],
        'cantidad': 4
    })

    for evento in eventos:
        if evento.usuario_creador_id:
            usuario = Usuario.get_by_id({'id': evento.usuario_creador_id})
            evento.creador_nombre = f"{usuario.nombre} {usuario.apellido}"
        elif evento.grupo_creador_id:
            grupo = Grupo.get_by_id({'id': evento.grupo_creador_id})
            evento.creador_nombre = f"Grupo: {grupo.nombre}"
        else:
            evento.creador_nombre = "Desconocido"

    return render_template('home.html', eventos=eventos, favoritos_semana=favoritos_semana)

# RUTAS ICONOS NAVBAR
@app.route('/ir_mapa')
def ir_mapa():
    if 'usuario_id' not in session:
        return redirect('/')
    return redirect('/mapa')

@app.route('/mapa')
def mapa():
    if 'usuario_id' not in session:
        return redirect('/')
    eventos_db = Evento.get_favoritos_con_coordenadas({
    'usuario_id': session['usuario_id']
    })
    eventos = []
    for evento in eventos_db:
        eventos.append({
            "nombre": evento.nombre,
            "ubicacion": evento.ubicacion,
            "ciudad": evento.ciudad,
            "latitud": evento.latitud,
            "longitud": evento.longitud
        })
    return render_template(
        'mapa.html',
        eventos=eventos,
        google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY"),
        google_maps_map_id=os.getenv("GOOGLE_MAPS_MAP_ID", "DEMO_MAP_ID")
    )

@app.route('/ir_crear_grupo')
def ir_crear_grupo():
    if 'usuario_id' not in session:
        return redirect('/')
    return redirect('/crear_grupo')

@app.route('/crear_evento')
def ir_crear_evento():
    if 'usuario_id' not in session:
        return redirect('/')
    return redirect('/crear_evento')

# RUTAS MENU DESPLEGABLE "MI CUENTA"
@app.route('/ir_perfil')
def ir_perfil():
    if 'usuario_id' not in session:
        return redirect('/')
    return redirect('/perfil')

@app.route('/ir_mis_grupos')
def ir_mis_grupos():
    if 'usuario_id' not in session:
        return redirect('/')
    return redirect('/mis_grupos')

@app.route('/ir_mis_eventos')
def ir_mis_eventos():
    if 'usuario_id' not in session:
        return redirect('/')
    return redirect('/mis_eventos')

@app.route('/ir_mis_favoritos')
def ir_mis_favoritos():
    if 'usuario_id' not in session:
        return redirect('/')
    return redirect('/mis_favoritos')

@app.route('/ir_mis_seguidores')
def ir_mis_seguidores():
    if 'usuario_id' not in session:
        return redirect('/')
    return redirect('/mis_seguidores')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
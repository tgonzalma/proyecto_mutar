from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app import bcrypt
from flask_app.models.seguidor import Seguidor
from flask_app.models.grupo import Grupo

@app.route('/seguir_usuario/<int:usuario_id>')
def seguir_usuario(usuario_id):
    if 'usuario_id' not in session:
        return redirect('/')
    datos = {
        'usuario_seguidor_id': session['usuario_id'],
        'usuario_seguido_id': usuario_id
    }
    Seguidor.seguir(datos)
    redirect_to = request.args.get('redirect_to')
    if redirect_to:
        return redirect(redirect_to)
    return redirect(f'/mis_seguidores')

@app.route('/mis_seguidores')
def mis_seguidores():
    if 'usuario_id' not in session:
        return redirect('/')
    datos = {
        'usuario_id': session['usuario_id']
    }
    seguidores = Seguidor.obtener_seguidores(datos)
    seguidos = Seguidor.obtener_seguidos(datos)
    # Obtener grupos para el menú desplegable
    mis_grupos = Grupo.obtener_grupos_por_usuario(datos)
    return render_template('mis_seguidores.html', seguidores=seguidores, seguidos=seguidos, mis_grupos=mis_grupos)

@app.route('/dejar_seguir/<int:usuario_id>')
def dejar_seguir(usuario_id):
    if 'usuario_id' not in session:
        return redirect('/')
    datos = {
        'usuario_seguidor_id': session['usuario_id'],
        'usuario_seguido_id': usuario_id
    }
    Seguidor.dejar_de_seguir(datos)
    redirect_to = request.args.get('redirect_to')
    if redirect_to:
        return redirect(redirect_to)
    if request.args.get('from') == 'perfil':
        return redirect(f'/perfil/{usuario_id}')
    return redirect('/mis_seguidores')
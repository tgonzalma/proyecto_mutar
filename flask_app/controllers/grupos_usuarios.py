from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.grupo_usuario import GrupoUsuario


@app.route('/invitar_a_grupo', methods=['POST'])
def invitar_a_grupo():
    if 'usuario_id' not in session:
        return redirect('/')
    redirect_to = request.form.get('redirect_to')

    datos = {
        'usuario_id': request.form['usuario_id'],
        'grupo_id': request.form['grupo_id']
    }
    GrupoUsuario.agregar_usuario_a_grupo(datos)
    flash('Usuario invitado al grupo exitosamente', 'invitacion')
    if redirect_to:
        return redirect(redirect_to)
    return redirect(f'/perfil_grupo/{request.form["grupo_id"]}')
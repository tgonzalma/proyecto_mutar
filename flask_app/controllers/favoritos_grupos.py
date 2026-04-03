from flask import redirect, session, render_template, request, flash
from flask_app import app
from flask_app.models.favorito_grupo import FavoritoGrupo
from flask_app.models.favorito_usuario import FavoritoUsuario


@app.route('/asignar_favorito_grupo', methods=['POST'])
def asignar_favorito_grupo():
    if 'usuario_id' not in session:
        return redirect('/')
    evento_id = request.form['evento_id']
    grupo_id = request.form['grupo_id']
    usuario_id = session['usuario_id']
    favorito = FavoritoUsuario.get_favorito_by_evento_and_usuario({'evento_id': evento_id, 'usuario_id': usuario_id})
    if not favorito:
        # Si no existe, crea el favorito
        FavoritoUsuario.agregar_favorito({'usuario_id': usuario_id, 'evento_id': evento_id})
        favorito = FavoritoUsuario.get_favorito_by_evento_and_usuario({'evento_id': evento_id, 'usuario_id': usuario_id})
        if not favorito:
            flash('No se pudo crear el favorito', 'error')
            return redirect('/mis_favoritos')
    # Verificar si el evento ya está asignado al grupo - IA
    eventos_favoritos = FavoritoGrupo.obtener_eventos_favoritos_por_grupo({'grupo_id': grupo_id})
    if any(str(e['id']) == str(evento_id) for e in eventos_favoritos):
        flash('Ese evento ya está asignado a este grupo', 'error')
        return redirect(f'/perfil_grupo/{grupo_id}')
    # Guardar el id del evento
    datos = {
        'favorito_id': favorito['id'],
        'grupo_id': grupo_id
    }
    FavoritoGrupo.agregar_favorito_a_grupo(datos)
    return redirect(f'/perfil_grupo/{grupo_id}')
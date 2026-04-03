from flask import redirect, session, render_template, request, flash
from flask_app import app
from flask_app.models.favorito_usuario import FavoritoUsuario
from flask_app.models.usuario import Usuario
from flask_app.models.grupo import Grupo
from flask_app.models.evento import Evento

@app.route('/evento_favorito/<int:evento_id>')
def evento_favorito(evento_id):
    if 'usuario_id' not in session:
        return redirect('/')
    datos = {
        'usuario_id': session['usuario_id'],
        'evento_id': evento_id
    }
    FavoritoUsuario.agregar_favorito(datos)
    return redirect('/mis_favoritos')

@app.route('/mis_favoritos')
def mis_favoritos():
    if 'usuario_id' not in session:
        return redirect('/')
    datos = {
        'usuario_id': session['usuario_id']
    }
    eventos_favoritos = FavoritoUsuario.obtener_favoritos_por_usuario(datos)
    # Obtener los grupos del usuario una sola vez (evita que mis_grupos quede
    # sin definir si el usuario no tiene favoritos)
    mis_grupos = Grupo.obtener_grupos_por_usuario({'usuario_id': session['usuario_id']})

    for evento in eventos_favoritos:
        # Cconvierte el diccionario en objeto
        evento_obj = Evento(evento)
        # Añade nombre creador
        if evento_obj.usuario_creador_id:
            # Si el evento fue creado por un usuario
            usuario_creador = Usuario.get_by_id({'id': evento_obj.usuario_creador_id})
            evento['creador_nombre'] = f"{usuario_creador.nombre} {usuario_creador.apellido}"
        elif evento_obj.grupo_creador_id:
            # Si el evento fue creado por un grupo
            grupo_creador = Grupo.get_by_id({'id': evento_obj.grupo_creador_id})
            evento['creador_nombre'] = grupo_creador.nombre
        else:
            evento['creador_nombre'] = "Creador desconocido"
    return render_template('mis_favoritos.html', eventos_favoritos=eventos_favoritos, mis_grupos=mis_grupos)

@app.route('/eliminar_favorito/<int:evento_id>')
def eliminar_favorito(evento_id):
    if 'usuario_id' not in session:
        return redirect('/')
    datos = {
        'usuario_id': session['usuario_id'],
        'evento_id': evento_id
    }
    FavoritoUsuario.eliminar_favorito(datos)
    return redirect('/mis_favoritos')
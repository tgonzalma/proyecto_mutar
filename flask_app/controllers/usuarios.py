from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app.models.evento import Evento
from flask_app.models.grupo import Grupo
from flask_app.models.seguidor import Seguidor
from flask_app import bcrypt

@app.route('/')
def index():
    return render_template('index_login.html')

# rutas del sidebar login y pagina

@app.route('/logo')
def ir_logo():
    if 'usuario_id' not in session:
        return redirect('/')
    return redirect('/home')

@app.route('/registro_btn')
def ir_registro():
    return redirect('/registrar_usuario')

@app.route('/login_btn')
def ir_login():
    return redirect('/')

#rutas de login y registro

@app.route('/login', methods=['POST'])
def login():
    usuario_encontrado = Usuario.get_by_email( { 'email': request.form['email'] } )
    if not usuario_encontrado:
        flash("Email o password incorrectos", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(usuario_encontrado.password, request.form['password']):
        flash("Email o password incorrectos", "login")
        return redirect('/')
    
    session['usuario_id'] = usuario_encontrado.id
    return redirect('/home')

@app.route('/ir_registrar')
def ir_registrar():
    return redirect('/registrar_usuario')

@app.route('/registrar_usuario')
def registro():
    return render_template('registro.html', datos={})

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    if not Usuario.validar_registro(request.form):
        return redirect('/registrar_usuario')
    
    datos_usuario = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id_usuario = Usuario.save(datos_usuario)
    
    # Actualizar nickname
    if 'nombre_usuario' in request.form and request.form['nombre_usuario']:
        from flask_app.config.mysqlconnection import connectToMySQL
        query = "UPDATE usuarios SET nickname = %(nickname)s WHERE id = %(id)s"
        datos_nickname = {
            'id': id_usuario,
            'nickname': request.form['nombre_usuario']
        }
        connectToMySQL('db_proyecto_final_grupos').query_db(query, datos_nickname)
    
    session['usuario_id'] = id_usuario
    return redirect('/home')

@app.route('/buscar_usuarios')
def buscar_usuarios():
    if 'usuario_id' not in session:
        return redirect('/')

    termino = request.args.get('q', '')
    usuarios_encontrados = Usuario.buscar_por_email_o_nombre(termino)
    eventos_encontrados = Evento.buscar(termino)
    seguidos = Seguidor.obtener_seguidos({'usuario_id': session['usuario_id']})
    seguidos_ids = {seguido['id'] for seguido in seguidos}
    redirect_to = request.full_path[:-1] if request.full_path.endswith('?') else request.full_path

    return render_template(
        'resultados_usuarios.html',
        usuarios=usuarios_encontrados,
        eventos=eventos_encontrados,
        termino=termino,
        seguidos_ids=seguidos_ids,
        redirect_to=redirect_to
    )

@app.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect('/')
    datos_usuario = {
        'id': session['usuario_id']
    }
    usuario = Usuario.get_by_id(datos_usuario)
    # Obtener los eventos creados por este usuario
    datos_eventos = {
        'usuario_id': session['usuario_id']
    }
    eventos_creados = Evento.obtener_eventos_por_usuario(datos_eventos)
    eventos_seguidores = Evento.obtener_eventos_de_seguidores(datos_eventos)
    eventos_seguidos = Evento.obtener_eventos_de_seguidos(datos_eventos)
    return render_template('perfil.html', usuario=usuario, eventos_creados=eventos_creados, eventos_seguidores=eventos_seguidores, eventos_seguidos=eventos_seguidos)

@app.route('/perfil/<int:usuario_id>')
def perfil_otro(usuario_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    # Usuario que está viendo el perfil (el logueado)
    datos_usuario_actual = {
        'id': session['usuario_id']
    }
    usuario_actual = Usuario.get_by_id(datos_usuario_actual)
    
    # Usuario cuyo perfil se está viendo
    datos_usuario = {
        'id': usuario_id
    }
    usuario = Usuario.get_by_id(datos_usuario)
    
    # Obtener eventos creados por este usuario
    datos_eventos = {
        'usuario_id': usuario_id
    }
    eventos_creados = Evento.obtener_eventos_por_usuario(datos_eventos)
    mis_grupos = Grupo.obtener_grupos_por_usuario({'usuario_id': session['usuario_id']})
    
    # Verificar si el usuario actual ya sigue a este usuario
    from flask_app.models.seguidor import Seguidor
    datos_seguidor = {
        'usuario_seguidor_id': session['usuario_id'],
        'usuario_seguido_id': usuario_id
    }
    esta_siguiendo = Seguidor.esta_siguiendo(datos_seguidor)
    
    return render_template(
        'perfil_otro.html',
        usuario=usuario,
        eventos_creados=eventos_creados,
        usuario_actual=usuario_actual,
        esta_siguiendo=esta_siguiendo,
        mis_grupos=mis_grupos
    )

@app.route('/editar_perfil')
def editar_perfil():
    if 'usuario_id' not in session:
        return redirect('/')
    datos_usuario = {
        'id': session['usuario_id']
    }
    usuario = Usuario.get_by_id(datos_usuario)
    return render_template('editar_perfil.html', usuario=usuario)

@app.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil():
    if 'usuario_id' not in session:
        return redirect('/')
    
    import os
    from werkzeug.utils import secure_filename
    import time
    
    datos_actualizar = {
        'id': session['usuario_id'],
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'nickname': request.form.get('nickname', ''),
        'descripcion': request.form.get('descripcion', '')
    }
    
    # Manejar foto de perfil
    foto_perfil = request.files.get('foto_perfil')
    if foto_perfil and foto_perfil.filename:
        filename = secure_filename(foto_perfil.filename)
        timestamp = str(int(time.time()))
        nombre_unico = f"{timestamp}_{filename}"
        
        upload_folder = 'flask_app/static/img/usuarios'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        foto_perfil.save(os.path.join(upload_folder, nombre_unico))
        datos_actualizar['foto_perfil'] = nombre_unico
    else:
        # Mantener la foto actual
        usuario_actual = Usuario.get_by_id({'id': session['usuario_id']})
        datos_actualizar['foto_perfil'] = usuario_actual.foto_perfil
    
    # validar y hashear nueva contraseña
    if request.form.get('password') and request.form['password'].strip():
        if request.form['password'] != request.form.get('confirmacion', ''):
            flash('Las contraseñas no coinciden', 'perfil')
            return redirect('/editar_perfil')
        if len(request.form['password']) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'perfil')
            return redirect('/editar_perfil')
        datos_actualizar['password'] = bcrypt.generate_password_hash(request.form['password'])
    
    Usuario.actualizar_perfil(datos_actualizar)
    flash('Perfil actualizado exitosamente', 'perfil')
    return redirect('/perfil')
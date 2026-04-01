from flask_app import app
from flask_app.controllers import eventos
from flask_app.controllers import favoritos_grupos
from flask_app.controllers import favoritos_usuarios
from flask_app.controllers import grupos
from flask_app.controllers import grupos_usuarios
from flask_app.controllers import seguidores
from flask_app.controllers import usuarios
from flask_app.controllers import home


if __name__ == "__main__":
    app.run(debug=True)

    
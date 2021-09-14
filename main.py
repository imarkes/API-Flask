from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from controllers.clientes import clientes
from controllers.usuarios import usuarios
from auth.secrete_key import palavra_secreta
from blacklist import BLACKLIST


# app
app = Flask(__name__)


# Documentação
SWAGGER_URL = '/v1/docs'
sw_blue = get_swaggerui_blueprint(SWAGGER_URL, api_url='/static/swagger.json')
app.register_blueprint(sw_blue, url_prefix=SWAGGER_URL)


# Instancia as rotas controllers
app.register_blueprint(clientes.getBlueprintClientes())
app.register_blueprint(usuarios.getBlueprintUsuarios())


# autenticação
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = palavra_secreta
app.config['JWT_BLACKLIST_ENABLED'] = True

app.config['JSON_SORT_KEYS'] = False  # Ordena o objeto json de retorno da requisição


# Verifica se o token está na Blacklist
@jwt.token_in_blocklist_loader
def verificaBlackList(jwt_header, jwt_payload):
    if jwt_payload['jti'] in BLACKLIST:
        return jsonify(message='Token in blacklist')


# Revoga a autorização do token
@jwt.revoked_token_loader
def token_invalidado(jwt_header, jwt_payload):
    return jsonify({'Alert':'Token Revoked', 'message': 'Contact Administrator'}), 401


if __name__ == ('__main__'):
    app.run(debug=True)

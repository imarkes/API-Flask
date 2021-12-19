import json

from flask import jsonify, request, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from models.model_autorizacao import TabelaAutorizacao
from models.model_user import TabelaUsuarios
from auth.secrete_key import palavra_secreta
from blacklist import BLACKLIST

# Define o escopo das rotas
app = Blueprint('usuarios', __name__)


def get_blueprint_usuarios():
    """define o escopo das rotas de usuarios"""
    return app


# Rota de cadastro de usuario
@app.post('/v1/usuarios')
def cadastra_usuario():
    """Rota para cadastrar usuario"""
    try:
        dados = json.loads(request.data)
        consulta = TabelaUsuarios().listar_usuarios()

        # Cadastro
        novo = TabelaUsuarios().cadastrar_usuario(
            dados['nome'],
            dados['email'],
            generate_password_hash(palavra_secreta + dados['senha']))  # Criptografa a senha

        # Verifica se nome já existe
        for nome in consulta['response']:
            if nome[1] == dados['nome']:
                return jsonify(message='User Already Exists'), 409

        # Verifica erro de banco
        if novo['Error']:
            return jsonify({'Error': novo['Error'], 'message': 'Internal Server Error'}), 500

        return jsonify({'Error': False, 'message': 'Successfully Registered User'}), 201

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


@app.get('/v1/usuarios')
# @jwt_required()
def lista_usuarios():
    """Rota para Listar todos Usuarios Cadastrados"""
    try:
        response = []
        dados = TabelaUsuarios().listar_usuarios()

        # Verifica se existe usuario cadastrado
        if dados == None:
            return jsonify(message='Not Found'), 404

        # Verifica erro de banco
        if dados['Error']:
            return jsonify({'Error': dados['Error'], 'message': 'Internal Server Error'}), 500

        # Lista Usuarios
        for d in dados['response']:
            response.append({
                'cod': d[0],
                'nome': d[1],
                'email': d[2]
            })
        return jsonify({'Error': False, 'response': response}), 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


@app.get('/v1/usuarios/<int:id>')
# @jwt_required()
def lista_usuario_id(id):
    """Rota para Listar o usuario pelo ID"""
    try:
        dados = TabelaUsuarios().listar_usuario_pelo_id(id)

        # Verifica se o Id Existe
        if dados == None:
            return jsonify(message='ID Not Found'), 404

        # Verifica erro de banco
        if dados['Error']:
            return jsonify({'Error': dados['Error'], 'message': 'Internal Server Error'}), 500

        # Lista ID
        if dados['response'][0] == id:
            return jsonify({'Error': False, 'response': [{
                'id': id,
                'nome': dados['response'][1],
                'email': dados['response'][2]}]}), 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


@app.put('/v1/usuarios/<int:id>')
@jwt_required()
def atualiza_usuario(id):
    """Rota para atualiza o usuario pelo ID"""
    try:
        dados = json.loads(request.data)
        consulta = TabelaUsuarios().listar_usuario_pelo_id(id)

        # Verifica se Id Existe
        if consulta == None:
            return jsonify(message='ID Not Found'), 404

        # Atualiza
        if id == consulta['response'][0]:
            response = TabelaUsuarios().atualizar_usuario_com_parametros(
                id,
                dados['email'],
                generate_password_hash(palavra_secreta + dados['senha']))

            # Verifica erro de banco
            if response['Error']:
                return jsonify({'Error': True, 'message': 'Internal Server Error'}), 500

            return jsonify({'Error': False, 'response': 'Updated Successfully'}), 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


# Rota para Deletar Usuario
@app.delete('/v1/usuarios/<int:id>')
@jwt_required()
def deleta_usuario(id):
    try:
        consulta = TabelaUsuarios().listar_usuario_pelo_id(id)

        # Verifica se Id Existe
        if consulta == None:
            return jsonify(message='ID Not Found'), 404

        # Deleta
        deletado = TabelaUsuarios().deleta_usuario_pelo_id(id)

        # Verifica erro de Banco
        if deletado['Error']:
            return jsonify({'Error': True, 'message': 'Internal Server Error'}), 500

        return jsonify({'Error': deletado['Error'], 'message': deletado['message']}), 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


@app.post('/v1/login')
def login():
    """ Rota para criar o login de usuario """
    try:
        user = json.loads(request.data)
        login = TabelaUsuarios().login_user(user['nome'])

        # Verifica erro de banco
        if login['Error']:
            return jsonify({'Error': True, 'message': 'Internal Server Error'}), 500

        if check_password_hash(login['message'][1], palavra_secreta + user['senha']):  # Compara as senhas
            token = create_access_token(identity=palavra_secreta + user['senha'])  # Gera o token de acesso

            aut = (login['message'][0], token)
            TabelaAutorizacao().adicionarToken(aut[0], aut[1])  # Inserir o token no Banco de dados

            return jsonify({
                'nome': login['message'][0],
                'token': token}), 200

        return jsonify({'message': 'Check Username or Password'}), 401

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


@app.post('/v1/logout')
@jwt_required()
def logout():
    """ Rota para fazer logout de usuario"""
    try:
        jwt_id = get_jwt()['jti']  # 'jti' é Identificador do token
        BLACKLIST.add(jwt_id)  # Adiciona o token na Blacklist
        return {'Alert': 'Logout', 'message': 'Login to access'}, 200

    except Exception as e:
        return {'Error': f'{e}', 'message': 'You are not logged in'}, 500

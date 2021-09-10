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


def getBlueprintUsuarios():
    return app


# Rota de cadastro de usuario
@app.post('/v1/usuarios')
def cadastrarUsuario():
    try:
        dados = json.loads(request.data)
        consulta = TabelaUsuarios().listar()

        # Verifica se nome já existe
        for nome in consulta['response']:
            if nome[1] == dados['nome']:
                return jsonify(message='Usuario já cadastrado', status=409), 409

        # Cadastra
        novo = TabelaUsuarios().cadastrar(
            dados['nome'],
            dados['email'],
            generate_password_hash(palavra_secreta + dados['senha']))  # Criptografa a senha
        return jsonify({'Error': False, 'message': 'Usuario cadastrado com sucesso'}), 201

    except Exception as e:
        return {'Error': e}, 500


# Rota para Listar todos Usuarios Cadastrados
@app.get('/v1/usuarios')
# @jwt_required()
def listaUsuario():
    try:
        response = []
        dados = TabelaUsuarios().listar()

        # Lista Usuarios
        for d in dados['response']:
            response.append({
                'cod': d[0],
                'nome': d[1],
                'email': d[2]
            })
        return jsonify({'Error': False, 'response': response}), 200

    except Exception as e:
        return {'Error': e}, 500


# Rota para Listar o usuario pelo ID
@app.get('/v1/usuarios/<int:id>')
# @jwt_required()
def listaUsuarioId(id):
    try:
        dados = TabelaUsuarios().listarId(id)

        # Verifica se o Id Existe
        if dados['Error']:
            return jsonify(dados)

        # Lista ID
        if dados['response'][0] == id:
            return jsonify({'Error': False, 'response': [{
                'id': id,
                'nome': dados['response'][1],
                'email': dados['response'][2]}]}), 200

    except Exception as e:
        return {'Error': e}, 400


# Rota para atualiza o usuario pelo ID
@app.put('/v1/usuarios/<int:id>')
@jwt_required()
def atualizarUsuario(id):
    try:
        dados = json.loads(request.data)
        consulta = TabelaUsuarios().listarId(id)

        # Verifica se Id Existe
        if consulta['Error']:
            return jsonify(consulta), 404

        # Atualiza
        if id == consulta['response'][0]:
            response = TabelaUsuarios().atualizar(
                id,
                dados['email'],
                dados['senha'])
            return jsonify({'Error': False, 'response': 'Updated'}), 200

    except Exception as e:
        return {'Error': e}, 500


# Rota para Deletar Usuario
@app.delete('/v1/usuarios/<int:id>')
@jwt_required()
def deletaUsuario(id):
    try:
        consulta = TabelaUsuarios().listarId(id)

        # Verifica se Id Existe
        if consulta['Error']:
            return jsonify(consulta), 404

        # Deleta
        return TabelaUsuarios().deletar(id), 200

    except Exception as e:
        return {'Error': e}, 500


# Rota de Login
@app.post('/v1/login')
def login():
    try:
        user = json.loads(request.data)
        login = TabelaUsuarios().loginUser(user['nome'])

        if check_password_hash(login['message'][1], palavra_secreta + user['senha']):  # Compara as senhas
            token = create_access_token(identity=palavra_secreta + user['senha'])  # Gera o token de acesso

            aut = (login['message'][0], token)
            TabelaAutorizacao().adicionarToken(aut[0], aut[1])  # Inserir o token no Banco de dados

            return jsonify({
                'nome': login['message'][0],
                'token': token})

        return jsonify({'message': 'Verifique Usuario e Senha'}), 401

    except Exception as e:
        return jsonify({'Error': True, 'message': e}), 500


# Rota de Logout
@app.post('/v1/logout')
@jwt_required()
def logout():
    try:
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)  # Adiciona o token na Blacklist
        return {'message': ' Faça o login para acessar'}, 200

    except Exception as e:
        return {'Error': e, 'message': 'Você não esta logado'}, 500

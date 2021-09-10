import json

from flask_jwt_extended import jwt_required
from flask import jsonify, request, Blueprint

from models.model_clientes import TabelaClientes


# Define o escopo das rotas
app = Blueprint('clientes', __name__)


def getBlueprintClientes():
    return app


# Rota para cadastra um novo Cliente
@app.post('/v1/clientes')
def cadastrarCliente():
    try:
        consulta = TabelaClientes().listar()
        dados = json.loads(request.data)

        ##Verifica se nome já Existe
        for nome in consulta['response']:
            if nome[1] == dados['nome']:
                return jsonify(message=f'Nome já cadastrado: {nome[1]}', status=409), 409

        # Cadastra
        novo = TabelaClientes().cadastrar(
            dados['nome'],
            dados['email'],
            dados['telefone'],
            dados['cidade'])
        return jsonify({'Error': False, 'response': dados}, status=201), 201

    except Exception as e:
        return {'Error': e}, 500


# Rota para Lista os clientes cadastrados
@app.get('/v1/clientes')
# @jwt_required()
def listaClientes():
    try:
        response = []
        dados = TabelaClientes().listar()

        # Lista Todos
        for d in dados['response']:
            response.append({
                'cod': d[0],
                'nome': d[1],
                'email': d[2],
                'telefone': d[3],
                'cidade': d[4]
            })
        return jsonify({'Error': False, 'response': response}), 200

    except Exception as e:
        return {'Error': e}, 500


# Rota para Listar o cliente pelo ID
@app.get('/v1/clientes/<int:id>')
# @jwt_required()
def listaClienteId(id):
    try:
        dados = TabelaClientes().listarId(id)

        # Verifica se Id Existe
        if dados['Error']:
            return jsonify(dados), 404

        # Lista ID
        if dados['response'][0] == id:
            return jsonify({'Error': False, 'response': [{
                'id': id,
                'nome': dados['response'][1],
                'email': dados['response'][2],
                'telefone': dados['response'][3],
                'cidade': dados['response'][4]}]}), 200

    except Exception as e:
        return {'Error': e}, 500


# Rota para Atualiza o cliente pelo ID
@app.put('/v1/clientes/<int:id>')
@jwt_required()
def atualizaCliente(id):
    try:
        dados = json.loads(request.data)
        consulta = TabelaClientes().listarId(id)

        # verifica se ID existe
        if consulta['Error']:
            return jsonify(consulta), 404

        # Atualiza
        if id == consulta['response'][0]:
            response = TabelaClientes().atualizar(
                id,
                dados['nome'],
                dados['email'],
                dados['telefone'],
                dados['cidade'])
            return jsonify({'Error': False, 'response': 'Updated'}), 200

    except Exception as e:
        return {'Error': e}, 500


# Rota para Deletar o Cliente pelo ID
@app.delete('/v1/clientes/<int:id>')
@jwt_required()
def deletaClienteId(id):
    try:
        consulta = TabelaClientes().listarId(id)

        # Verifica se Id Existe
        if consulta['Error']:
            return jsonify(consulta), 404

        # Deleta
        return TabelaClientes().deletar(id), 200

    except Exception as e:
        return {'Error': e}, 500

import json

from flask_jwt_extended import jwt_required
from flask import jsonify, request, Blueprint

from models.model_clientes import TabelaClientes


# Define o escopo clientes
app = Blueprint('clientes', __name__)
def getBlueprintClientes():
    return app


# Rota para cadastra um novo Cliente
@app.post('/v1/clientes')
@jwt_required()
def cadastrarCliente():
    try:
        consulta = TabelaClientes().listar()
        dados = json.loads(request.data)

        # Cadastro
        novo = TabelaClientes().cadastrar(
            dados['nome'],
            dados['email'],
            dados['telefone'],
            dados['cidade'])

        # Verifica os tipos de dados enviados
        if dados['nome'] is None or dados['nome'] == "":
             return jsonify(message='Name is required'),400
        elif dados['email'] is None or dados['email']== "":
            return jsonify(message ="Email is required"),400
        elif dados['telefone'] is not int:
            return jsonify(message='Telefone type Integer is required'),400


        ##Verifica se nome já Existe
        for nome in consulta['response']:
            if nome[1] == dados['nome']:
                return jsonify(message='User Already Exists'), 409

        # Verifica erro de servidor
        if novo['Error']:
            return jsonify({'Error': novo['Error'], 'message': 'Internal Server Error'}), 500

        retorno= jsonify({'Error': False, 'message': 'Successfully Registered Client'})
        return retorno,201

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


# Rota para Lista os clientes cadastrados
@app.get('/v1/clientes')
@jwt_required()
def listaClientes():
    try:
        response = []
        dados = TabelaClientes().listar()

        # Verifica se existe usuario cadastrado
        if dados is None:
            return jsonify(message='Not Found'), 404

        # Verifica erro de servidor
        if dados['Error']:
            return jsonify({'Error': dados['Error'], 'message': 'Internal Server Error'}), 500

        # Lista Todos
        for d in dados['response']:

            response.append({
                'cod': d[0],
                'nome': d[1],
                'email': d[2],
                'telefone': int(d[3]),
                'cidade': d[4],
                'criacao':d[5]
            })

        retorno = jsonify({'clients': response})
        return retorno, 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


# Rota para Listar o cliente pelo ID
@app.get('/v1/clientes/<int:id>')
@jwt_required()
def listaClienteId(id):
    try:
        dados = TabelaClientes().listarId(id)

        # Verifica se o Id Existe
        if dados is None:
            return jsonify(message='ID Not Found'), 404

        # Verifica erro de servidor
        if dados['Error']:
            return jsonify({'Error': dados['Error'], 'message': 'Internal Server Error'}), 500

        # Lista ID
        if dados['response'][0] == id:
            return jsonify({'Error': False, 'clients': [{
                'id': id,
                'nome': dados['response'][1],
                'email': dados['response'][2],
                'telefone':int(dados['response'][3]),
                'cidade': dados['response'][4],
                'criacao':dados['response'][5]}]}), 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


# Rota para Atualiza o cliente pelo ID
@app.put('/v1/clientes/<int:id>')
@jwt_required()
def atualizaCliente(id):
    try:
        dados = json.loads(request.data)
        consulta = TabelaClientes().listarId(id)

        # Verifica se Id Existe
        if consulta is None:
            return jsonify(message='ID Not Found'), 404

        # Atualiza
        if id == consulta['response'][0]:
            response = TabelaClientes().atualizar(
                id,
                dados['nome'],
                dados['email'],
                dados['telefone'],
                dados['cidade'])

            # Verifica erro de servidor
            if response['Error']:
                return jsonify({'Error': True, 'message': 'Internal Server Error'}), 500

            return jsonify({'Error': False, 'response': 'Updated Successfully'}), 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


# Rota para Deletar o Cliente pelo ID
@app.delete('/v1/clientes/<int:id>')
@jwt_required()
def deletaClienteId(id):
    try:
        consulta = TabelaClientes().listarId(id)

        # Verifica se Id Existe
        if consulta == None:
            return jsonify(message='ID Not Found'), 404

        # Deleta
        deletado = TabelaClientes().deletar(id)

        # Verifica erro de servidor
        if deletado['Error']:
            return jsonify({'Error': True, 'message': 'Internal Server Error'}), 500

        return jsonify({'Error': deletado['Error'], 'message': deletado['message']}), 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500

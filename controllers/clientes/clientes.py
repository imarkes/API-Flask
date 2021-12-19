import json

from flask_jwt_extended import jwt_required
from flask import jsonify, request, Blueprint

from models.model_clientes import TabelaClientes

app = Blueprint('clientes', __name__)


def get_blueprint_clientes():
    """Define o escopo clientes"""
    return app


# Rota para cadastra um novo Cliente
@app.post('/v1/clientes')
@jwt_required()
def cadastrar_cliente():
    """ Rota para cadastrar os clientes"""
    try:
        consulta = TabelaClientes().listar_clientes()
        dados = json.loads(request.data)

        novo = TabelaClientes().cadastra_clientes(
            dados['nome'],
            dados['email'],
            dados['telefone'],
            dados['cidade'])

        # Verifica os tipos de dados enviados
        if dados['nome'] is None or dados['nome'] == "":
            return jsonify(message='Name is required'), 400
        elif dados['email'] is None or dados['email'] == "":
            return jsonify(message="Email is required"), 400
        elif dados['telefone'] is not int:
            return jsonify(message='Telefone type Integer is required'), 400

        # Verifica se nome já Existe
        for nome in consulta['response']:
            if nome[1] == dados['nome']:
                return jsonify(message='User Already Exists'), 409

        # Verifica erro de servidor
        if novo['Error']:
            return jsonify({'Error': novo['Error'], 'message': 'Internal Server Error'}), 500

        retorno = jsonify({'Error': False, 'message': 'Successfully Registered Client'})
        return retorno, 201

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


@app.get('/v1/clientes')
@jwt_required()
def lista_clientes():
    """Rota para Lista os clientes cadastrados"""
    try:
        response = []
        dados = TabelaClientes().listar_clientes()

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
                'criacao': d[5]
            })

        retorno = jsonify({'clients': response})
        return retorno, 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


@app.get('/v1/clientes/<int:id>')
@jwt_required()
def lista_cliente_Id(id):
    """Rota para Listar o cliente pelo ID"""
    try:
        dados = TabelaClientes().lista_cliente_pelo_id(id)

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
                'telefone': int(dados['response'][3]),
                'cidade': dados['response'][4],
                'criacao': dados['response'][5]}]}), 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500


@app.put('/v1/clientes/<int:id>')
@jwt_required()
def atualiza_cliente(id):
    """Rota para Atualiza o cliente pelo ID"""
    try:
        dados = json.loads(request.data)
        consulta = TabelaClientes().atualizar_cliente_com_args(id)

        # Verifica se Id Existe
        if consulta is None:
            return jsonify(message='ID Not Found'), 404

        # Atualiza
        if id == consulta['response'][0]:
            response = TabelaClientes().atualizar_cliente_com_args(
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


@app.delete('/v1/clientes/<int:id>')
@jwt_required()
def deleta_cliente_id(id):
    """ Rota para Deletar o Cliente pelo ID"""
    try:
        consulta = TabelaClientes().lista_cliente_pelo_id(id)

        # Verifica se Id Existe
        if consulta == None:
            return jsonify(message='ID Not Found'), 404

        # Deleta
        deletado = TabelaClientes().deletar_cliente_pelo_id(id)

        # Verifica erro de servidor
        if deletado['Error']:
            return jsonify({'Error': True, 'message': 'Internal Server Error'}), 500

        return jsonify({'Error': deletado['Error'], 'message': deletado['message']}), 200

    except Exception as e:
        return jsonify({'Error': True, 'message': f'{e}'}), 500

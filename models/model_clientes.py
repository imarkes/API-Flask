from connection.conection import Connection
from psycopg2 import Error


class TabelaClientes(Connection):
    """Manipula a tabela Clientes"""

    def __init__(self):
        """Instancia a conexão"""
        Connection.__init__(self)

    def cadastra_clientes(self, *args):
        """SQL Cadastra clientes"""
        try:
            sql = "INSERT INTO clientes (nome, email, telefone, cidade) VALUES (%s, %s, %s, %s)"

            self.execute(sql, args)
            self.commit()
            return {'Error': False, 'message': 'created', 'status': 201}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

    def listar_clientes(self):
        """SQL Retorna a consulta SQL com base nos parametros"""
        try:
            sql = f"SELECT cod, nome, email, telefone, cidade, criacao FROM clientes"
            dados = self.query(sql)

            if dados:
                return {'Error': False, 'response': dados, 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

    def lista_cliente_pelo_id(self, id):
        """SQL Retorna a consulta SQL com base no ID"""
        try:
            sql = f"SELECT cod, nome, email, telefone, cidade, criacao FROM clientes WHERE cod = '{id}'"
            dados = self.query(sql)

            if len(dados) > 0:
                return {'Error': False, 'response': dados[0], 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

    def atualizar_cliente_com_args(self, id, *args):
        """SQL Atualiza os clientes com base nos parametros"""
        try:
            sql = f"UPDATE clientes SET (nome, email, telefone, cidade) = (%s, %s, %s, %s) WHERE cod = '{id}'"
            self.execute(sql, args)
            self.commit()
            return {'Error': False, 'message': 'Updated', 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

    def deletar_cliente_pelo_id(self, id):
        """SQL Deleta cliente com base no ID"""
        try:
            sql = f"DELETE FROM clientes WHERE cod = '{id}'"
            self.execute(sql)
            self.commit()
            return {'Error': False, 'message': 'Deletead', 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}  # retorno status

from connection.conection import connection
from psycopg2 import Error


#Conectando ao BD Clientes
class TabelaClientes(connection):
    def __init__(self):
        connection.__init__(self)


    def cadastrar(self, *args):
        try:
            sql = "INSERT INTO clientes (nome, email, telefone, cidade) VALUES (%s, %s, %s, %s)"

            self.execute(sql, args)
            self.commit()
            return {'Error': False, 'message': 'created', 'status': 201}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}


    def listar(self):
        try:
            sql = f"SELECT cod, nome, email, telefone, cidade FROM clientes"
            dados = self.query(sql)

            if dados:
                return {'Error': False, 'response': dados, 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}


    def listarId(self, id):
        try:
            sql = f"SELECT cod, nome, email, telefone, cidade FROM clientes WHERE cod = '{id}'"
            dados = self.query(sql)

            if len(dados) > 0:
                return {'Error': False, 'response': dados[0], 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}


    def atualizar(self, id, *args):
        try:
            sql = f"UPDATE clientes SET (nome, email, telefone, cidade) = (%s, %s, %s, %s) WHERE cod = '{id}'"
            self.execute(sql, args)
            self.commit()
            return {'Error': False, 'message': 'Updated', 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}


    def deletar(self, id):
        try:
            sql = f"DELETE FROM clientes WHERE cod = '{id}'"
            self.execute(sql)
            self.commit()
            return {'Error': False, 'message': 'Deletead', 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}# retorno status


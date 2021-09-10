from connection.conection import connection
from psycopg2 import Error


#Conectando ao BD Clientes
class TabelaUsuarios(connection):
    def __init__(self):
        connection.__init__(self)


    def cadastrar(self, *args):
        try:
            sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"

            self.execute(sql, args)
            self.commit()
            return {'Error': False, 'message': 'Created', 'status': 201}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}


    def listar(self):
        try:
            sql = f"SELECT cod, nome, email FROM usuarios"
            dados = self.query(sql)

            if dados:
                return {'Error': False, 'response': dados, 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}


    def listarId(self, id):
        try:
            sql = f"SELECT cod, nome, email FROM usuarios WHERE cod = '{id}'"
            dados = self.query(sql)

            if len(dados) > 0:
                return {'Error': False, 'response': dados[0], 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}


    def atualizar(self, id, *args):
        try:
            sql = f"UPDATE usuarios SET (email, senha) = (%s, %s) WHERE cod = '{id}'"
            self.execute(sql, args)
            self.commit()
            return {'Error': False, 'message': 'Updated', 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}


    def deletar(self, id):
        try:
            sql = f"DELETE FROM usuarios WHERE cod = '{id}'"
            self.execute(sql)
            self.commit()
            return {'Error': False, 'message': 'Deletead', 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}


    def loginUser(self, nome):
        try:
            sql = f"SELECT nome, senha FROM usuarios WHERE nome = '{nome}'"
            dados = self.query(sql)

            if len(dados)>0:
                return {'Error': False, 'message':dados[0]}

        except Error as e:
            return {'Error':True, 'message': e}



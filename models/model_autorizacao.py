from connection.conection import connection
from psycopg2 import Error


#Conectando ao BD Clientes
class TabelaAutorizacao(connection):
    def __init__(self):
        connection.__init__(self)

    # Adiciona o login e token no banco de dados
    def adicionarToken(self, *args):
        try:
            sql = "INSERT INTO autorizacao (login, validador) VALUES (%s, %s)"

            self.execute(sql, args)
            self.commit()
            return {'Error': False, 'message': 'created', 'status': 201}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

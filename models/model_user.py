from connection.conection import Connection
from psycopg2 import Error


class TabelaUsuarios(Connection):
    """#Manipula a tabela Usuarios"""

    def __init__(self):
        """Instancia a conexao"""
        Connection.__init__(self)

    def cadastrar_usuario(self, *args):
        """SQL para cadastrar usuario"""
        try:
            sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"

            self.execute(sql, args)
            self.commit()
            return {'Error': False, 'message': 'Created', 'status': 201}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

    def listar_usuarios(self):
        """SQL para listar todos usuarios"""
        try:
            sql = f"SELECT cod, nome, email FROM usuarios"
            dados = self.query(sql)

            if dados:
                return {'Error': False, 'response': dados, 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

    def listar_usuario_pelo_id(self, id):
        """SQL para listar o usuario pelo ID"""
        try:
            sql = f"SELECT cod, nome, email FROM usuarios WHERE cod = '{id}'"
            dados = self.query(sql)

            if len(dados) > 0:
                return {'Error': False, 'response': dados[0], 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

    def atualizar_usuario_com_parametros(self, id, *args):
        """SQL para atualizar usuarios com parametros"""
        try:
            sql = f"UPDATE usuarios SET (email, senha) = (%s, %s) WHERE cod = '{id}'"
            self.execute(sql, args)
            self.commit()
            return {'Error': False, 'message': 'Updated', 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

    def deleta_usuario_pelo_id(self, id):
        """SQL para deletar usuario pelo ID"""
        try:
            sql = f"DELETE FROM usuarios WHERE cod = '{id}'"
            self.execute(sql)
            self.commit()
            return {'Error': False, 'message': 'Deletead', 'status': 200}

        except Error as e:
            return {'Error': True, 'message': e, 'status': 500}

    def login_user(self, nome):
        """SQL para consultar o login e senha do usuario"""
        try:
            sql = f"SELECT nome, senha FROM usuarios WHERE nome = '{nome}'"
            dados = self.query(sql)

            if len(dados) > 0:
                return {'Error': False, 'message': dados[0]}

        except Error as e:
            return {'Error': True, 'message': e}

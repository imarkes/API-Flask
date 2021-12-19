import psycopg2 as db
from connection.db_config import Conect_postgress


class Connection(Conect_postgress):
    """ Executa as intruções de DML """

    def __init__(self):
        """Instancia a configuração com o banco de dados"""
        Conect_postgress.__init__(self)
        try:
            # cria a conexão com o dicionario db_config
            self.conn = db.connect(**self.config['postgres'])  # (**) para desempacotar o config
            self.cur = self.conn.cursor()
        except db.Error as e:
            print(f'Erro ao se conectar {e}')
            exit(1)  # parametro para sair da conexao

    def __enter__(self):
        """Entra e retornar o objeto conexao"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Finaliza a conexao com banco de dados"""
        self.commit()
        self.conn.close()

    @property
    def connection(self):
        """Objeto da conexão"""
        return self.conn

    @property
    def cursor(self):
        """Manipula o banco de dados"""
        return self.cur

    def commit(self):
        """Persiste as instruções SQL"""
        self.connection.commit()
        return self.cur

    def fetchall(self):
        """ Retorna todos itens da consulta SQL"""
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        """Executa as instruções SQL"""
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        """instrução SQL com ou sem parametros"""
        self.cursor.execute(sql, params or ())
        return self.fetchall()

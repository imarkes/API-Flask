class conect_postgress:
    def __init__(self):
        self.config = {
            'postgres':{
                'host': 'localhost',
                'database': 'clientes_db',
                'user': 'postgres',
                'password': 'henet',
                'port': 5432
            }
    }

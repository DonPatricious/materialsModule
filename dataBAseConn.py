import psycopg



class DatabaseConnection:
    def __init__(self, 
                 host="localhost", 
                 port=5432, 
                 database="candorlocaldb", 
                 user="postgres", 
                 password="EskyuEl1#653"):
        
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False
    
    def connect(self):
        self.conn = psycopg.connect(
            host=self.host,
            port=self.port,
            dbname=self.database,
            user=self.user,
            password=self.password
        )
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
    
    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        cursor.close()
        return results, columns
    
    def executemany(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.executemany(query, params)
        self.conn.commit()
        results = cursor.fetchall()
        cursor.close()
        return results


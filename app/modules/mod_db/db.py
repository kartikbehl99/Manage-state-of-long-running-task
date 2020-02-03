import pymysql
import sqlalchemy
import logging
from app.exts import app


class DB:
    def __init__(self):
        self.db_name = app.config["DB_NAME"]
        self.db_password = app.config["DB_PASSWORD"]
        self.db_host = app.config["DB_HOST"]
        self.db_username = app.config["DB_USERNAME"]
        self.cursor = None

    def create_connection(self):
        conn = f'mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_host}/{self.db_name}'
        engine = sqlalchemy.create_engine(conn, echo=False)
        self.cursor = engine.connect()
        return self.cursor

    def run(self, query):
        response = []
        try:
            result = self.cursor.execute(query)
            for row in result:
                response.append(list(row))
        except Exception as e:
            logging.error(str(e))
        return response

    def close_connection(self):
        self.cursor.close()

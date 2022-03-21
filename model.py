import mysql.connector
from mysql.connector import Error

class Connection:

    def __init__(self) -> None:
        pass

    def connect(self):
        connection = mysql.connector.connect(user='lat',
                                    password='latif123',
                                    host='localhost',
                                    database='jensel',
                                    auth_plugin='mysql_native_password')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)

        return connection


    def insert(self, socmed, nickname, datetime, tagline, images, connection):

        try:

            if connection.is_connected():
                query  = """
                            INSERT INTO crawl_socmed (socmed, nickname, datetime, tagline, image, created_at) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP())
                         """
                cursor = connection.cursor()
                cursor.execute(query, [socmed, nickname, datetime, tagline, images])
                connection.commit()
                id = cursor.lastrowid

        except Error as e:
            #print("Error while connecting to MySQL", e)
            pass

        finally:
            if connection.is_connected():
                cursor.close()
                # print("cursor is closed")


    def close_connection(self, connection):
        connection.close()
        # print("MySQL connection is closed")

import mysql.connector
from typing import List


class Database:
    """Class for working with resources DB"""
    def __init__(self, *, user_name: str = 'root', user_password: str = 'root'):
        """Establishes connection with DB"""
        try:
            self.connection = mysql.connector.connect(
                user=user_name,
                password=user_password,
                host='localhost',
                port=3306,
                database='resources')
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            print("Connect error: ", e)
            self.__del__()

    def __del__(self):
        """Closes connection just before removal object"""
        self.connection.commit()
        self.connection.close()

    def select(self, *, table: str, select: str, where: str = '',
               group_by: str = '', join: str = '') -> List[tuple]:
        """SELECT query"""
        query = f"""SELECT {select} FROM {table} a"""
        if join:
            query += f""" JOIN {join} b ON a.lux_name = b.lux_name"""
        if where:
            query += f""" WHERE {where}"""
        if group_by:
            query += f""" GROUP BY {group_by}"""
        print(f'{query=}')
        try:
            if ';' in select + table + join + where + group_by:
                raise mysql.connector.Error('Unsafe parameter for select query')
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(e)

    def insert(self, *, table: str, columns: str, values: str) -> None:
        """INSERT query"""
        query = f"""INSERT {table}({columns}) VALUES ({values})"""
        print(f'{query=}')
        try:
            if ';' in table + columns + values:
                raise mysql.connector.Error('Unsafe parameter for insert query')
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(e)

    def update(self, *, table: str, values: str, where: str) -> None:
        """UPDATE query"""
        query = f"""UPDATE {table} SET {values} WHERE {where}"""
        print(f'{query=}')
        try:
            if ';' in table + values + where:
                raise mysql.connector.Error('Unsafe parameter for update query')
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(e)

    def delete(self, *, table: str, where: str) -> None:
        """DELETE query"""
        query = f"""DELETE FROM {table} WHERE {where}"""
        print(f'{query=}')
        try:
            if ';' in table + where:
                raise mysql.connector.Error('Unsafe parameter for delete query')
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(e)

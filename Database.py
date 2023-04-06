import mysql.connector
from typing import List


class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                user='root',
                password='12345',
                host='localhost',
                port=3306,
                database='resources')
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            print("Connect error: ", e)
            self.__del__()

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def select(self, *, table: str, select: str, where: str = None,
               group_by: str = None, join: str = None) -> List[tuple]:
        query = f"""SELECT {select} FROM {table} a"""
        if join:
            query += f""" JOIN {join} b ON a.lux_name = b.lux_name"""
        if where:
            query += f""" WHERE {where}"""
        if group_by:
            query += f""" GROUP BY {group_by}"""
        print(f'{query=}')
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(e)

    def insert(self, *, table: str, columns: str, values: str) -> None:
        query = f"""INSERT {table}({columns}) VALUES ({values})"""
        print(f'{query=}')
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(e)

    def update(self, *, table: str, values: str, where: str) -> None:
        query = f"""UPDATE {table} SET {values} WHERE {where}"""
        print(f'{query=}')
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(e)

    def delete(self, *, table: str, where: str) -> None:
        query = f"""DELETE FROM {table} WHERE {where}"""
        print(f'{query=}')
        self.cursor.execute(query)
        self.connection.commit()

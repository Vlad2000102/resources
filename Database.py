import mysql.connector


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

    def select(self, *, table, select, where=None, group_by=None, join=None):
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

    def insert(self, *, table, columns, values):
        query = f"""INSERT {table}({columns}) VALUES ({values})"""
        print(f'{query=}')
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(e)

    def update(self, *, table, values, where):
        query = f"""UPDATE {table} SET {values} WHERE {where}"""
        print(f'{query=}')
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(e)

    def delete(self, *, table, where):
        query = f"""DELETE FROM {table} WHERE {where}"""
        print(f'{query=}')
        self.cursor.execute(query)
        self.connection.commit()


if __name__ == "__main__":
    print("Go out there!!!")

# -*- coding: utf-8 -*-
import sqlite3


class ConnectionDB:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite.db")
        self.cursor = self.conn.cursor()

    def insert(self, table: str, columns: str, values: str) -> str:
        """inserindo um registro na tabela"""

        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(query)
        self.conn.commit()  # gravando no bd
        return "Dado inserido com sucesso."

    def select_all(self, table: str) -> list:
        """lendo todos os dados"""

        query = f"SELECT * FROM {table}"
        tb = self.cursor.execute(query)
        columns = [i[0] for i in tb.description]
        return [dict(zip(columns, row)) for row in tb.fetchall()]

    def select_filter(self, table: str, where: str, limit: int = None) -> list:
        """filtrando os dados"""

        query = f"SELECT * FROM {table} WHERE {where}"

        if limit:
            query = f"SELECT * FROM {table} WHERE {where} LIMIT {limit}"

        tb = self.cursor.execute(query)
        columns = [i[0] for i in tb.description]
        return [dict(zip(columns, row)) for row in tb.fetchall()]

    def update(self, table: str, col_val: str, where: str) -> str:
        """atualizando registros"""

        query = f"UPDATE {table} SET {col_val} WHERE {where}"
        self.cursor.execute(query)
        self.conn.commit()  # gravando no bd
        return "Dados atualizados com sucesso."

    def finish(self):
        self.conn.close()

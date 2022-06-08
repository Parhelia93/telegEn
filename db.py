import os
from typing import Dict, List, Tuple

import sqlite3


conn = sqlite3.connect(os.path.join("db", "finance.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def fetch_where(table: str, columns: List[str], where_column: str, where_val:str) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {where_column}={where_val}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def fetch_limit(table: str, columns: List[str],where_column: str, where_val:str,limit:int) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {where_column}={where_val} LIMIT {limit}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def update_columns(table: str, column: str, where_col: str, where_val: str, val:str):
    cursor.execute(f"UPDATE {table} SET {column} = '{val}' WHERE {where_col} = '{where_val}'")
    conn.commit()


def fetch_new_words(table: str, columns: List[str], limit: int, user_id: str, code:str) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE words.id NOT IN (SELECT word_id from users_words WHERE user_id = {user_id}) AND words.category_id = {code} LIMIT {limit}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def fetch_learned_words(table: str, columns: List[str], user_id: str):
    columns_joined = ", ".join(columns)
    cursor.execute(
        f"SELECT {columns_joined} FROM {table} WHERE user_id = {user_id} AND stage = 1")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result



def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='words'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()

# print(fetchall('word', 'word word_translate'.split()))
# print(fetch_where('word', 'word word_translate'.split(), 'cat_id', '1'))
# insert('word', {'word': 'sign', 'word_translate':'signal', 'cat_id':'1'})
# print(fetch_where('word', 'word word_translate'.split(), 'cat_id', '1'))

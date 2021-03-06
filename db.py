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

def fetch_where_1(table: str, columns: List[str], where_column: str, where_val:str) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {where_column}='{where_val}'")
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


def fetch_limit_and(table: str, columns: List[str],where_column: str, where_val:str,limit:int, where_column1: str, where_val1:str) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {where_column}={where_val} AND {where_column1}={where_val1} LIMIT {limit}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result



def update_columnss(table: str, columns: List[str], values: List[str], where_col: str, where_val: str):
    cursor.execute(f"UPDATE {table} SET {columns[0]} = '{values[0]}', {columns[1]} = '{values[1]}', {columns[2]} = '{values[2]}' WHERE {where_col} = '{where_val}'")
    conn.commit()



def update_columns(table: str, column: str, where_col: str, where_val: str, val:str):
    cursor.execute(f"UPDATE {table} SET {column} = '{val}' WHERE {where_col} = '{where_val}'")
    conn.commit()


def update_columns_and(table: str, column: str, where_col: str, where_val: str, val:str, where_col1: str, where_val1: str):
    cursor.execute(f"UPDATE {table} SET {column} = '{val}' WHERE {where_col} = '{where_val}' AND {where_col1} = {where_val1}")
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


def fetch_new_words_all(table: str, columns: List[str], user_id: str, code:str) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE words.id NOT IN (SELECT word_id from users_words WHERE user_id = {user_id}) AND words.category_id = {code}")
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
    """???????????????????????????? ????"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """??????????????????, ???????????????????????????????? ???? ????, ???????? ?????? ??? ????????????????????????????"""
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

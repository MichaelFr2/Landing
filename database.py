import sqlite3

DB_NAME = 'users.db'

def init_vacancies_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {'Employers'}(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            premium BOOL DEFAULT FALSE,
            new_user BOOl DEFAULT TRUE,
            tutorial_complete BOOl DEFAULT 0,
            date_of_registration TEXT
        );
    """)




    connect.commit()
    connect.close()

def init_response_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {'Responses'}(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
            name TEXT NOT NULL,
            email TEXT  NOT NULL,
            tel TEXT NOT NULL,
            req_type TEXT NOT NULL,
            comment TEXT,
            date_of_recieve TEXT
        );
    """)
    connect.commit()
    connect.close()

def init_request_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {'Requests'}(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
            req_id TEXT NOT NULL,
            name TEXT NOT NULL,
            company TEXT  NOT NULL,
            quantity TEXT  NOT NULL,
            english_level TEXT NOT NULL,
            required_skill TEXT NOT NULL,
            position TEXT NOT NULL,
            date_of_recieve TEXT,
            req_edu TEXT NOT NULL,
            req_work_exp TEXT,
            req_comment TEXT,
            vacancy_id TEXT NOT NULL,
            client_id TEXT NOT NULL
        );
    """)
    connect.commit()
    connect.close()

def init_tech_skill_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {'Tech_skills'}(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
            req_id TEXT NOT NULL,
            client_id TEXT NOT NULL,
            name TEXT NOT NULL,
            date_of_recieve TEXT

        );
    """)
    connect.commit()
    connect.close()

def init_soft_skill_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {'Soft_skills'}(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
            req_id TEXT NOT NULL,
            client_id TEXT NOT NULL,
            name TEXT NOT NULL,
            date_of_recieve TEXT

        );
    """)
    connect.commit()
    connect.close()

def init_language_skill_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {'Language_skills'}(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
            req_id TEXT NOT NULL,
            client_id TEXT NOT NULL,
            name TEXT NOT NULL,
            date_of_recieve TEXT

        );
    """)
    connect.commit()
    connect.close()


def delete_table(table):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table};")
    connect.commit()
    connect.close()


def display_table(table):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM {table};")
    rows = cursor.fetchall()
    return rows


def get_table_columns(table):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    table_info_sql_command = f"PRAGMA table_info({table});"
    cursor.execute(table_info_sql_command)
    row = cursor.fetchall()
    connect.close()
    return [ table_info[1] for table_info in row ]


def insert(table, insert_values):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    columns = ", ".join(insert_values.keys())
    placeholders = ", ".join("?" * len(insert_values.keys()))
    values = tuple(insert_values.values())
    sql_insert_command = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
    cursor.execute(sql_insert_command, values)
    connect.commit()
    connect.close()



def update(table, new_values, where):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    columns_equal = [f"{column}=?" for column, value in new_values.items()]
    placeholders = ", ".join(columns_equal)
    conditions = [f"{key} = '{value}'" for key, value in where.items()]
    conditions = " AND ".join(conditions)
    values = tuple(new_values.values())
    sql_update_command = f"UPDATE {table} SET {placeholders} WHERE {conditions};"
    cursor.execute(sql_update_command, values)
    connect.commit()
    connect.close()

def get_values(table, columns="*", where={}):
    try:
        connect = sqlite3.connect(DB_NAME)
        cursor = connect.cursor()
        if columns == "*": columns = get_table_columns(table)
        where_placeholder = "WHERE"
        if where == {}: where_placeholder = ""
        column_names = ", ".join(columns)
        conditions = [f"{key} = '{value}'" for key, value in where.items()]
        conditions = " AND ".join(conditions)
        get_user_sql_command = f"SELECT {column_names} FROM {table} {where_placeholder} {conditions};"
        cursor.execute(get_user_sql_command)
        rows = cursor.fetchall()
        connect.close()
        return [dict(zip(columns, row)) for row in rows]
    except sqlite3.Error as e:
        print("???????????? ?????????????????? ???????????? ???? ???? "+str(e))
    return False

def employer_exists(where):
    found_instances = get_values("Employers", ["email"], where=where)
    return not len(found_instances) == 0

def init_db_tables():
    init_vacancies_table()
    init_response_table()
    init_request_table()
    init_language_skill_table()
    init_tech_skill_table()
    init_soft_skill_table()

def delete_db_tables():
    delete_table("Requests")
    delete_table("Language_skills")
    delete_table("Tech_skills")
    delete_table("Soft_skills")
    delete_table("Employers")
    delete_table("Responses")




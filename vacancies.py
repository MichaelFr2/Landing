import sqlite3

DB_NAME = 'users.db'

## Init Tables
def init_vacancies_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Orders'}(
        vacancy_id INTEGER PRIMARY KEY NOT NULL, 
        employer_login TEXT, 
        employer_name TEXT,
        company_name TEXT,
        quantity INTEGER,
        english_level TEXT,
        position TEXT,
        developer BOOL DEFAULT 0,
        analyst BOOL DEFAULT 0,
        qa BOOL DEFAULT 0,
        ui_ux BOOL DEFAULT 0,
        dev_ops BOOL DEFAULT 0,
        tech_manager BOOL DEFAULT 0,
        product_manager BOOL DEFAULT 0,
        data_scientist BOOL DEFAULT 0,
        other_skill TEXT,
        date_of_creation TEXT,
        FOREIGN KEY(employer_login) REFERENCES Employers(login)
    );""")

    connect.commit()
    connect.close()

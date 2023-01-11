import sqlite3
from dicts import *
DB_NAME = 'users.db'

import datetime
from employee_database import *

## Init Tables
def init_vacancies_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Employers'}(
        employer_id INTEGER PRIMARY KEY NOT NULL, 
        premium BOOL,
        first_name TEXT, 
        last_name TEXT,
        login TEXT,
        date_of_registration TEXT,
        date_of_subscribe TEXT,
        prolongating_vacacny_id INTEGER,
        FOREIGN KEY(prolongating_vacacny_id) REFERENCES Vacancies(vacancy_id)
    );""")

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Vacancies'}(
        vacancy_id INTEGER NOT NULL, 
        employer_login TEXT, 
        employer_name TEXT,
        quantity TEXT,
        english_level TEXT,
        position TEXT,
        email TEXT,
        creation_date TEXT,
        FOREIGN KEY(employer_login) REFERENCES Employers(employer_id)
    );""")

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Vacancy_skills'}(
        vacancy_id INTEGER NOT NULL, 
        employer_id INTEGER NOT NULL, 
        qa BOOL DEFAULT 0,
        ui_ux BOOL DEFAULT 0,
        dev_ops BOOL DEFAULT 0,
        tech_manager BOOL DEFAULT 0,
        product_manager BOOL DEFAULT 0,
        data_scientist BOOL DEFAULT 0,
        user_option TEXT NULL,
        FOREIGN KEY(vacancy_id) REFERENCES Vacancies(vacancy_id)
    );""")

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Vacancy_developer_skills'}(
        vacancy_id INTEGER NOT NULL, 
        employer_id INTEGER NOT NULL, 
        c_sharp BOOL DEFAULT 0,
        cpp BOOL DEFAULT 0,
        erlang BOOL DEFAULT 0,
        go BOOL DEFAULT 0,
        html_css BOOL DEFAULT 0,
        java BOOL DEFAULT 0,
        java_script BOOL DEFAULT 0,
        kotlin BOOL DEFAULT 0,
        node_js BOOL DEFAULT 0,
        php BOOL DEFAULT 0,
        python BOOL DEFAULT 0,
        ruby BOOL DEFAULT 0,
        swift BOOL DEFAULT 0,
        ios BOOL DEFAULT 0,
        android BOOL DEFAULT 0,
        user_option TEXT,
        FOREIGN KEY(vacancy_id) REFERENCES Vacancy_skills(vacancy_id)
    );""")

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Vacancy_analyst_skills'}(
        vacancy_id INTEGER NOT NULL, 
        employer_id INTEGER NOT NULL, 
        systems BOOl DEFAULT 0,
        business BOOl DEFAULT 0,
        FOREIGN KEY(vacancy_id) REFERENCES Vacancy_skills(vacancy_id)
        FOREIGN KEY(employer_id) REFERENCES Vacancy_skills(employer_id)
    );""")

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Views'}(
        employer_id INTEGER NOT NULL, 
        vacancy_id INTEGER NOT NULL, 
        employee_id INTEGER NOT NULL,
        FOREIGN KEY(employee_id) REFERENCES Vacancy_skills(vacancy_id)
        FOREIGN KEY(vacancy_id) REFERENCES Vacancy_skills(vacancy_id)
        FOREIGN KEY(employer_id) REFERENCES Employees(employee_id)
    );""")

    connect.commit()
    connect.close()

# Employer functions

def get_vacancies_of_employer(employer_id):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    if_exists_sql_command = f"SELECT vacancy_id FROM Vacancies WHERE employer_id = {employer_id}"
    cursor.execute(if_exists_sql_command)
    row = cursor.fetchall()
    connect.close()
    return row

def get_unfinished_vacancies_of_employer(employer_id):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    if_exists_sql_command = f"SELECT vacancy_id FROM Vacancies WHERE employer_id = {employer_id} AND paid = 0 LIMIT 1;"
    cursor.execute(if_exists_sql_command)
    row = cursor.fetchall()
    connect.close()
    return row

def init_vacancy_skill_table(employer_id, vacancy_id):
    for skill_table in ["Vacancy_skills", "Vacancy_developer_skills", "Vacancy_analyst_skills"]:
        insert(skill_table, {"employer_id": employer_id, 'vacancy_id': vacancy_id})


def employer_exists(employer_id):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    if_exists_sql_command = f"SELECT employer_id FROM Employers WHERE employer_id = {employer_id}"
    cursor.execute(if_exists_sql_command)
    row = cursor.fetchall()
    connect.close()
    return not row == []


def vacancy_exists(employer_id, vacancy_id):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    if_exists_sql_command = f"SELECT vacancy_id FROM Vacancies WHERE employer_id = {employer_id} AND vacancy_id = {vacancy_id};"
    cursor.execute(if_exists_sql_command)
    row = cursor.fetchall()
    connect.close()
    return not row == []

def add_employer(employer_id, values):
    TABLE = "Employers"
    values['employer_id'] = employer_id
    if not employer_exists(employer_id):
            values['premium'] = 0
            values['date_of_registration'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            insert(TABLE, values)
    elif get_values(TABLE, values.keys(), where={"employer_id": employer_id}) != values:
            update(TABLE, values, where={'employer_id': employer_id})

def employer_want_vacancy(employer_id, vacancy_info):
    recent_vacancies = get_unfinished_vacancies_of_employer(employer_id)
    if recent_vacancies == [] or recent_vacancies == None:
        done_vacancies = get_vacancies_of_employer(employer_id)
        if done_vacancies != [] and done_vacancies != None:
            vacancy_id = max(done_vacancies)[0] + 1
        else:
            vacancy_id = 1

        vacancy_info['vacancy_id'] = vacancy_id
        vacancy_info['paid'] = False
        vacancy_info['done'] = False
        vacancy_info['active'] = False
        insert("Vacancies", vacancy_info)
        init_vacancy_skill_table(employer_id, vacancy_id)

def get_vacancy_info(table, employer_id, columns):
    vacancy_id = get_unfinished_vacancies_of_employer(employer_id)[0][0]
    return get_values(table, columns,
               where={"employer_id": employer_id, "vacancy_id": vacancy_id})


def update_employer(employer_id, new_values):
    TABLE = "Employers"
    if employer_exists(employer_id):
        if get_values(TABLE, new_values.keys(), where={"employer_id": employer_id}) != new_values:
            update(TABLE, new_values, where={'employer_id': employer_id})
            return "Done"
        else:
            return "Nothing changed"
    else:
        return "User not found"

def update_vacancy(employer_id, new_values):
    TABLE = "Vacancies"
    vacancy_id = get_unfinished_vacancies_of_employer(employer_id)[0][0]
    if vacancy_exists(employer_id, vacancy_id):
        if get_values(TABLE, new_values.keys(), where={"employer_id": employer_id, "vacancy_id": vacancy_id}) != new_values:
            update(TABLE, new_values, where={'employer_id': employer_id, "vacancy_id": vacancy_id})
            return "Done"
        else:
            return "Nothing changed"
    else:
        return "User not found"

def change_vacancy(employer_id, vacancy_id, new_values):
    TABLE = "Vacancies"
    if vacancy_exists(employer_id, vacancy_id):
        if get_values(TABLE, new_values.keys(), where={"employer_id": employer_id, "vacancy_id": vacancy_id}) != new_values:
            update(TABLE, new_values, where={'employer_id': employer_id, "vacancy_id": vacancy_id})
            return "Done"
        else:
            return "Nothing changed"
    else:
        return "User not found"

def get_selected_employer_skills(employer_id, section, vacancy_id=None):
    if vacancy_id == None:
        vacancy_id = get_unfinished_vacancies_of_employer(employer_id)[0][0]
    section_columns = get_table_columns(section)
    section_values = get_values(section, section_columns, where={"employer_id": employer_id, 'vacancy_id': vacancy_id})
    section_values.pop("employer_id")
    section_values.pop("vacancy_id")
    selected_columns = [column for column, value in section_values.items() if value == 1]
    if 'user_option' in section_values.keys():
        if section_values['user_option'] != None:
            selected_columns.append(section_values['user_option'])
    return selected_columns

def display_selected_employer_skills(employer_id, section, vacancy_id=None):
    if vacancy_id == None:
        vacancy_id = get_unfinished_vacancies_of_employer(employer_id)[0][0]
    displayed_skills = {}
    section_columns = get_table_columns(section)
    section_values = get_values(section, section_columns, where={"employer_id": employer_id, 'vacancy_id': vacancy_id})
    section_values.pop("employer_id")
    section_values.pop("vacancy_id")
    translate = inv_translate_employer_skills_columns[section]
    selected_columns = [translate[column] for column, value in section_values.items() if value == 1]
    if selected_columns != []:
        displayed_skills['skills'] = selected_columns
    if 'user_option' in section_values.keys():
        if section_values['user_option'] != None:
            displayed_skills['user_option'] = section_values['user_option']
    return displayed_skills

def get_total_employer_skill_choice(employee_id):
    section_skills = display_selected_employer_skills(employee_id, 'Vacancy_skills')
    developer = display_selected_employer_skills(employee_id, "Vacancy_developer_skills")
    analyst = display_selected_employer_skills(employee_id, "Vacancy_analyst_skills")

    if not section_skills.get("skills", False):
        section_skills["skills"] = []
    if developer != {}:
        section_skills["skills"].append("Developer")
    if analyst != {}:
        section_skills["skills"].append("Analyst")

    return section_skills

def add_employer_skill(employer_id, section, skill):
    vacancy_id = get_unfinished_vacancies_of_employer(employer_id)[0][0]
    translate = translate_employer_skills_columns[section]
    skill = translate[skill]
    if vacancy_exists(employer_id, vacancy_id):
        if skill not in get_selected_employer_skills(employer_id, section):
            update(section, {skill: 1}, where={'employer_id': employer_id, "vacancy_id": vacancy_id})
            return "Added"
        else:
            update(section, {skill: 0}, where={'employer_id': employer_id, "vacancy_id": vacancy_id})
            return "Deleted"
    else:
        return "User not found"

def add_other_employer_skill(employer_id, section, other_skill):
    vacancy_id = get_unfinished_vacancies_of_employer(employer_id)[0][0]
    if vacancy_exists(employer_id, vacancy_id):
        if display_selected_employer_skills(employer_id, section).get('user_option', False):
            update(section, {'user_option': None}, where={'employer_id': employer_id, "vacancy_id": vacancy_id})
            return "Deleted"
        else:
            update(section, {'user_option': other_skill}, where={'employer_id': employer_id, "vacancy_id": vacancy_id})
            return "Added"
    else:
        return "User not found"


def save_vacancy(employer_id, vacancy):
    vacancy_id = get_unfinished_vacancies_of_employer(employer_id)[0][0]
    if vacancy_exists(employer_id, vacancy_id):
        update_vacancy(employer_id, vacancy)
    else:
        return "User not found"


def get_all_finished_vacancies(employer_id):
    where = {"employer_id": employer_id, "active": 0, "paid": 1}
    columns = ["vacancy_id", "name"]
    table = "Vacancies"
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    column_names = ", ".join(columns)
    conditions = [f"{key} = {value}" for key, value in where.items()]
    conditions = " AND ".join(conditions)
    get_user_sql_command = f"SELECT {column_names} FROM {table} WHERE {conditions};"
    cursor.execute(get_user_sql_command)
    rows = cursor.fetchall()
    connect.close()
    return rows

def get_all_active_vacancies():
    columns = ["employer_id", "vacancy_id"]
    where = {"active": 1, "paid": 1}
    table = "Vacancies"
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    column_names = ", ".join(columns)
    conditions = [f"{key} = {value}" for key, value in where.items()]
    conditions = " AND ".join(conditions)
    get_user_sql_command = f"SELECT {column_names} FROM {table} WHERE {conditions};"
    cursor.execute(get_user_sql_command)
    rows = cursor.fetchall()
    connect.close()
    return rows

def check_vacancies():
    where = {"active": 1, "paid": 1}
    conditions = [f"{key} = {value}" for key, value in where.items()]
    conditions = " AND ".join(conditions)
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    get_user_sql_command = f"SELECT vacancy_id, employer_id, date FROM Vacancies WHERE {conditions};"
    cursor.execute(get_user_sql_command)
    rows = cursor.fetchall()
    for vacancy_id, employer_id, vacancy_date in rows:
        date = pd.to_datetime(vacancy_date, format="%Y-%m-%d %H:%M")
        if (datetime.datetime.now()-date).seconds > 60*5:
            new_values = {
                'active': 0
            }
            result = change_vacancy(employer_id, vacancy_id, new_values)

    return "Done"

def get_seen_resumes(employer_id, vacancy_id):
    table = "Views"
    where = {"employer_id": employer_id, "vacancy_id": vacancy_id}
    columns = ["employee_id"]
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    column_names = ", ".join(columns)
    conditions = [f"{key} = {value}" for key, value in where.items()]
    conditions = " AND ".join(conditions)
    get_user_sql_command = f"SELECT {column_names} FROM {table} WHERE {conditions};"
    cursor.execute(get_user_sql_command)
    rows = cursor.fetchall()
    connect.close()
    return [row[0] for row in rows]


def see_employee(employer_id, vacancy_id, employee_id):
    TABLE = "Views"
    new_values = {
        "employer_id": employer_id,
        "vacancy_id": vacancy_id,
        "employee_id":  employee_id
    }
    insert(TABLE, new_values)
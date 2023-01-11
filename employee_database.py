import sqlite3
DB_NAME = 'users.db'

## Init Tables
def init_employee_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Employees'}(
        employee_id INTEGER PRIMARY KEY NOT NULL, 
        first_name TEXT, 
        last_name TEXT,
        username TEXT,
        relocate_option TEXT,
        english_level TEXT,
        level TEXT,
        resume_file BLOB,
        resume_file_name TEXT,
        date TEXT
    );""")

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Skills'}(
        employee_id INTEGER PRIMARY KEY NOT NULL,
        qa BOOL DEFAULT 0,
        ui_ux BOOL DEFAULT 0,
        dev_ops BOOL DEFAULT 0,
        tech_manager BOOL DEFAULT 0,
        product_manager BOOL DEFAULT 0,
        data_scientist BOOL DEFAULT 0,
        user_option TEXT NULL,
        FOREIGN KEY(employee_id) REFERENCES Employees(employee_id)
    );""")

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Developer_skills'}(
        employee_id INTEGER PRIMARY KEY NOT NULL,
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
        user_option TEXT NULL,
        FOREIGN KEY(employee_id) REFERENCES Skills(skill_id)
    );""")

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Analyst_skills'}(
        employee_id INTEGER PRIMARY KEY NOT NULL,
        systems BOOl DEFAULT 0,
        business BOOl DEFAULT 0,
        FOREIGN KEY(employee_id) REFERENCES Skills(skill_id)
    );""")

    connect.commit()
    connect.close()

## Main functions
def delete_table(table):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table};")
    connect.commit()
    connect.close()


def delete_all_tables():
    for table in ["Employees", "Skills", "Developer_skills", "Analyst_skills",
                  "Employers", "Vacancies", "Vacancy_skills", "Vacancy_developer_skills", "Vacancy_analyst_skills", "Views"]:
        delete_table(table)

def display_table(table):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM {table};")
    rows = cursor.fetchall()
    return rows

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
    conditions = [f"{key} = {value}" for key, value in where.items()]
    conditions = " AND ".join(conditions)
    values = tuple(new_values.values())
    sql_update_command = f"UPDATE {table} SET {placeholders} WHERE {conditions};"
    cursor.execute(sql_update_command, values)
    connect.commit()
    connect.close()

def get_values(table, columns, where):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    column_names = ", ".join(columns)
    conditions = [f"{key} = {value}" for key, value in where.items()]
    conditions = " AND ".join(conditions)
    get_user_sql_command = f"SELECT {column_names} FROM {table} WHERE {conditions};"
    cursor.execute(get_user_sql_command)
    rows = cursor.fetchall()
    connect.close()
    if rows == []:
        rows = [[None]]
    return dict(zip(columns, rows[0]))

def get_table_columns(table):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    table_info_sql_command = f"PRAGMA table_info({table});"
    cursor.execute(table_info_sql_command)
    row = cursor.fetchall()
    connect.close()
    return [ table_info[1] for table_info in row ]

# Employees functions
def init_employee_skill_table(employee_id):
    for skill_table in ["Skills", "Developer_skills", "Analyst_skills"]:
        insert(skill_table, {"employee_id": employee_id})

def employee_exists(employee_id):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    if_exists_sql_command = f"SELECT employee_id FROM Employees WHERE employee_id = {employee_id} LIMIT 1;"
    cursor.execute(if_exists_sql_command)
    row = cursor.fetchall()
    connect.close()
    return not row == []

def if_value_present(table, column, where):
    column_name = list(column.keys())[0]
    column_value = column[column_name]
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    conditions = [f"{key} = {value}" for key, value in where.items()]
    conditions = " AND ".join(conditions)
    get_user_sql_command = f"SELECT {column_name} FROM {table} WHERE {conditions};"
    cursor.execute(get_user_sql_command)
    rows = cursor.fetchall()
    for db_value in rows:
        if db_value[0] == column_value:
            connect.close()
            return True
    connect.close()
    return False

def add_employee(employee_id, values):
    TABLE = "Employees"
    values['employee_id'] = employee_id
    if not employee_exists(employee_id):
            insert(TABLE, values)
            init_employee_skill_table(employee_id)
    elif get_values(TABLE, values.keys(), where={"employee_id": employee_id}) != values:
            update(TABLE, values, where={'employee_id': employee_id})


def update_employee(employee_id, new_values):
    TABLE = "Employees"
    if employee_exists(employee_id):
        if get_values(TABLE, new_values.keys(), where={"employee_id": employee_id}) != new_values:
            update(TABLE, new_values, where={'employee_id': employee_id})
            return "Done"
        else:
            return "Nothing changed"
    else:
        return "User not found"

def get_selected_employee_skills(employee_id, section):
    section_columns = get_table_columns(section)
    section_values = get_values(section, section_columns, where={"employee_id": employee_id})
    selected_columns = [column for column, value in section_values.items() if value == 1]
    if 'user_option' in section_values.keys():
        if section_values['user_option'] != None and section_values['user_option'] != '0':
            selected_columns.append(section_values['user_option'])
    return selected_columns

def display_selected_employee_skills(employee_id, section):
    displayed_skills = {}
    section_columns = get_table_columns(section)
    section_columns.remove("employee_id")
    section_values = get_values(section, section_columns, where={"employee_id": employee_id})
    translate = inv_translate_employee_skills_columns[section]
    selected_columns = [translate[column] for column, value in section_values.items() if value == 1]
    if selected_columns != []:
        displayed_skills['skills'] = selected_columns
    if 'user_option' in section_values.keys():
        if section_values['user_option'] != None and section_values['user_option'] != '0':
            displayed_skills['user_option'] = section_values['user_option']
    return displayed_skills

def get_total_employee_skill_choice(employee_id):
    section_skills = display_selected_employee_skills(employee_id, 'Skills')
    developer = display_selected_employee_skills(employee_id, "Developer_skills")
    analyst = display_selected_employee_skills(employee_id, "Analyst_skills")

    if not section_skills.get("skills", False):
        section_skills["skills"] = []
    if developer != {}:
        section_skills["skills"].append("Developer")
    if analyst != {}:
        section_skills["skills"].append("Analyst")

    return section_skills

def add_employee_skill(employee_id, section, skill):
    translate = translate_employee_skills_columns[section]
    skill = translate[skill]
    if employee_exists(employee_id):
        if skill not in get_selected_employee_skills(employee_id, section):
            update(section, {skill: 1}, where={'employee_id': employee_id})
            return "Added"
        else:
            update(section, {skill: 0}, where={'employee_id': employee_id})
            return "Deleted"
    else:
        return "User not found"

def add_other_employee_skill(employee_id, section, other_skill):
    if employee_exists(employee_id):
        if display_selected_employee_skills(employee_id, section).get('user_option', False):
            update(section, {'user_option': None}, where={'employee_id': employee_id})
            return "Deleted"
        else:
            update(section, {'user_option': other_skill}, where={'employee_id': employee_id})
            return "Added"
    else:
        return "User not found"

def save_resume(employee_id, resume):
    update("Employees", resume, where={'employee_id': employee_id})


def get_registered_employees():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    get_user_sql_command = f"SELECT * FROM Employees WHERE resume_file IS NOT NULL;"
    query = cursor.execute(get_user_sql_command)
    cols = [column[0] for column in query.description]
    df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    return df


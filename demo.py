from flask import Flask, redirect, abort, url_for, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

import json
from markupsafe import escape

import datetime
import html
from mail_service import *
from dicts import *
from employee_database import *
from database import *
import ast

import jinja2
jinja2.filters.FILTERS['to_json'] = lambda s: json.dumps(s)

SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'


init_db_tables()

app = Flask(__name__)
app.config.from_object(__name__)


login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)

@app.route("/test", methods=['GET', 'POST'])
def test():
    return render_template('resume-page 3.html')


@app.route("/")
def hello_world():
    return redirect(url_for('main'))

@app.route("/home/")
@login_required
def home():
    logout_user()
    return redirect(url_for('login'))

@app.route("/main", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':

        name = str(escape(request.form.get('name')))
        email = str(escape(request.form.get('email')))
        tel = str(escape(request.form.get('tel')))
        req_type = str(escape(request.form.get('req_type')))
        comment = str(escape(request.form.get('comment')))
        response_info = {
             "name": name,
             "email": email,
             "tel": tel,
            "req_type": req_type,
            "comment": comment,
            "date_of_recieve": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        insert("Responses", response_info)
        send_response(name, email, tel, req_type, comment)

        return render_template('main.html')
    else:
        return render_template('main.html')




@app.route("/outstaff", methods=['GET', 'POST'])
def outstaff():
    if request.method == 'POST':

        name = str(escape(request.form.get('name')))
        email = str(escape(request.form.get('email')))
        tel = str(escape(request.form.get('tel')))
        req_type = str(escape(request.form.get('req_type')))
        comment = str(escape(request.form.get('comment')))
        response_info = {
             "name": name,
             "email": email,
             "tel": tel,
            "req_type": req_type,
            "comment": comment,
            "date_of_recieve": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        insert("Responses", response_info)
        send_response(name, email, tel, req_type, comment)

        return render_template('outstaff.html')
    else:
        return render_template('outstaff.html')



@app.route("/payroll", methods=['GET', 'POST'])
def payroll():
    if request.method == 'POST':

        name = str(escape(request.form.get('name')))
        email = str(escape(request.form.get('email')))
        tel = str(escape(request.form.get('tel')))
        req_type = str(escape(request.form.get('req_type')))
        comment = str(escape(request.form.get('comment')))
        response_info = {
             "name": name,
             "email": email,
             "tel": tel,
            "req_type": req_type,
            "comment": comment,
            "date_of_recieve": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        insert("Responses", response_info)
        send_response(name, email, tel, req_type, comment)

        return render_template('payroll.html')
    else:
        return render_template('payroll.html')

@app.route("/payrollPageForm", methods=['GET', 'POST'])
def payrollPageForm():
    if request.method == 'POST':

        name = str(escape(request.form.get('name')))
        email = str(escape(request.form.get('email')))
        tel = str(escape(request.form.get('tel')))
        comment = str(escape(request.form.get('comment')))
        req_type = "payroll"
        response_info = {
             "name": name,
             "email": email,
             "tel": tel,
            "req_type": req_type,
            "comment": comment,
            "date_of_recieve": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        insert("Responses", response_info)
        send_response(name, email, tel, req_type, comment)

        return render_template('payroll.html')
    else:
        return render_template('payroll.html')

# Line

@app.route("/registration", methods=['GET', 'POST'])
def add_new_user():
    if request.method == 'POST':
        #company_name = escape(request.form.get('company_name'))
        # login = escape(request.form.get('login'))
        email = escape(request.form.get('email'))
        password = escape(request.form.get('password'))
        password_repeat = escape(request.form.get('password-repeat'))

        if password != password_repeat:
            return render_template('registration.html', error=escape(PASSWORD_MATCH_ERROR))
        if email == None or password == None:
            return render_template('registration.html', error=escape(MISSING_FIELD_ERROR))
        # if employer_exists(where={"login": login}):
        #     return render_template('registration.html', error=escape(LOGIN_EXISTS_ERROR))
        if employer_exists(where={"email": email}):
            return render_template('registration.html', error=escape(EMAIL_EXISTS_ERROR))

        user_info = {
            # "company_name": 1,
            # "login": login,
            "email": email,
            "password": generate_password_hash(password),
            "date_of_registration": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        insert("Employers", user_info)

        if employer_exists(where={"email": email}):
            return redirect(url_for('login'))
        else:
            # TO DO
            abort(404)
    else:
        if current_user.is_authenticated:
             return redirect(url_for('form'))
        return render_template('registration.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = escape(request.form.get('login'))
        password = escape(request.form.get('password'))

        if employer_exists(where={"email": login}):
            user = get_values("Employers", where={"email": login})[0]
            if user and check_password_hash(user["password"], password):
                userlogin = UserLogin().create(user)
                login_user(userlogin, remember=True)


                return redirect(url_for('form'))
            else:
                return render_template('login.html', error=escape(INVALID_PASSWORD_ERROR))

        else:
            return render_template('login.html', error=escape(USER_NOT_FOUND_ERROR))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('form'))
        return render_template('login.html')


@app.route("/form", methods=['GET', 'POST'])
@login_required
def form():
    if request.method == 'POST':
        name = str(escape(request.form.get('name')))
        company = str(escape(request.form.get('company')))
        quantity = str(escape(request.form.get('quantity')))
        english_level = str(escape(request.form.get('english_level')))
        
        required_skill = str(escape(request.form.get('skill_checked')))

        position = escape(request.form.get('position'))

        login = current_user.get_id()

        vacancy_request = {
            "name": name,
            "company": company,
            "quantity": quantity,
            "english_level": english_level,
            "required_skill": required_skill,
            "position": position,
            "tutorial_complete": get_values("Employers", ["tutorial_complete"], where={"email": login})[0]["tutorial_complete"]
        }

        options = {
            "english_level": ["A1", "A2", "B1", "B2", "C1", "C2"],
            "work_experience": list(range(10)),
            "education": ["Economics", "Technical", "Design", "Management", "Not matter"]
        }

        with open('fake2.json') as f:
            vacancies = json.load(f)

        suggested_vacancy = None

        desired_vacancy_name = MATCHING.get(required_skill, None)

        for vacancy in vacancies:
            if (vacancy["position_name"] == desired_vacancy_name) and (vacancy["position"].lower() == position or vacancy["position"].lower() == "any"):
                suggested_vacancy = vacancy

        if suggested_vacancy == None:
            return "Didnt found any vacancy"
        else:
            session["technology_stack"] = suggested_vacancy["technology_stack"]
            session["soft_skills"] = suggested_vacancy["soft_skills"]
            session["language_skills"] = []
            session["tutorial_complete"] = get_values("Employers", ["tutorial_complete"], where={"email": login})[0]["tutorial_complete"]
            session["suggested_vacancy"] = suggested_vacancy
            session["options"] = options
            session["bd"] = vacancy_request
            session["vacancy_id"] = suggested_vacancy["id"]

            return redirect(url_for('loading'))
    else:
        return render_template('form.html', menu=MENU)


@app.route("/loading", methods=['GET', 'POST'])
def loading():
    return render_template('load_page.html')


@app.route("/presentation", methods=['GET', 'POST'])
def presentation():
    login = current_user.get_id()

    if get_values("Employers", ["new_user"], where={"email": login})[0]["new_user"]:
        new_info = {"new_user": False}
        update("Employers", new_info, where={"email": login})
        return render_template('form_AI.html')
    else:
        return redirect(url_for('suggested_vacancy'))


@app.route("/suggested_vacancy", methods=['GET', 'POST'])
@login_required
def suggested_vacancy():

    if request.method == 'POST':
        request_f = session["bd"]
        tech_skills = session["technology_stack"]
        language_skills = session["language_skills"]
        soft_skills = session["soft_skills"]
        vacancy_id = session["vacancy_id"]

        req_id = get_values("Requests", ["req_id"], where={"client_id": current_user.get_id()})
        if len(req_id) == 0: req_id = 1
        else:
            req_id = int(req_id[-1]["req_id"]) + 1

        req_edu = str(escape(request.form.get('req_edu')))
        req_work_exp = str(escape(request.form.get('req_work_exp')))
        req_comment = str(escape(request.form.get('req_comment')))



        vacancy_req = {
            "req_id": req_id,
            "name": request_f["name"],
            "company": request_f["company"],
            "quantity": request_f["quantity"],
            "english_level": request_f["english_level"],
            "required_skill": request_f["required_skill"],
            "position": request_f["position"],
            "req_edu": req_edu,
            "req_work_exp": req_work_exp,
            "client_id": current_user.get_id(),
            "req_comment": req_comment,
            "vacancy_id": vacancy_id,
            "date_of_recieve": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        for skill in tech_skills:
            tech_skill = {
                "name": skill,
                "req_id": req_id,
                "client_id": current_user.get_id(),
                "date_of_recieve": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            insert("Tech_skills", tech_skill)

        for skill in soft_skills:
            soft_skill = {
                "name": skill,
                "req_id": req_id,
                "client_id": current_user.get_id(),
                "date_of_recieve": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            insert("Soft_skills", soft_skill)

        for skill in language_skills:
            language_skill = {
                "name": skill,
                "req_id": req_id,
                "client_id": current_user.get_id(),
                "date_of_recieve": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            insert("Language_skills", language_skill)




        insert("Requests", vacancy_req)
        # return render_template("resume-page 4.html", tutorial_complete=session["tutorial_complete"],
        #                        vacancy=session["suggested_vacancy"], options=session["options"])
        return redirect(url_for('flying'))
    else:
        print(type(session["tutorial_complete"]))
        return render_template("resume-page 4.html", tutorial_complete=session["tutorial_complete"],
                               vacancy=session["suggested_vacancy"], options=session["options"])




@app.route("/add_skills", methods=['GET', 'POST'])
def add_skills():


    if request.method == 'GET':
        skill = request.args.get('skill')
        section = request.args.get('section')
        if skill != '':
            lst = session[section]

            if skill not in lst:
                lst += [skill]

                session[section] = lst

        return render_template('skill_stack_window.html', skill_section=session[section], section=section)


@app.route("/delete_skills", methods=['GET', 'POST'])
def delete_skills():
    if request.method == 'GET':
        skill = request.args.get('skill')
        section = request.args.get('section')

        lst = session[section]
        lst.remove(skill)
        session[section] = lst

        print(session[section])

        return render_template('skill_stack_window.html', skill_section=session[section], section=section)


@app.route("/flying", methods=['GET', 'POST'])
def flying():
    login = current_user.get_id()
    if not get_values("Employers", ["tutorial_complete"], where={"email": login})[0]["tutorial_complete"] :
        new_info = {"tutorial_complete": True}
        update("Employers", new_info, where={"email": login})
    return render_template('flying.html')

@app.route("/questions", methods=['GET', 'POST'])
def questions():
    return render_template('questions.html')

@app.route("/delete_db", methods=['GET', 'POST'])
def delete_db():
    delete_table("Employers")
    init_vacancies_table()
    return "DB deleted"



@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':

        name = str(escape(request.form.get('name')))
        email = str(escape(request.form.get('email')))
        tel = str(escape(request.form.get('tel')))
        req_type = str(escape(request.form.get('req_type')))
        comment = str(escape(request.form.get('comment')))
        response_info = {
             "name": name,
             "email": email,
             "tel": tel,
            "req_type": req_type,
            "comment": comment,
            "date_of_recieve": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        insert("Responses", response_info)
        send_response(name, email, tel, req_type, comment)

        return render_template('contact.html')
    else:
        return render_template('contact.html')


if __name__ == "__main__":
    init_vacancies_table()

    app.run(host='127.0.0.1', port=5001, debug=True)


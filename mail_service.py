import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader, select_autoescape

mail_login = 'yui678mf@gmail.com'
mail_password = 'ffjepfbqifozdini'

def send_response(name, email, tel, req_type, comment):
    sender_email = "yui678mf@gmail.com"
    receiver_email = "yui678m@mail.ru"
    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'Response'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    body_text = """
    Name: {name}   \r\n
    Email: {email}   \r\n
    Telephone: {tel}   \r\n
    Request type: {req_type}   \r\n
    Comment: {comment}   \r\n
    """.format(name=name, email=email, tel=tel, req_type=req_type, comment=comment)

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('response_form.html')
    body_html = template.render(name=name, email=email, tel=tel, req_type=req_type, comment=comment)
    msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(mail_login, mail_password)
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(e)

def send_request(init_id, name, company, quantity, english_level, required_skill,
                 position, req_edu, req_work_exp, client_id, req_comment, vacancy_id,
                 tech_skills, soft_skills, language_skills, options):

    sender_email = "yui678mf@gmail.com"
    receiver_email = "yui678m@mail.ru"
    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'Request'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    body_text = """
    Request № {init_id}   \r\n
    Name: {name}   \r\n
    Email: {client_id}   \r\n
    Company: {company}   \r\n
    Quantity: {quantity}   \r\n
    English level: {english_level}   \r\n
    Required skill: {required_skill}   \r\n
    Position: {position}   \r\n
    Required education: {req_edu}   \r\n
    Required working experience: {req_work_exp}   \r\n
    Required tech-skills: {tech_skills}   \r\n
    Required soft-skills: {soft_skills}   \r\n
    Required language-skills: {language_skills}   \r\n
    System vacancy id: {vacancy_id}   \r\n
    Comment: {req_comment}   \r\n
    """.format(init_id=init_id, name=name, company=company, quantity=quantity, english_level=english_level,
               required_skill=options[required_skill] , position=position , req_edu=req_edu,
               req_work_exp=req_work_exp , client_id=client_id, req_comment=req_comment, vacancy_id=vacancy_id,
               tech_skills=tech_skills, soft_skills=soft_skills, language_skills=language_skills, )

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('request_form.html')
    body_html = template.render(init_id=init_id, name=name, company=company, quantity=quantity,
                                english_level=english_level, required_skill=required_skill , position=position ,
                                req_edu=req_edu, req_work_exp=req_work_exp , client_id=client_id,
                                req_comment=req_comment, tech_skills=tech_skills, soft_skills=soft_skills,
                                language_skills=language_skills, vacancy_id=vacancy_id, options=options )

    msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(mail_login, mail_password)
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(e)
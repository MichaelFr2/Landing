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
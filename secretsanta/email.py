import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class email_send():
    def __init__(self, from_address, subject, host_name, port_nbr, login_address, passwd, template_file):
        self.from_address = from_address
        self.subject = subject
        self.host = host_name
        self.port = port_nbr
        self.login = login_address
        self.passwd = passwd
        self.template_file = template_file

    def read_template(self, filename):
        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        self.template = Template(template_file_content)

    def smtp_config(self):
        self.server = smtplib.SMTP(host=self.host, port=self.port)
        self.server.starttls()
        self.server.login(self.login, self.passwd)

    def send_message(self, name, gift_recipient, email):
        msg = MIMEMultipart()       
     
        message_text = message_template.substitute(PERSON_NAME=name)
        message_text = message_template.substitute(GIFT_RECIPIENT=gift_recipient)
        
        msg['From']=self.from_address
        msg['To']=email
        msg['Subject']=self.subject

        msg.attach(MIMEText(message, 'plain'))

        self.server.send_message(msg)
        

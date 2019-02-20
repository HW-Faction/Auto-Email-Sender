import smtplib
import io

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import credentials

import os

# system commands 
clear = 'clear' # clear screen
header = 'sudo ./Header.sh'



def get_contacts(filename):
    names = []
    emails = []
    with io.open(filename, encoding='utf-8') as contacts_file:
        for contact in contacts_file:
            names.append(contact.split()[0])
            emails.append(contact.split()[1])
    return names, emails


def read_template(filename):
   
    with io.open(filename, encoding='utf-8') as template_file:
        template = template_file.read()
    return Template(template)


def main():
    # get names and contact list
    names, emails = get_contacts('my_contacts.txt')
    message_template = read_template('message.txt')

    # setup the SMTP server
    server = smtplib.SMTP(credentials.HOST_NAME, credentials.PORT)
    server.ehlo()
    server.starttls()
    server.login(credentials.EMAIL_ADDRESS, credentials.PASSWORD)

    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message

        # add name to the title
        message = message_template.substitute(PERSON_NAME=name.title())

        # setup the message parameters
        msg['From'] = credentials.EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = 'Auto Email Sender' # change subject here

        # add message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server setup earlier
        server.send_message(msg)
        del msg

    # close the SMTP session and close the connection
    server.quit()

os.system(header)
print('-'*128)


if __name__ == '__main__':
    main()


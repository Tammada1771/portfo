from datetime import datetime
from email.message import EmailMessage, Message
from string import Template
from pathlib import Path
import smtplib
import csv
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        date = data['date']
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(
            f'\n Recieved on: {date} \n Email: {email} \n Subject: {subject} \n Message: {message} \n')


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database_csv:
        date = data['date']
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(
            database_csv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([date, email, subject, message])


def send_sms(data):
    email = data['email']
    subject = data['subject']
    message = data['message']
    text = (
        f'\n Email: {email} \n Subject: {subject} \n Message: {message} \n')
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login('tammingaar@gmail.com', 'test1234!')
    server.sendmail('tammingaar@gmail.com',
                    '2623585391@vzwpix.com', text)


def send_email(data):
    senderemail = data['email']
    subject = data['subject']
    message = data['message']

    email = EmailMessage()
    email['to'] = 'Tammingaar@gmail.com'
    email['from'] = senderemail
    email['subject'] = subject

    email.set_content(
        f'\n Email: {senderemail} \n Subject: {subject} \n Message: {message} \n')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        # tammingaar@gmail.com
        # test1234!
        smtp.login('tammingaar@gmail.com', 'test1234!')
        smtp.send_message(email)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            data['date'] = datetime.now()
            write_to_file(data)
            write_to_csv(data)
            # send_sms(data)
            send_email(data)
            return redirect('/thank_you.html')
        except:
            return 'Did not save to DB'
    else:
        return 'Something wrong'

import time
import pandas as pd
import re
import speech_recognition as sr
import pyttsx3
import nltk
import smtplib
import imaplib
import email
import requests
import bs4
import datetime as dt
import random
# nltk.download('vader_lexicon') #use this for first time installation alone

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from accounts import patients, doctors

from rooms import *
from intents_responses_copy import *
from chitchat import chit_chat
from email.message import EmailMessage
from stress_test import *

mail = EmailMessage()


def voice_output(msg):
    engine = pyttsx3.init()
    engine.setProperty('rate', 135)
    engine.setProperty('volume', 0.7)
    engine.say(str(msg))
    engine.runAndWait()


def get_mail(username, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')
    _, search_data = mail.search(None, 'UNSEEN')
    inbox = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
        inbox.append(email_data)

    return inbox


def read_mail(username, password):
    print('Please wait, messages are being loaded for you')
    voice_output('Please wait messages are being loaded for you')
    messages = get_mail(username, password)

    if len(messages) != 0:
        for num in messages:
            sender = 'Message from ' + num['from']
            print('Assistant : {}'.format(sender))
            voice_output(sender)
            print('Assistant : {}'.format(num['body']))
            voice_output(num['body'])
    else:
        print('No new messages are in your inbox')
        voice_output('No new messages are in your inbox')


def sender(p_id, p_pwd, p_to, msg, name):

    if p_id != 0:
        voice_output('Please wait I am processing your message to send')
        try:
            mailServer = smtplib.SMTP('smtp.gmail.com', 587)
            mailServer.starttls()
            mailServer.login(p_id, p_pwd)
            mailServer.sendmail(p_id, p_to, msg)
            voice_output('Message sent to ' + name + ' successfully')
            print('Assistant : Message sent ' + name + ' successfully')
        except:
            print('Assistant : Unable to send your message due to network issue, Please try again')
            voice_output('Assistant : Unable to send your message due to network issue, Please try again')


def call_doctor(p_id, p_pwd):
    p_to, name = 0, 0
    print('Doctor Names ')
    doctors_names = ['doctor_1', 'doctor_2', 'doctor_3', 'doctor_4']
    print(doctors_names)
    voice_output( 'Tell from above list which doctor you want to speak')
    print("Assistant : Tell from above list which doctor you want to speak")
    user_input = speech_input(listen=4)
    word = user_input.lower().split()
    for i in word:
        if i in doctors_names:
            name = i
            p_to = doctors[i]
    if p_to == 0:
        p_to = doctors['default_doctor']
    voice_output('Tell your message to the doctor')
    print('Assistant : Tell your message to the doctor')
    msg = speech_input(listen=5)

    return sender(p_id, p_pwd, p_to, msg, name)


def match_room(msg, room_pattern):
    msg = msg.lower()
    matched_intent = None
    for intent, pattern in room_pattern.items():
        if re.search(pattern, msg):
            matched_intent = intent

    return matched_intent


def match_intent(msg, patterns):
    msg = msg.lower()
    matched_intent = None
    for intent, pattern in patterns.items():
        if re.search(pattern, msg):
            matched_intent = intent

    return matched_intent


def details():
    # global username, password
    username, password=0,0
    room_number = speech_input(listen=3)
    room_number = match_room(room_number, room_pattern)
    if room_number in patients.keys():
        username = patients[room_number][0]
        password = patients[room_number][1]
    else:
        voice_output('Please tell a valid room number in which you are staying')
        print('Assistant : Please tell a valid room number in which you are staying')
        details()

    return username, password, room_number


def respond(msg):
    response_intent = match_intent(msg, patterns)
    keys = 'default'
    if response_intent == 'stop':
        keys = 'stop'
    elif response_intent in responses:
        keys = response_intent

    return keys


def say_emergency(room_no):
    p_id, p_pwd, p_to = 0, 0, 0
    doctor_id = ('default_doctor@hospital.com')
    msg = ('The patient is in emergency! Doctor, His room no is   ' + str(room_no))
    try:
        p_id = patients[room_no][0]
        p_pwd = patients[room_no][1]
        p_to = [doctor_id]
    except:
        print('Error')

    return emergency_sender(p_id, p_pwd, p_to, msg)


def emergency_sender(p_id, p_pwd, p_to, msg):
    if p_id != 0:
        voice_output('Emergency message sending')
        try:
            mailServers = smtplib.SMTP('smtp.gmail.com', 587)
            mailServers.starttls()
            mailServers.login(p_id, p_pwd)
            mailServers.sendmail(p_id, p_to, msg)
            # voice_output('Message sent to ' + name + ' successfully')
            # print('Assistant : Message sent ' + name + ' successfully')
            print("Assistant : Emergency message sent to doctor, the doctor is on his way")
            voice_output("Emergency message sent to doctor, the doctor is on his way")
        except:
            print("Assistant : Could not send the message")
            voice_output("Could not send the message")


def email_notifications(username, password, response, room_number):
    if username == 0:
        username, password, room_number = details()
        if response == 'send':
            call_doctor(username, password)
        else:
            read_mail(username, password)
    else:
        if response == 'send':
            call_doctor(username, password)
        else:
            read_mail(username, password)


def indian_news():
    url = 'https://timesofindia.indiatimes.com/'
    r = requests.get(url)
    page = r.content
    soup = bs4.BeautifulSoup(page, 'html.parser')
    top_news = soup.find('ul', class_="list8").text
    news = top_news.split('\n')
    times_of_india = [line for line in news if line.strip() != ""]
    print('Assistant : Here are the top' + str(len(times_of_india)) + ' headlines from Times of India')
    voice_output('Here are the top' + str(len(times_of_india)) + ' headlines from Times of India')
    for line in times_of_india:
        print(line)
        voice_output(line)


def ask_dt(key):
    now = dt.datetime.now()
    if key == 'time':
        dt_string = now.strftime("%H:%M:%S")
        print("Assistant : The time is {} ".format(dt_string))
        voice_output("The time is:{}" .format(dt_string))
    else:
        dt_string = now.strftime("%d/%m/%Y")
        print("Assistant : The date is {} ".format(dt_string))
        voice_output("The date is:{} ".formar(dt_string))


def sentiment_analyse(sentiment_text):
    result = ''
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neu'] > score['pos'] > score['neg']:
        result = 'negative'
    elif score['pos'] > score['neu'] > score['neg']:
        result = 'positive'
    else:
        result = 'neutral'

    return str(result)


def speech_input(listen):
    r = sr.Recognizer()
    with sr.Microphone() as src:
        print('Listening')
        input_audio = r.record(src, duration=listen)
        converted_text = ''
        try:
            converted_text = r.recognize_google(input_audio)
            print('Speaker : {}'.format(converted_text))
        except:
            print('Going sleep for 3 secs')

    return converted_text


def stress_result_send(p_id, p_pwd, p_to,stress_report,room_number):
    if p_id != 0:
        print('Sending stress test report to the doctor ')
        voice_output('Sending stress test report to the doctor')
        print(p_id)
        print(p_pwd)
        print(p_to)
        print(stress_report)
        print(room_number)
        stress_report1="The stress test of Patient in room number " + str(room_number) + " is" + str(stress_report)
        try:
            mailServer1 = smtplib.SMTP('smtp.gmail.com', 587)
            mailServer1.starttls()
            mailServer1.login(p_id, p_pwd)
            mailServer1.sendmail(p_id, p_to,stress_report1)
            print('Assistant : Stress test sent to the doctor successfully')
            voice_output('Stress test sent to the doctor successfully')
        except:
            print('Assistant : Unable to send your message to the doctor due to network issues, Please try again.')
            voice_output('Unable to send your message to the doctor due to network issues, Please try again')



def stress_test_result(room_number,stress_report):
    p_id, p_pwd, p_to = 0, 0, 0
    doctor_id = "default_doctor@hospital.com"
    if p_id == 0:
        p_id = patients[room_number][0]
        print(p_id)
        p_pwd = patients[room_number][1]
        print(p_pwd)
        p_to = [doctor_id]
        print(p_to)

    return stress_result_send(p_id, p_pwd, p_to, stress_report, room_number)



def room(room_number):
    print("Your room number is: {}".format(room_number))
    voice_output("Your room number is: {}".format(room_number))


def self_intro():
    self_intro=''''Hi, I am your patient monitoring bot.
            These are some of my special abilities.
            I can check your blood pressure, pulse, sentimental analysis and I also can read news, send and recieve messages for you.
            I can also update you with today's date and time.
            If you need me just say the wake up code, 'PM Robot'.
            I will be here for you at anytime, because your health is our only concern.'''
    print(self_intro)
    voice_output(self_intro)


def process_msg(msg):

    gfg = TextBlob(msg)
    gfg = str(gfg.correct())
    a = word_tokenize(gfg)
    lem = WordNetLemmatizer()
    b = []
    for w in a:
        b.append(lem.lemmatize(w))
    c = TreebankWordDetokenizer().detokenize(b)

    return c


print("Please tell PM Robot to start the robot.")
voice_output("Please tell PM Robot to start the robot")
x=1
while True:

    WAKE = "pm robot"
    strt = speech_input(3)
    if strt.count(WAKE) > 0.5:
        speaker = []
        assistant = []
        sentiment = []
        patient_chat = {}
        print('Welcome, I am PM Robot')
        voice_output('Welcome, I am PM Robot')
        print('Assistant : To chat with me tell your room number')
        voice_output('To chat with me tell your room number')
        username, password, room_number = details()
        room_no=room_number
        print("You can chat with me now")
        voice_output('You can chat with me now')
        while x!= "bye":
            msg = speech_input(listen=5)
            preprocess_msg = process_msg(msg)

            if msg!=["bye","quit","exit"]:
                if preprocess_msg != None:
                    key = respond(preprocess_msg)
                    if key == 'stop':
                        break
                    elif (key == 'read') or (key == 'send'):
                        email_notifications(username, password, key, room_number)
                    elif key == 'news':
                        indian_news()
                    elif key == 'emergency':
                        say_emergency(room_number)
                    elif key == 'room_number':
                        room(room_number)
                    elif (key == 'time') or (key == 'date'):
                        ask_dt(key)
                    elif key == 'self_intro':
                        self_intro()
                    elif key == 'stress_test':
                        stress_report=stress_calc()
                        stress_test_result(room_number,stress_report)
                    elif key == 'default':
                        reply = chit_chat(msg)
                        speaker.append(preprocess_msg)
                        assistant.append(reply)
                        sentiment.append(sentiment_analyse(msg))
                    else:
                        response_speech = random.choice(responses[key])
                        print('Assistant : {}'.format(response_speech))
                        voice_output(response_speech)
                        speaker.append(msg)
                        assistant.append(response_speech)
                        sentiment.append(sentiment_analyse(msg))
            else:
                voice_output("bye")
                print("Bye")
                break

                patient_chat['assistant'] = assistant
                patient_chat['speaker'] = speaker
                patient_chat['sentiment'] = sentiment

                chat = pd.DataFrame(patient_chat)
                filename = username.split('@')[0] + '_' + room_number + '.csv'
                chat.to_csv(filename)

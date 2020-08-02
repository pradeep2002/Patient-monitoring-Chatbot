# Patient Monitoring Chatbot

In this Covid-19 pandemic situation, many doctors and health care workers are being affected by this virus. Since they need to interact to know about the patient’s body conditions with time. So the method of interaction will be lost when the contact between the patient is reduced. Here comes our Patient Monitoring chatbot to overcome this problem by performing a set of tasks.

## Task Performed
Here is our Patient Monitoring chatbot, this bot can perform the following tasks

* The chatbot is activated only when the wake word is said for example (“Hey PM Robot”).
* The chatbot then asks for the room number so that it can be used to store the data of the particular patient in that room.
* Patients can also start chatting with the bot like greeting it, chitchat, etc.
* The chatbot is very helpful in reporting the blood pressure, pulse rate, and oxygen level in the blood to the doctor.
* Under the emergency situation, the chatbot will send emergency notifications to the doctor.
* Since the patients are isolated and they are getting stressed very easily,  the chatbot will take a stress test and will report the result to the doctor.
* The chatbot could also send messages to the doctor and read the messages from the patient’s inbox.
* The chatbot will also help the patients with getting the headlines from “The Times of India”  news.
* The chatbot is also capable of telling the current date and time.


## Scope of the project
* Fully voice based chatbot.
* Tests mental-stress analysis of patients.
* Helps to know current top news in India.
* Can send and read email of patients.
* Can send emergency message to doctor.


## Goals of the chatbots
To reduce doctors and health care workers to be affected by Covid-19 spread. The chatbot can also be used to chat with the patients, to make fun with them. The chatbot is used to analyze the stress level of patients and indicate them.


## Technologies and libraries used
Python:
```
import datetime
import random
import re
  ```
  
NLP:
 ```
import nltk
 ```
Web scrapping:
 ```
import bs4
import requests
  ```
 
Email notifications:
 ```
import smtplib
import imaplib
import email
 ```
 
Voice input & output:
 ```
import speech_recognition 
import pyttsx3
import Pyaudio
 ```
 

## Installation of source code from Github

```
git clone https://github.com/pradeep2002/Patient-monitoring-Chatbot.git
cd Patient-monitoring-Chatbot
cd main.py
```

## Datasets
Datasets are already available in this repository.It is enough to train the chatbot.You can also change the dataset according to users convenience .
Orelse if you want to download datasets you may refer,
https://github.com/microsoft/BotBuilder-PersonalityChat/blob/master/CSharp/Datasets/README.md



## Troubleshoots & FAQ
1. Unable to download Pyaudio in command prompt or pycharm
   Download Pyaudio wheel file from here 
   https://pypi.org/project/PyAudio/#files
   Then use the command prompt or terminal to install from wheel file.
   
2. Unable to use datasets available in source code
   Download new datasets from the above-mentioned link, then train the bot.
   
3. Unable to access above mentioned email id
   Change email id according to the user’s  convenience.
   
4. Can't recognize voice properly
   Pronounce correctly in English.
   

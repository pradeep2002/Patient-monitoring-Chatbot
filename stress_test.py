import pandas as pd
import speech_recognition as sr
from stress_intents import *
import pyttsx3


def voice_output(msg):
    engine = pyttsx3.init()
    engine.setProperty('rate', 135)
    engine.setProperty('volume', 0.7)
    engine.say(str(msg))
    engine.runAndWait()


def match_stress(msg, patterns):
    msg = msg.lower()
    matched_intent = None

    for intent, pattern in patterns.items():
        if re.search(pattern, msg):
            matched_intent = intent

    return matched_intent


def user_input(listen):
    r = sr.Recognizer()
    with sr.Microphone() as src:
        print('Listening')
        input_audio = r.record(src, duration=listen)
        converted_text = ''
        Condition, value = 0, 0

    try:
        converted_text = r.recognize_google(input_audio)
        print('Speaker : {}'.format(converted_text))
        condition = match_stress(converted_text, stress_patterns)

        if condition in parameters:
            value = parameters.index(condition)

        else:
            print('Assistant : Please tell from above option')
            voice_output('Please tell from above option')
            user_input(4)
    except:
        print('Assistant : Please tell from above option')
        voice_output('Please tell from above option')
        user_input(4)

    return value


df = pd.read_csv('stress_questions_values.csv')
forward = df[df['values'] == 'forward']
backward = df[df['values'] == 'backward']

forward_questions = forward['question'].to_list()
backward_questions = backward['question'].to_list()

parameters = ['never', 'almost_never', 'sometimes', 'fairly_often', 'very_often']
display='            1 Never 2 Almost never 3 Sometimes 4 Fairly often 5 Very often'
f_values = [0, 1, 2, 3, 4]
b_values = [4, 3, 2, 1, 0]

no_of_questions = len(forward_questions) + len(backward_questions)
max_stress = no_of_questions * 4
max_range = 40


def start_test():
    f_stress, b_stress = 0, 0
    for question in forward_questions:
        print("Assistant : " + question)
        voice_output(question)
        print(display)
        voice_output(display)
        value = user_input(4)
        f_stress += f_values[value]

    for question in backward_questions:
        print("Assistant : " + question)
        voice_output(question)
        print(display)
        voice_output(display)
        value = user_input(4)
        b_stress += b_values[value]

    return f_stress, b_stress


def stress_calc():
    f_stress, b_stress = start_test()
    pss_value = 40 * (f_stress + b_stress) / max_stress
    print('Stress PSS Value = {}'.format(pss_value))
    if pss_value <= 13:
        print('Low stress')
        voice_output('Low stress')

    elif (pss_value > 13) & (pss_value <= 26):
        print('Moderate stress')
        voice_output('Moderate stress')

    else:
        print('High Stress')
        voice_output('High Stress')

    return pss_value


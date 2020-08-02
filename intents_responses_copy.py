import re

def match_intent(msg, patterns):
    msg = msg.lower()
    matched_intent = None
    for intent, pattern in patterns.items():
        if re.search(pattern, msg):
            matched_intent = intent

    return matched_intent

intents = {
    'greet': ['hi','hello','hey','bot'],
    'fine': ['how are you (.*)','how do you do (.*)','how are you','how do you do'],
    'blood_pressure': ['blood pressure','pressure ','bp'],
    'pulse': ['pulse'],
    'stop': ['quit', 'exit', ' stop', 'close', 'thank you (.*)', 'thank', 'bye', 'goodbye'],
    'news': ['news', 'headline', 'tell (.*) news', 'tell (.*) headline', '(.*) news', '(.*) headline'],
    'read': ['read mail', 'read message', 'read mail (.*)', 'read message (.*)',' (.*) read inbox (.*)'
            '(.*) read mail', 'read (.*) mail (.*)', '(.*) read message',
            'read (.*) mail', 'read (.*) message', '(.*) read (.*) mail', '(.*) read (.*) message'],
    'send': ['send mail', 'send message', 'send mail (.*)', 'send message (.*)',
            '(.*) send mail', 'send (.*) mail (.*)', '(.*) send message',
            'send (.*) mail', 'send (.*) message', '(.*) send (.*) mail', '(.*) send (.*) message'],
    'emergency': ['emergency', '(.*) emergency', 'emergency (.*)', '(.*) emergency (.*)'],
    'self_intro':['(.*) about you','who are you?','what can you do','what can you do (.*)'],
    'stress_test':['(.*) stress test','stress test','stress test (.*)'],
    'room_number':['rooom number','(.*)room number'],
    'time': ['time','(.*)'],
    'date': ['date']
}


responses = {
    'default': ['Sorry, it is beyond my ability.'],
    'greet': ['Hi! ,what can I do for you?', 'Good to see you, how can I help you?'],
    'fine': ['I am fine. Thank you so much for asking!'],
    'blood_pressure': ['Inorder to check your blood pressure, please keep your right hand on this plate infront of you.'],
    'pulse': ['For checking your pulse, please keep your left hand inside this device below.'],
    'stop': ['Bye. Take care. Get well soon.'],
    'read': ['Reading in progress. Please wait...'],
    'send': ['Sending in progress. Please wait...'],
    'news': ["Todays news"],
    'time': ['The time is'],
    'date': ['The date is'],
    'emergency': ['Emergency.'],
    'self_intro':['Self introduction.'],
    'stress_test':['stress test'],
    'room_number':['your room number is:']
}


patterns = {}
for intent, values in intents.items():
    patterns[intent] = re.compile(r'|'.join(values))
while True:
    msg=input()
    print(match_intent(msg, patterns))
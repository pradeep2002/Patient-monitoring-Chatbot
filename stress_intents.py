import re


stress_intents = {
    'never': ['never', '(.*) never', 'never (.*)', '(.*) never (.*)'],
    'almost_never': ['almost never', '(.*) almost never', 'almost never (.*)', '(.*) almost never (.*)'],
    'sometimes': ['sometimes', '(.*) sometimes', 'sometimes (.*)', '(.*) sometimes (.*)','sometime','(.*) sometime','(.*) sometime (.*)'],
    'fairly_often': ['fairly often', '(.*) fairly often', 'fairly often (.*)', '(.*) fairly often (.*)'],
    'very_often': ['very often', '(.*) very often', 'very often (.*)', '(.*) very often (.*)'],
}

stress_patterns = {}
for intent, values in stress_intents.items():
    stress_patterns[intent] = re.compile(r'|'.join(values))


def match_stress(msg, patterns):
    msg = msg.lower()
    print(msg)
    matched_intent = None
    for intent, pattern in patterns.items():
        if re.search(pattern, msg):
            matched_intent = intent

    return matched_intent



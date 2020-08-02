import re

room_intents = {
    '1' : ['1', '(.*) 1 (.*)', '(.*) one', '(.*) one (.*)','(.*)first room', 'first room (.*)'],
    '2' : ['2', '(.*) 2 (.*)', '(.*) two', '(.*) two (.*)',' (.*) second room',' second room (.*)'],
    '3' : ['3', '(.*) 3 (.*)', '(.*) three', '(.*) three (.*)','(.*) third room',' third room (.*)'],
    '4' : ['4', '(.*) 4 (.*)', '(.*) four', '(.*) four(.*)', 'last one',' (.*) fourth room',' fourth room (.*)']
}

room_pattern = {}
for intent, values in room_intents.items():
    room_pattern[intent] = re.compile(r'|'.join(values))


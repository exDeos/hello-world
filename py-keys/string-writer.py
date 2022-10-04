import keyboard
last_key_press = None
built_str = ''

def Main():
    while True:
        pass
    return

def WhatDat(Q):
    global last_key_press
    if last_key_press != Q and Q.event_type == 'down':
        print(Q.name+' '+Q.event_type)
    last_key_press = Q

def StrBuild(Q):
    global built_str
    global last_key_press
    if last_key_press != Q and Q.event_type == 'down':
        if Q.name == 'space':
            next_char= ' '
        elif ('enter' in Q.name) or ('shift' in Q.name) or ('alt' in Q.name) or ('ctrl' in Q.name):
            next_char= ''
        else:
            next_char= Q.name
        built_str = built_str + next_char
        if Q.name == 'enter':
            print(built_str)
            built_str = ''
    last_key_press = Q

X = keyboard.hook(StrBuild)
Main()

# -*- coding: utf-8 -*-
import praw

UA = 'my user-agent string. Contact me at /r/yourAccount or your@email.com'
r = praw.Reddit(UA)
r.login()

def codes_left():
    #Checks if there are any codes left. Returns True or False.
    with open('codes.txt','r') as f:
        raw = f.read()
    codes = raw.split(',')

    if codes != ['']:
        return True
    else:
        return False

def get_code():
    # Gets all codes from the file, picks one, writes the rest back
    # to the original file and returns the single code.
    with open('codes.txt','r') as f:
        raw = f.read()
    codes = raw.split(',')

    code = codes.pop()

    with open('codes.txt','w') as f:
        f.write(','.join(codes))

    return code

        

def user_is_eligible(u):
    # Checks if the user has already gotten a code.
    # If user has got a code already, return False.
    # If user has not got a code, adds the username to the file
    # and then returns True.
    with open('users.txt','r') as f:
        raw = f.read()
    users = raw.split(',')

    if u in users:
        return False

    else:
        users.append(u)
        with open('users.txt','w') as f:
            f.write(','.join(users))
        return True
    
def check_condition(c):
    # See PRAW documentation
    text = c.body
    tokens = text.split()

    # This string is what the bot searches for. If it finds the
    # string in a comment, it will reply with a code.
    if 'SELECTED PHRASE FOR BOT TO DETECT' in tokens:
        return True

def bot_action(c, verbose=True, respond=False):
    # This function is called when the selected phrase is found in a comment.
    
    # Checks if there are codes left
    if codes_left():
        # Checks if the user is eligible for a code
        if user_is_eligible(str(c.author)):
            if respond:
                # Will send a reply with a code to the comment
                c.reply(get_code())
            elif verbose:
                # Just for testing purposes
                print get_code()
                
    # If no more codes, writes out a reply stating so and then quits.
    else:
        print 'Out of codes at the moment. You will be getting one as soon as they are refilled. Dont worry!'
        quit()
    
# Loops through the most recent 500 comments at r/Sweden
for c in praw.helpers.comment_stream(r,'Sweden',500):
    if check_condition(c):
       bot_action(c)

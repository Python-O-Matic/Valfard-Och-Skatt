# -*- coding: utf-8 -*-
import praw,datetime

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

    if str(u) in users:
        print 'Account {} already in Users.txt file.'.format(str(u))
        return False

    user_created_date = datetime.date.fromtimestamp(u.created_utc)
    today = datetime.date.today()
    # Checks if account if over 30 days old to prevent scammers
    
    if (today - user_created_date).days < 30:
        print 'Account {} not older than 30 days.'.format(str(u))
        return False

    else:
        users.append(str(u))
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
        print '\nFound comment'
        return True

def bot_action(c, verbose=True, respond=False):
    # This function is called when the selected phrase is found in a comment.
    
    # Checks if there are codes left
    if codes_left():
        print 'Are codes left'
        # Checks if the user is eligible for a code
        if user_is_eligible(c.author):
            print 'Author {} is eligible'.format(str(c.author))
            if respond:
                code = get_code()
                print 'Selected code: {}'.format(code)
                # Will send a PM with a code to the comment
                try:
                    print 'Trying to send PM'
                    c.author.send_message(subject='Chromecast Code',message=code)
                    c.reply('Sent PM!')
                    print 'Sent PM and Reply successfully \n\n'
                    
                except Exception, e:
                    print 'Exception Raised: \n\n{}'.format(str(e))
                    
                    # Put code back into file. No wasteage here.
                    with open('codes.txt','a') as f:
                        f.write(','+code)

                    # Also remove user from the users.txt file.
                    with open('users.txt','r') as f:
                        raw = f.read()
                    users = raw.split(',')
                    users.remove(str(c.author))

                    with open('users.txt','w') as f:
                        f.write(','.join(users))

        else:
            print 'Author is not eligible'
                
    # If no more codes, writes out a reply stating so and then quits.
    else:
        print 'Out of codes. Quitting'
        quit()

# Loops through the most recent 500 comments at r/Sweden
for c in praw.helpers.comment_stream(r,'Sweden',100):
    if check_condition(c):
       bot_action(c,respond=True)

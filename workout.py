#standard modules
import argparse
import sys
import time
import random

#external libs (already ensured these were installed in setup)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

# 'environment' variables
from envl import REST, ALL_EPS, VID_LINKS, DAY
from envb import *

#manipulate specifically DAY var
def writeDay(val):
    with open(f'envl.py', 'r') as f:
        lines = f.readlines()
        lines.pop()
        lines.append(f'DAY = {val}\n')

    with open(f'envl.py', 'w+') as f:
            f.writelines(lines)

#manipulate specifically REST arr var
def writeRest(arr):
    with open(f'envl.py', 'r') as f:
        lines = f.readlines()
        day = lines.pop()
        lines.pop()
        lines.append(f'REST = {arr}\n')
        lines.append(day)

    with open(f'envl.py', 'w+') as f:
            f.writelines(lines)

#associate arrays of episode names with days (these will be processed into an array of links in vidSetup)
def synthEps():
    i = 1
    arr = []
    d = {}

    for x in ALL_EPS:
        day = f'Day {i}'
        if day in REST:
            d[day] = ['ACTIVE REST DAY']
            i += 1
            continue
        if 'Warm' in x:
            if WARM_UP_BOOL:
                arr.append(x)
            continue
        if 'Cool' in x:
            if COOLDOWN_BOOL:
                arr.append(x)
            d[day] = arr
            arr = []
            i += 1
            continue
        arr.append(x)
    return d

#shuffle a list of links randomly (while maintaining warm up as first and cooldown as last if applicable)
def shuffle(links):
    if WARM_UP_BOOL:
        w = links.pop(0)
    if COOLDOWN_BOOL:
        c = links.pop(-1)
    random.shuffle(links)
    if WARM_UP_BOOL:
        links.insert(0, w)
    if COOLDOWN_BOOL:
        links.append(c)
    return links

#allow for modification (append/remove) of rest days (function can be accessed though a flag)
def modRest():
    print('Current rest days are: ')
    for x in REST:
        print('\t'+x)

    inp = input('Would you like to append a rest day? ')
    if 'y' in inp.lower():
        while True:
            inp = input('Enter a day number to append that day to your rest days: ')
            if inp == 'quit':
                sys.exit()
            try:
                inp = int(inp)
            except:
                print('Try again (enter a number plz)')
                continue
            if inp <= 0 or inp > CHALL_LEN:
                print('Try again (enter a VALID number plz)')
            else:
                break
        REST.append(f'Day {inp}')

    inp = input('Would you like to remove a rest day? ')
    if 'y' in inp.lower():
        while True:
            inp = input('Enter a day number to remove that day from your rest days: ')
            if inp == 'quit':
                sys.exit()
            try:
                inp = int(inp)
            except:
                print('Try again (enter a number plz)')
                continue
            days = [int(x[-1]) for x in REST]
            if inp not in days:
                print('Try again (enter a VALID number plz)')
            else:
                break
        REST.remove(f'Day {inp}')

    writeRest(REST)

    print('Rest days modified. Enjoy!')

#allow for modification of current DAY (function can be accessed directly though a flag)
def modDay(dayn):
    try:
        dayn = int(dayn)
    except:
        print('Enter an integer')
        sys.exit(-1)
    if dayn > CHALL_LEN or dayn <= 0:
        print(f'Enter an integer between 1 and the challenge length ({CHALL_LEN})')
        sys.exit(-1)
    writeDay(dayn)
    sys.exit()
    

#open tab with music, either args.music or default envar MUSIC (if music isnt customized this will never be invoked)
def initMusic(music=MUSIC):
    driver.get(music)
    #give the user some time to skip ads and such
    time.sleep(18)

    #if playlist, attempt to shuffle vid order bc why not
    if args.shuffle:
        try:
            driver.find_element_by_css_selector('ytd-toggle-button-renderer.style-grey-text:nth-child(2) > a:nth-child(1) > yt-icon-button:nth-child(1) > button:nth-child(1) > yt-icon:nth-child(1)').click()
        except:
            pass
    return

#open videos, get input after each vid to pause execution until user finishes
def vidSetup():
    links = []
    ep = synthEps()
    print('Videos for the day: ')

    #videos for the DAY are associated with their links to form an array of links and also printed for convenience of the user and bc why not
    for x in ep[f'Day {DAY}']:
        print('\t'+x)
        links.append(VID_LINKS[x])
    
    #log is setup
    log = f'Day {DAY}:\n'

    #perhaps shuffle links
    if args.shuffle:
        links = shuffle(links)

    #iterate through videos by index
    for x in range(len(links)):
        vid_name = ep[f'Day {DAY}'][x]

        #check condition so as not to open an empty tab
        if not MUSIC and x == 0:
            pass
        else:
            driver.execute_script("window.open('about:blank', 'tab2');")
            driver.switch_to.window('tab2')

        driver.get(links[x])

        #mute the video if user specifies their own music (#movie_player is clicked for focus but not really, its just something the library renders necessary lol)
        if MUSIC and x == 0:
            driver.find_element_by_css_selector('#movie_player').send_keys('m')
        
        #skip most of the talking part automatically UNLESS it's a warm-up or cooldown vid since those start much earlier and are shorter anyway
        if 'Warm Up' not in vid_name and 'Cooldown' not in vid_name:
            for i in range(4):
                driver.find_element_by_css_selector('#movie_player').send_keys('l')
        
        #fullscreen unless told otherwise
        if not args.fullscreen:
            driver.find_element_by_css_selector('#movie_player').send_keys('f')

        #allow for logging of progress on each vid to external log.txt file
        if LOG or args.log:
            inp = input(f'\nDid you complete the video ({vid_name})? ')
            if inp == 'quit':
                sys.exit()
            if 'y' in inp:
                print('Wow good job! Keep it up!')
                log += f'\tALL of \'{vid_name}\' complete! Impressive! :)\n'
            else:
                while True:
                    inp = input(f'How much of of the video did you complete (as a percentage)? ')
                    if inp == 'quit':
                        sys.exit()
                    if inp == '100':
                        print('Wow good job! Keep it up!')
                        log += f'\tALL of \'{vid_name}\' complete! Impressive! :)\n'
                        break
                    try:
                        inp = int(inp)
                    except:
                        print('Try again (enter a number plz)')
                        continue
                    print('Regardless of how much you did today, keep going! You can do it!')
                    log += f'\t{inp}% of \'{vid_name}\' complete.\n'
                    inp = input('\nWould you like to add a note to the log with a reason for why you didn\'t complete the video? ')
                    if 'y' in inp.lower():
                        note = input('Note here: ')
                        log += f'\t\tNote: {note}\n'
                    break
        else:
            #getting 'input' is necessary even if you dont want to log, so here's motivation i guess
            if x+1 == 1:
                z = input(f'\nPress enter to continue :) and feel accomplished that you got the first video down!)')
            else:
                z = input(f'\nPress enter to continue :) and feel accomplished, {x+1} videos down already!)')

    #allow for user to note down things (in the log)
    if NOTES or args.notes:
        print('\nNotes or comments for the day - can be multiline (q to stop writing): ')
        notes = ''
        while True:
            line = input()
            if line == 'q':
                break
            notes += '\t\t'+line+'\n'

        log += f'\tNotes: \n{notes}'

    with open('log.txt', 'a') as f:
        if log != f'Day {DAY}:\n':
            f.write(log)
    return

#make sure all data is here and has been setup
if not SETUP:
    print('Run setup.py first to initialize plz')
    sys.exit(-1)
        
parser = argparse.ArgumentParser(description='Automate working out')
#parser.add_argument('-w', '--warm', action='store', help='Include Warm-up - specify url') haha neither of these works lmao i'll fix it later maybe
#parser.add_argument('-c', '--cool', action='store', help='Include Cooldown - specify url')
parser.add_argument('-s', '--shuffle', action='store_true', help='Shuffle video order')
parser.add_argument('-l', '--log', action='store_true', help='Add a log entry for the day')
parser.add_argument('-n', '--notes', action='store_true', help='Add notes for the day')
parser.add_argument('-f', '--fullscreen', action='store_true', help='Videos are NOT fullscreen')
parser.add_argument('-r', '--rest', action='store_true', help='Modify rest days')
parser.add_argument('-d', '--daynum', action='store', help='Modify current day num (specify int)')
parser.add_argument('-m', '--music', action='store', help='Choosing your own music - specify url (put the link in quotes if it is a playlist)', type=str)

args = parser.parse_args()

#allow for DAY envvar mods
if args.daynum != None:
    dayn = args.daynum
    modDay(dayn)

#check if today is rest
if f'Day {DAY}' in REST:
    REST.remove(f'Day {DAY}')
    writeRest(REST)
    with open('log.txt', 'a') as f:
        f.write(f'Day {DAY}:\n\tREST DAY!\n')
    writeDay(DAY+1)
    print('Rest day!')
    sys.exit()

#allow for rest day mods
if args.rest:
    modRest()
    sys.exit()

"""
if args.warm != None:
    try:
        if requests.get(args.warm).status_code != 200:
            print('Warm up link invalid, try again')
            sys.exit(-1)
    except:
        print('Warm up link not a url (try prepending \'http(s)://\'?)')
        sys.exit(-1)
    WARM_UP_BOOL = True
    WARM_UP_LINK = args.warm

if args.cool != None:
    try:
        if requests.get(args.cool).status_code != 200:
            print('Cooldown link invalid, try again')
            sys.exit(-1)
    except:
        print('Cooldown link not a url (try prepending \'http(s)://\'?)')
        sys.exit(-1)
    COOLDOWN_BOOL = True
    COOLDOWN_LINK = args.cool
"""

print(f'Congrats, you are on day {DAY} of {CHALL}')

#check if music specified as an arg
if args.music != None:
    print(f"You have specified your own music (playlist {args.music})")
    if requests.get(args.music).status_code != 200:
        print('Try again, your url is invalid')
        sys.exit(-1)

#init drivers (setup.py should have made sure they existed)
if DRIVER == 'Firefox':
    driver = webdriver.Firefox()
elif DRIVER == 'Chrome':
    driver = webdriver.Chrome()
else:
    driver = webdriver.Safari()

#full browser window
driver.maximize_window()

#actually set up music (this is done AFTER the drivers init)
if args.music != None:
    initMusic(args.music)

elif MUSIC != '':
    print(f"You have specified your own (default) music - playlist is {MUSIC})")
    initMusic()

#open videos + begin logging/notes
vidSetup()

#closure
driver.quit()
print(f'Day {DAY} complete!')

#ensure that days are updated with each time the program is run
DAY += 1
writeDay(DAY)

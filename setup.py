#standard library modules
import time #for pretty printing
import sys #for exit calls

#internal modules
import soup_parse #webscraping funcs

#checksum it later? bc why not

#make new files/truncate prev to store env vars
def clearEnvFiles():
    f1 = open("envb.py", "w+").close()
    f2 = open("envl.py", "w+").close()

#append environment variable with a certain value to one of the env files
def writeEnv(env, var, val):
    with open(f'{env}.py', 'a') as f:
        f.write(f'{var} = {val}\n')

#allow user to choose a driver and make sure that it is installed (if not, user is redirected to an instructional document)
def driverSetup():
    d = input('Driver (Chrome, Safari, Firefox): ').lower()
    if d == 'quit':
        sys.exit(-1)
    if 'g' in d or 'c' in d:
        try:
            #make sure that chromedriver can be accessed!
            x = webdriver.ChromeOptions()
            x.add_argument('--headless')
            y = webdriver.Chrome(options=x)
            y.close()
        except:
            print('It seems you don\'t have a driver for Chrome. Install one?')
            time.sleep(0.5)
            print('\tGuide: chromedriver_install.txt')
            time.sleep(0.5)
            print('\tShort Guide: driver_setup_nv.txt')
            sys.exit(-1)
        print('~ Your driver is now set to Chrome ~')
        writeEnv('envb', 'DRIVER', '\'Chrome\'')
    elif 's' in d:
        try:
            x = webdriver.SafariOptions()
            x.add_argument('--headless')
            y = webdriver.Safari(options=x)
            y.close()
        except:
            print('It seems you don\'t have a driver for Safari. Install one?')
            sys.exit(-1)
        print('~ Your driver is now set to Safari ~')
        writeEnv('envb', 'DRIVER', '\'Safari\'')
    else:
        try:
            x = webdriver.FirefoxOptions()
            x.add_argument('--headless')
            y = webdriver.Firefox(options=x)
            y.close()
        except:
            print('It seems you don\'t have a driver for Firefox. Install one?')
            time.sleep(0.5)
            print('\tGuide: geckodriver_install.txt')
            time.sleep(0.5)
            print('\tShort Guide: driver_setup_nv.txt')
            sys.exit(-1)
        print('~ Your driver is now set to Firefox ~')
        writeEnv('envb', 'DRIVER', '\'Firefox\'')

#input structure for warm-up/cooldown vids
def inpWC(string):
    s = string.lower().replace('_', ' ')
    inp = input(f'Would you like to include {s} videos (yours or default)? ').lower()
    if inp == 'quit':
            sys.exit(-1)
    wc_link = ''
    if 'y' in inp:
        writeEnv('envb', f'{string}_BOOL', 'True')
        inp = input(f'Would you like to set a custom default {s} video (not the one provided)? ').lower()
        if inp == 'quit':
            sys.exit(-1)
        if 'y' in inp:
            while True:
                inp = input('Put the youtube link to the video here: ')
                if inp == 'quit':
                    sys.exit(-1)
                if requests.get(inp).status_code != 200:
                    print('Sorry, cannot access that link. Try again?')
                    continue
                print(f'~ Custom {s} link has been set! ~')
                writeEnv('envb', f'{string}_LINK', f'\'{inp}\'')
                wc_link = inp
                break
        else:
            print(f'~ Provided {s} videos will be used ~')

    else:
        print('~ No? Okay! ~')
        writeEnv('envb', f'{string}_BOOL', 'False')
    return wc_link


#basic input structure
def inp(d, string):
    if d == 'quit':
        sys.exit(-1)
    if 'y' in d.lower():
        print(f'~ {string.capitalize()} set to true as default ~')
        writeEnv(f'envb', string, 'True')
    else:
        print(f'~ {string.capitalize()} set to false as default ~')
        writeEnv('envb', string, 'False')

#returns either single chall name as a string or an array of possibilities (possibilitites will be parsed by helper function to narrow them down)
def challInp():
    #this is hardcoded. If you want all new challs, you can either run the below commented script or just directly add html page of a newer chall in here
    page_links = ['2021/hourglass-challenge.html', '2021/flat-stomach-challenge.html', '2020/get-peachy-challenge.html', '2020/two-weeks-shred-challenge.html', '2020/get-fit-challenge.html', '2020/intense-core-challenge.html', '2020/summer-shred-challenge.html', '2020/hourglass-program.html', '2020/slim-thigh-challenge.html', '2020/flat-tummy-challenge.html', '2019/booty-challenge.html', '2019/lean-arms-challenge.html', '2019/two-weeks-shred-challenge.html', '2019/hourglass-program.html', '2019/summer-shred-challenge.html', '2019/lean-thigh-challenge.html', '2019/flat-belly-challenge.html', '2018/eight-week-challenge.html']
    """
        links = []
        for x in soup.findAll('a'):
            links.append(x['href'])

        links = links[6:-3]
        links.remove('2020/movember-holiday-schedule.html')
        print(links)
    """
    #get input
    while True:
        inp = input('Which challenge are you doing: ')
        if inp == 'quit':
            sys.exit(-1)

        link = [x.replace('-', ' ').replace('.html', '') for x in page_links if inp in x.replace('-', ' ')]

        if len(link) == 0:
            #apply stricter processing
            link = [x.replace('-', ' ').replace('.html', '') for x in page_links if inp.lower().replace('week', 'weeks').replace('2 ', 'two ') in x.replace('-', ' ').replace('/', ' ')]
            if len(link) == 0:
                print('Try again...')
                continue

        if len(link) == 1:
            print(f'~ Your challenge has been set to {link[0]} ~')
            chall = link[0].replace(' ', '-') + '.html'
            writeEnv('envb', 'CHALL', '\''+chall+'\'')
            return chall

        else:
            return link


#utility function to challInp to choose a challenge out of a list of possibilities
def chooseChall(link):
    i = 1
    for x in link:
        print(str(i) + ") " + x)
        i += 1
    while True:
        idx = input('Choose a number: ')
        try:
            idx = int(idx) - 1
        except:
            if idx == 'quit':
                sys.exit(-1)
            print('Try again...')
            continue
        
        if idx < len(link) and idx >= 0:
            print(f'\n~ Your challenge has been set to {link[idx]}! ~\n')
            chall = link[idx].replace(' ', '-') + '.html'
            writeEnv('envb', 'CHALL', '\''+chall+'\'')
            break
    return chall

#pretty print dict(ionary) with time delays between each line
def ppd(d):
    for k, v in d.items():
        if len(k) < 6:
            print(f'\t{k}  *** {v}')
            time.sleep(.4)
        else:
            print(f'\t{k} *** {v}')
            time.sleep(.4)

#set all persistent 'setup' variables (will be used and reused in workout.py)
def setEnvVars():
    links = soup_parse.getLinks(soup)
    if warm_up_link != '':
        links['Warm Up'] = warm_up_link
    if cooldown_link != '':
        links['Cooldown'] = cooldown_link

    writeEnv('envl', 'VID_LINKS', str(links))
    writeEnv('envl', 'ALL_EPS', str(soup_parse.getEps(soup)))

    writeEnv('envb', 'CHALL_LEN', chall_len)
    writeEnv('envb', 'SETUP', 'True')

    writeEnv('envl', 'REST', str(soup_parse.getRest(soup)))
    writeEnv('envl', 'DAY', DAY)


#make sure this can actually be run... (try to import 3rd party libs)
try:
    import requests #to get content for soup and for testing urls
except:
    print('pip3 install requests')
    sys.exit(-1)
try:
    from bs4 import BeautifulSoup #html parser
except:
    print('pip3 install bs4')
    sys.exit(-1)
try:
    from selenium import webdriver #test if selenium driver(s) installed
except:
    print('pip3 install selenium')
    sys.exit(-1)

#create/truncate env files (used to store persistent vars)
clearEnvFiles()

#begin data collection
print('Type \'quit\' to quit')

driverSetup()
print()

# setup music (user can use default music or set their own playlist)
m = input("Would you like to choose your own music (a default playlist or video)? ").lower()
if m == 'quit':
    sys.exit(-1)
elif 'y' in m:
    while True:
        m = input("Put a link to your chosen music here (ctrl+shift+v to paste in terminal): ")
        if m == 'quit':
            sys.exit(-1)
        if 'https://www.youtube.com/watch?v=' in m:
            if requests.get(m).status_code != 200:
                print('Sorry, cannot access that link. Try again?')
                continue
            writeEnv('envb', 'MUSIC', f'\'{m}\'')
            break
        else:
            print('Put in music in the format \'https://www.youtube.com/watch?v=\' plz, try again')
    print('~ A custom default playlist/video has been set! ~')
else:
    print('~ No? Okay then. Default royalty-free EDM it is! ~')
    writeEnv('envb', 'MUSIC', '\'''\'')

#newline for aesthetic spacing
print()

#setup whether or not 'recommended' w/c videos will be included
warm_up_link = inpWC('WARM_UP')
print()
cooldown_link = inpWC('COOLDOWN')

print()

#allow the user to track (or not track) their progress
d = input('Would you like to have logging as a default? ')
inp(d, 'LOG')
print()
d = input('Would you like to have daily notes as a default? ')
inp(d, 'NOTES')

print()

#choose challenge (challInp returns either a string (singular challenge name) or a list to choose a challenge from)
chall = challInp()
if isinstance(chall, list):
    chall = chooseChall(chall)

#get content of page for scraping
response = requests.get("https://www.chloeting.com/program/" + chall)
if response.ok:
    #if page exists/is up, setup html parser
    soup = BeautifulSoup(response.text, features="lxml")
else:
    print('Can\' access the page. Try again later since this probably isn\'t my fault :)')
    sys.exit(-1)

#read the comment on the other hardcoded piece of data (page_links)
targets = {'2021/hourglass-challenge.html': 'Booty, Abs, Full Body', '2021/flat-stomach-challenge.html': 'Weight loss, Abs, Full Body', '2020/movember-holiday-schedule.html': 'Full Body, Weight Loss', '2020/get-peachy-challenge.html': 'Booty, Abs, Full Body', '2020/two-weeks-shred-challenge.html': 'Abs, Weight Loss, Full Body', '2020/get-fit-challenge.html': 'Full Body, Resistance', '2020/intense-core-challenge.html': 'Core, Full-Body', '2020/summer-shred-challenge.html': 'Weight loss, Abs, Full Body', '2020/hourglass-program.html': 'Abs, Waist, Butt', '2020/slim-thigh-challenge.html': 'Thighs, Butt, Waist', '2020/flat-tummy-challenge.html': 'Abs, Core, Weight Loss', '2019/booty-challenge.html': 'Booty, Abs, Hourglass', '2019/lean-arms-challenge.html': 'Arms, Abs, Toning', '2019/two-weeks-shred-challenge.html': 'Abs, Weight Loss, Full Body', '2019/hourglass-program.html': 'Abs, Butt, Toning', '2019/summer-shred-challenge.html': 'Abs, Full Body, Weight Loss', '2019/lean-thigh-challenge.html': 'Thigh, lean legs', '2019/flat-belly-challenge.html': 'Abs, Core, Weight Loss', '2018/eight-week-challenge.html': 'Full Body'}
"""
url = "https://www.chloeting.com/program/"
d = {}
for x in page_links:
    response = requests.get(url+x)
    soup = BeautifulSoup(response.text, features='lxml')
    info = soup.findAll('div', attrs={'class':'type-and-equips'})
    for y in info:
        z = str(y.findAll('p')[0]).splitlines()[4].lstrip()
        d[x] = z
print(d)
"""

print('Challenge overview: ')
#this targets part took so much work to get right and its only one pathetic line :(
print(f'\tTargets - {targets[chall]}')

#give the user some information about the challenge to show off webscraping info + to be useful
info = soup_parse.getInfo(soup)
chall_len = len(info)
ppd(info)

#allow for people to start using the tool on a certain day and not just Day 1 as default
d = input('\nAre you just starting this challenge (is this Day 0 or 1 for you)? ')
if d == 'quit':
    sys.exit(-1)
if 'y' in d.lower():
    print('And in the beginning there was ... one determined person who wont give up :P')
    DAY = 1
else:
    while True:
        d = input(f'What day are you starting from? [this challenge has {chall_len} days]: ')
        try:
            d = int(d)
            if d > chall_len or d < 0:
                print('That number of days is incorrect. Try again.')
                continue
            if d >= 6:
                print('Wow you\'ve been doing this for over 6 days and studies have shown you will likely follow through all the way! You can do it!')
            DAY = d
            break
        except:
            print('Enter the day number please, try again')

print('\n~ Setup complete! Enjoy your challenge! You can do this! ~')

setEnvVars()

open('log.txt', 'w+').close()




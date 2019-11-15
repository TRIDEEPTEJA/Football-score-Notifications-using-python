from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.request import urlopen
from sys import exit
from time import sleep
import platform
    
def sendmessage(message):
    if pf == 2:
        Popen(['notify-send', message])
    else:
        toaster = ToastNotifier()
        toaster.show_toast("Match Update!",message)
    print(message)

def Retrieve_Data(url):
    try:
        global source, html, match_container, match_status, home, away, home_score, away_score, time, print_score, print_time
        source = urlopen(url)
        html = source.read()
        source.close()
        soup = BeautifulSoup(html, "html.parser")
        match_container = soup.find("div",{"class":"widget-match-header"})
        match_status = match_container.find("div",{"class":"widget-match-header__info"})
        teams = match_container.findAll("div",{"class":"widget-match-header__name"})
        home = teams[0].text
        away = teams[1].text
        time = match_status.div.span.text
        score = match_status.find("div",{"class":"widget-match-header__score"}).span.text
        home_score = score.split(" ")[0]
        away_score = score.split(" ")[2]
        print_score = "{} {}-{} {}".format(home, home_score, away_score, away)
        print_time = "Time : {}".format(time)
    except ValueError:
        print("**** Invalid url. Try again. Make sure the url has http:// ****")
        exit()
    except URLError:
        print("There is an error. Follow the below steps and run the code again:\n1. Check if the URL is correct\n2. Check your internet connection")
        exit()

global pf
if platform.system() == 'Windows' and platform.release() == '10':
    from win10toast import ToastNotifier
    pf = 1
elif platform.system() == 'Linux':
    from subprocess import Popen
    pf = 2
else:
    pf = 0

if pf == 0:
    print('No support yet for the given OS')
    exit()

url = input('Enter the Goal.com live match url here:  ')
Retrieve_Data(url)
if(time == "v"):
    print("{} vs {}\nMatch didn't start yet".format(home, away))
    exit()
elif(time == "FT"):
    print("FT: {}\nMatch already finished".format(print_score))
    exit()
elif(time != "HT"):
    print("{}\n{}".format(print_score, print_time))

while(True):
    home_score_prev = home_score
    away_score_prev = away_score
    Retrieve_Data(url)
    if (home_score != home_score_prev or away_score != away_score_prev):
        sendmessage("Goal update! {}\n{}".format(print_time, print_score))
    if(time == "HT"):
        sendmessage("Half-Time\n{}".format(print_score))
        sleep(600)
        while(True):
            Retrieve_Data(url)
            if (time != "HT"):
                sendmessage("2nd half-kickoff\n{}".format(print_score))
                break
            else:
                sleep(30)
    if(time == "FT"):
        sendmessage("Full-Time\n{}".format(print_score))
        break
import requests
from mojang import MojangAPI
import time
import datetime
import colorama
from colorama import Back, Fore, Style

# Enable colors in Terminal
colorama.init(autoreset=True)

# Getting the names you put in the names.txt file
my_file = open("names.txt", "r")
content_list = my_file.readlines()
my_file.close()

# Getting the API key you put in the config.txt file
delimeter = "="
def findValue(fullString):
    fullString = fullString.rstrip("\n")
    value = fullString[fullString.index(delimeter)+1:]
    value = value.replace(" ", "")
    return value

config_file = open("config.txt", "r")
for line in config_file:
    if line.startswith("API_KEY"):
        API_KEY = findValue(line)
config_file.close()

# Making a loop to check name by name
loop = True

while loop:
    for line in content_list:
            userinput = line.rstrip("\n")

            # Getting the UUID from the names and making the link to get all the data
            uuid = MojangAPI.get_uuid(userinput)
            requestlink = str("https://api.hypixel.net/player?key="+API_KEY+"&uuid="+uuid)
            hydata = requests.get(requestlink).json()

            # Define the needed data to a variable
            playerName = hydata["player"]["displayname"]
            lastLogin = hydata["player"]["lastLogin"]
            lastLogout = hydata["player"]["lastLogout"]

            # Making the time format readable
            unixTimestamp = lastLogin / 1000.0
            lastLogin = (datetime.datetime.fromtimestamp(unixTimestamp).strftime('%d.%m.%Y - %H:%M'))
            unixTimestamp = lastLogout / 1000.0
            lastLogout = (datetime.datetime.fromtimestamp(unixTimestamp).strftime('%d.%m.%Y - %H:%M'))

            # Creating a much better readable output with this
            spaceNumber = 20 - len(playerName)
            space = "" + " " * spaceNumber

            # Define if the player is online or offline
            if lastLogin > lastLogout:
                onlineStatus = "Online"
            else:
                onlineStatus = "Offline"

            # Printing the final output
            if onlineStatus == "Online":
                print("\n", Fore.GREEN + playerName, space, Fore.GREEN + onlineStatus, "\n")
            else:
                print(Fore.WHITE + playerName, space, Fore.WHITE + lastLogout)
            
            # Making a delay of 0.75 soconds because there is a limit of 120 request per minute for the API
            time.sleep(0.75)

input()
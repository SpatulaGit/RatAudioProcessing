
import json
import sounddevice as sd
import numpy

def ChangeSettings():

    #get all audio devices and output them to user
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device["max_input_channels"] > 0:
            print(i,device["name"])
    print()

    #ask user for what their input is
    userDeviceID = int(input("What device is your input device (use device index)? "))

    #add input information to settings.json
    with open("settings.json","r") as file:
        settings = json.load(file)
    settings["devices"]["inputDeviceID"] = userDeviceID
    with open("settings.json","w") as file:
        json.dump(settings,file,indent=4)






userChoice = int(input("""
What would you like to do?
1) Change Settings
2) Activate Audio Processing
"""))

if userChoice == 1:
    ChangeSettings()

print("Good Bye :)")


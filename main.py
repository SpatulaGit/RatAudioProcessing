
import json
import sounddevice as sd
import numpy as np

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





def ActivateAudioProcessing():
    import numpy as np

    with open("settings.json", "r") as file:
        settings = json.load(file)

    # Your selected physical microphone
    deviceID = settings["devices"]["inputDeviceID"]
    deviceInfo = sd.query_devices(deviceID)
    sampleRate = int(deviceInfo["default_samplerate"])

    # Find VB-CABLE's playback device
    cableID = None

    for i, device in enumerate(sd.query_devices()):
        if (
            "CABLE Input" in device["name"]
            and device["max_output_channels"] > 0
        ):
            cableID = i
            break

    if cableID is None:
        print("VB-CABLE Input not found!")
        return

    cableInfo = sd.query_devices(cableID)
    outputChannels = min(2, cableInfo["max_output_channels"])

    # Circular delay buffer
    delaySeconds = 0.5
    delaySamples = int(sampleRate * delaySeconds)
    delayBuffer = np.zeros(delaySamples, dtype=np.float32)
    writePos = 0

    def callback(indata, outdata, frames, time, status):
        nonlocal writePos

        if status:
            print(status)

        for i in range(frames):
            delayedSample = delayBuffer[writePos]
            delayBuffer[writePos] = indata[i, 0]

            # Send delayed mono audio to every output channel
            for channel in range(outdata.shape[1]):
                outdata[i, channel] = delayedSample

            writePos = (writePos + 1) % delaySamples

    print("Microphone:", deviceInfo["name"])
    print("Output:", cableInfo["name"])
    print("Sending delayed audio to VB-CABLE...")

    with sd.Stream(
        device=(deviceID, cableID),
        samplerate=sampleRate,
        channels=(1, outputChannels),
        dtype="float32",
        callback=callback
    ):
        try:
            while True:
                sd.sleep(1000)
        except KeyboardInterrupt:
            pass



userChoice = int(input("""
What would you like to do?
1) Change Settings
2) Activate Audio Processing
"""))

if userChoice == 1:
    ChangeSettings()
elif userChoice == 2:
    ActivateAudioProcessing()

print("Good Bye :)")


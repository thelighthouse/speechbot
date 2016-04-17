import speech_recognition as sr
import pyaudio
import re
import webbrowser
import phue
import time
import random

TRIGGER_THRESHOLD = 20
PAUSE_THRESHOLD = 0.3 # number of seconds to signal end of phrase
CHUNK = 1024 # The size of each audio chunk coming from the input device.
RATE = 16000 # Speech recognition only works well with this rate.  Don't change unless your microphone demands it.

colors = {"alice blue":[0.3088,0.3212],"antique white":[0.3548,0.3489],"aqua":[0.17,0.3403],"aquamarine":[0.2138,0.4051],"azure":[0.3059,0.3303],"beige":[0.3402,0.356],"bisque":[0.3806,0.3576],"black":[0.139,0.081],"blanched almond":[0.3695,0.3584],"blue":[0.139,0.081],"blue violet":[0.245,0.1214],"brown":[0.6399,0.3041],"burlywood":[0.4236,0.3811],"cadet blue":[0.2211,0.3328],"chartreuse":[0.2682,0.6632],"chocolate":[0.6009,0.3684],"coral":[0.5763,0.3486],"cornflower":[0.1905,0.1945],"cornsilk":[0.3511,0.3574],"crimson":[0.6531,0.2834],"cyan":[0.17,0.3403],"dark blue":[0.139,0.081],"dark cyan":[0.17,0.3403],"dark goldenrod":[0.5265,0.4428],"dark gray":[0.3227,0.329],"dark green":[0.214,0.709],"dark khaki":[0.4004,0.4331],"dark magenta":[0.3787,0.1724],"dark olive green":[0.3475,0.5047],"dark orange":[0.5951,0.3872],"dark orchid":[0.296,0.1409],"dark red":[0.7,0.2986],"dark salmon":[0.4837,0.3479],"dark sea green":[0.2924,0.4134],"dark slate blue":[0.2206,0.1484],"dark slate gray":[0.2239,0.3368],"dark turquoise":[0.1693,0.3347],"dark violet":[0.2742,0.1326],"deep pink":[0.5454,0.2359],"deep sky blue":[0.1576,0.2368],"dim gray":[0.3227,0.329],"dodger blue":[0.1484,0.1599],"firebrick":[0.6621,0.3023],"floral white":[0.3361,0.3388],"forest green":[0.2097,0.6732],"fuchsia":[0.3787,0.1724],"gainsboro":[0.3227,0.329],"ghost white":[0.3174,0.3207],"gold":[0.4947,0.472],"goldenrod":[0.5136,0.4444],"gray":[0.3227,0.329],"web gray":[0.3227,0.329],"green":[0.214,0.709],"web green":[0.214,0.709],"green yellow":[0.3298,0.5959],"honeydew":[0.316,0.3477],"hot pink":[0.4682,0.2452],"indian red":[0.5488,0.3112],"indigo":[0.2332,0.1169],"ivory":[0.3334,0.3455],"khaki":[0.4019,0.4261],"lavender":[0.3085,0.3071],"lavender blush":[0.3369,0.3225],"lawn green":[0.2663,0.6649],"lemon chiffon":[0.3608,0.3756],"light blue":[0.2621,0.3157],"light coral":[0.5075,0.3145],"light cyan":[0.2901,0.3316],"light goldenrod":[0.3504,0.3717],"light gray":[0.3227,0.329],"light green":[0.2648,0.4901],"light pink":[0.4112,0.3091],"light salmon":[0.5016,0.3531],"light sea green":[0.1721,0.358],"light sky blue":[0.214,0.2749],"light slate gray":[0.2738,0.297],"light steel blue":[0.276,0.2975],"light yellow":[0.3436,0.3612],"lime":[0.214,0.709],"lime green":[0.2101,0.6765],"linen":[0.3411,0.3387],"magenta":[0.3787,0.1724],"maroon":[0.5383,0.2566],"web maroon":[0.7,0.2986],"medium aquamarine":[0.215,0.4014],"medium blue":[0.139,0.081],"medium orchid":[0.3365,0.1735],"medium purple":[0.263,0.1773],"medium sea green":[0.1979,0.5005],"medium slate blue":[0.2179,0.1424],"medium spring green":[0.1919,0.524],"medium turquoise":[0.176,0.3496],"medium violet red":[0.504,0.2201],"midnight blue":[0.1585,0.0884],"mint cream":[0.315,0.3363],"misty rose":[0.3581,0.3284],"moccasin":[0.3927,0.3732],"navajo white":[0.4027,0.3757],"navy blue":[0.139,0.081],"old lace":[0.3421,0.344],"olive":[0.4432,0.5154],"olive drab":[0.354,0.5561],"orange":[0.5614,0.4156],"orange red":[0.6726,0.3217],"orchid":[0.3688,0.2095],"pale goldenrod":[0.3751,0.3983],"pale green":[0.2675,0.4826],"pale turquoise":[0.2539,0.3344],"pale violet red":[0.4658,0.2773],"papaya whip":[0.3591,0.3536],"peach puff":[0.3953,0.3564],"peru":[0.5305,0.3911],"pink":[0.3944,0.3093],"plum":[0.3495,0.2545],"powder blue":[0.262,0.3269],"purple":[0.2651,0.1291],"web purple":[0.3787,0.1724],"rebecca purple":[0.2703,0.1398],"red":[0.7,0.2986],"rosy brown":[0.4026,0.3227],"royal blue":[0.1649,0.1338],"saddle brown":[0.5993,0.369],"salmon":[0.5346,0.3247],"sandy brown":[0.5104,0.3826],"sea green":[0.1968,0.5047],"seashell":[0.3397,0.3353],"sienna":[0.5714,0.3559],"silver":[0.3227,0.329],"sky blue":[0.2206,0.2948],"slate blue":[0.2218,0.1444],"slate gray":[0.2762,0.3009],"snow":[0.3292,0.3285],"spring green":[0.1994,0.5864],"steel blue":[0.183,0.2325],"tan":[0.4035,0.3772],"teal":[0.17,0.3403],"thistle":[0.3342,0.2971],"tomato":[0.6112,0.3261],"turquoise":[0.1732,0.3672],"violet":[0.3644,0.2133],"wheat":[0.3852,0.3737],"white":[0.3227,0.329],"white smoke":[0.3227,0.329],"yellow":[0.4432,0.5154],"yellow green":[0.3517,0.5618]}

# Define methods
def find_device(p, tags):
    """
    Find an audio device to read input from
    """
    device_index = None
    for i in range(p.get_device_count()):
        devinfo = p.get_device_info_by_index(i)
        print("Device %d: %s" % (i, devinfo["name"]))

        for keyword in tags:
            if keyword in devinfo["name"].lower():
                print("Found an input: device %d - %s"%(i, devinfo["name"]))
                device_index = i
                return device_index

    if device_index is None:
        print("No preferred sound input found; using default input device.")

    return device_index

def interpret_command(command, bridge):
    print("Command: " + command)
    if re.search('fabulous',command):
        print("it's FABBBBUUULLLOOUSSSSS time")
        fabulous(bridge)
    if re.search('party',command):
        print("it's FABBBBUUULLLOOUSSSSS time")
        fabulous(bridge)
        reset_lights(bridge)
    # if re.search("blue", result.lower()) :
        # print("blue found in result")
        # webbrowser.open('http://192.168.1.5:5000/color?hue=173')
    # if re.search("red", result.lower()) :
        # print("red found in result")
        # webbrowser.open('http://192.168.1.5:5000/color?hue=8')
    # if re.search("green", result.lowerc()) :
        # print("green found in result")
        # webbrowser.open('http://192.168.1.5:5000/color?hue=95')
    # if re.search("melon", result.lower()) :
        # print("melon found in result")
        #webbrowser.open('http://192.168.1.5:5000/color?hue=76')

def fabulous(bridge):
    light_names = bridge.get_light_objects('name')
    party_lights = ['Kitchen light 1','Kitchen light 2','Living room','Back hallway','Hue Downlight 1']
    rainbow = ['violet','indigo','blue','green','yellow','orange','red']
    for l in party_lights:
        light_names[l].transitiontime = 2
    for _ in range(60):
        for l in party_lights:
            i = random.randint(0,6)
            light_names[l].xy = colors[rainbow[i]]
            time.sleep(0.02)

def reset_lights(bridge, color=None):
    light_names = bridge.get_light_objects('name')
    party_lights = ['Kitchen light 1','Kitchen light 2','Living room','Back hallway','Hue Downlight 1']
    if color is None:
        color = "navy blue"
    for l in party_lights:
        light_names[l].xy = colors[color]

if __name__ == '__main__':
    print("SETUP LIGHTS. PRESS CONNECT ON BRIDGE")
    from phue import Bridge
    bridge = Bridge('192.168.1.134')
    bridge.connect()

    print("STARTING LIGTHOUSE LISTENER...")
    r = sr.Recognizer()
    p = pyaudio.PyAudio()
    device_index = find_device(p, ["input", "mic", "audio"])
    m = sr.Microphone(device_index,RATE,CHUNK)
    listen = False
    while True:
        while listen == False:
            try:
                print("start listening for command word...")
                with m as source:
                    r.adjust_for_ambient_noise(source, duration = 1)
                    r.pause_threshold = 1.2
                    if r.energy_threshold > TRIGGER_THRESHOLD:
                        r.energy_threshold = TRIGGER_THRESHOLD
                    
                    print("Threshold set to: " + str(r.energy_threshold))
                    audio = r.listen(source,5)
                    pinger = r.recognize_google(audio)
                    print(pinger)
                try:
                    if re.search("house", pinger.lower()):
                        interpret_command(pinger.lower(),bridge)
                    else:
                        continue
                except LookupError:
                    continue
            except sr.UnknownValueError:
                continue
            except sr.WaitTimeoutError:
                continue

        # while listen == True:
            # try:
                # with m as source:
                    # r.adjust_for_ambient_noise(source)
                    # audio = r.listen(source)
                    # phrase=r.recognize_google(audio)
                # if (phrase.lower() == "stop") :
                    # listen = False
                    # print("Listening stopped. Goodbye")
                    # break
                # else:
                    # interpret_command(phrase)
                    # listen = False
            # except LookupError:
                # print("Could not understand audio")
                # listen = False
            # except sr.UnknownValueError:
                # print("Google Speech Recognition could not understand audio")
                # listen = False
                # continue
            # except sr.RequestError:
                # print("Could not request results from Google Speech Recognition service")
                # continue
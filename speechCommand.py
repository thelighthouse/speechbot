#Python speech recognition testing
#saving audio file done with pyaudio
#speech recognition options are:
#  SpeechRecognition https://pypi.python.org/pypi/SpeechRecognition
#  Dragonfly (using dragon naturally speaking) https://pythonhosted.org/dragonfly
#  Sphinx https://github.com/VikParuchuri/scribe
#then match transcription by regular expression

import pyaudio
import wave
import os
import speech_recognition as sr
import re
import webbrowser

# Paths
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

# Options
CHUNK = 128 # The size of each audio chunk coming from the input device.
FORMAT = pyaudio.paInt16 # Should not be changed, as this format is best for speech recognition.
RATE = 16000 # Speech recognition only works well with this rate.  Don't change unless your microphone demands it.
RECORD_SECONDS = 3 # Number of seconds to record, can be changed.
WAVE_OUTPUT_FILENAME = "output.wav" # Where to save the recording from the microphone.

def find_device(p, tags):
    """
    Find an audio device to read input from.
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
        print("No preferred input found; using default input device.")

    return device_index

def save_audio(wav_file):
    """
    Stream audio from an input device and save it.
    """
    p = pyaudio.PyAudio()

    device = find_device(p, ["input", "mic", "audio"])
    device_info = p.get_device_info_by_index(device)
    channels = int(device_info['maxInputChannels'])

    stream = p.open(
        format=FORMAT,
        channels=channels,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=device
    )

    print("***RECORDING***")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("***FINISHED RECORDING***")

    stream.stop_stream()
    stream.close()

    p.terminate()

    wf = wave.open(wav_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def recognize(wav_file):
    r = sr.Recognizer()
    with sr.WavFile(wav_file) as source:
        audio = r.record(source) # read the entire WAV file
    # """
    # Run speech recognition on a given file.
    # """
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said: " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    # speech_rec = pocketsphinx.Decoder(hmm=HMDIR, lm=LMDIR, dict=DICTD)
    # wav_file = file(wav_file, 'rb')
    # speech_rec.decode_raw(wav_file)
    # result = speech_rec.get_hyp()
    result = r.recognize_google(audio)
    return result

print("Run the thing!")
if __name__ == '__main__':
    save_audio(WAVE_OUTPUT_FILENAME)
    result = recognize(WAVE_OUTPUT_FILENAME)
    print "You just said: {0}".format(result)
    if re.search("blue", result.lower()) :
        print("blue found in result")
        webbrowser.open('http://192.168.1.5:5000/color?hue=173')
    if re.search("red", result.lower()) :
        print("red found in result")
        webbrowser.open('http://192.168.1.5:5000/color?hue=8')
    if re.search("green", result.lower()) :
        print("green found in result")
        webbrowser.open('http://192.168.1.5:5000/color?hue=95')
    if re.search("melon", result.lower()) :
        print("melon found in result")
        webbrowser.open('http://192.168.1.5:5000/color?hue=76')

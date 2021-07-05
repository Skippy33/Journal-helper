import sounddevice as sd
from scipy.io.wavfile import write
import time
import tkinter
fs = 44100  # Sample rate

class gui:
    def __init__(self):
        root = tkinter.Tk


myrecording = sd.rec(frames=(44100 * 5), blocking=True, samplerate=fs, channels=2)
sd.stop()
write('output.wav', fs, myrecording)  # Save as WAV file



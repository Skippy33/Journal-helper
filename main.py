import pyaudio
import wave
import time
import tkinter

#making a class for stuff related to recording
class Recording:
    #initialize
    def __init__(self, recordbutton, window):
        #initialize the recordbutton variable
        self.window = window
        self.recordbutton = recordbutton
        self.audio = pyaudio.PyAudio()
        self.frames = []

    #starts recording
    def startrecording(self):
        print("started recording")
        #starts the recording
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.recordswitch()

    def stoprecording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        sound_file = wave.open("test.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(self.frames))
        sound_file.close()

    #switches the recording
    def recordswitch(self, from_button=False):
        #if the record button has the text "start recording"
        self.window.update()
        if self.recordbutton["text"] == "start recording" and from_button:
            #update the text
            self.recordbutton["text"] = "stop recording"
            self.recordbutton.update()
            self.startrecording()
        elif self.recordbutton["text"] == "stop recording" and from_button:
            #update the text
            self.recordbutton["text"] = "start recording"
            self.recordbutton.update()
            self.stoprecording()

        elif self.recordbutton["text"] == "stop recording" and not from_button:
            self.frames.append(self.stream.read(1024))
            self.recordswitch()





def Main():
    #makes a window
    window = tkinter.Tk()
    window.geometry("200x100")
    #make a record button
    recordbutton = tkinter.Button(window, text="start recording", padx=10, pady=15)
    recordbutton.pack()

    #start a recording class
    record = Recording(recordbutton, window)
    #configure the recordbutton
    recordbutton.configure(command=lambda : record.recordswitch(from_button=True))
    recordbutton.pack()
    #mainloop
    window.mainloop()

if __name__ == '__main__':
    Main()

#sd.stop()
#write('output.wav', fs, myrecording)  # Save as WAV file

#find some better way to record audio
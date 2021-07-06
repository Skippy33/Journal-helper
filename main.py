import pyaudio
import wave
import time
import tkinter

#making a class for stuff related to recording
class Recording:
    #initialize the variables
    def __init__(self, recordbutton, window):
        #self.window takes the place of tk.Tk()
        self.window = window
        #recordbutton is what you press to start/stop recordings
        self.recordbutton = recordbutton
        #audio recording variable
        self.audio = pyaudio.PyAudio()
        #list of frames
        self.frames = []

    #starts recording
    def startrecording(self):
        print("started recording")
        #starts the recording
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        #go back to start
        self.recordswitch()

    #stops recording
    def stoprecording(self):
        #stops the audio stream
        self.stream.stop_stream()
        #closes the audio stream
        self.stream.close()
        #closes the audio window
        self.audio.terminate()
        #open a file to writing
        sound_file = wave.open("test.wav", "wb")
        #set the number of channels
        sound_file.setnchannels(1)
        #the "width" (presumably the type of file)
        sound_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        #sets framerate
        sound_file.setframerate(44100)
        #actually writes the file
        sound_file.writeframes(b"".join(self.frames))
        #closes the file
        sound_file.close()
        #clears frames list for any more recordings
        self.frames = []

    #switches the recording
    def recordswitch(self, from_button=False):
        #update the window
        self.window.update()

        #if the text is "start recording" and the press comes from the button
        if self.recordbutton["text"] == "start recording" and from_button:
            #update the text
            self.recordbutton["text"] = "stop recording"
            self.recordbutton.update()
            #start recording
            self.startrecording()

        #elif the text is "stop[ recording" and the press comes from the button
        elif self.recordbutton["text"] == "stop recording" and from_button:
            #update the text
            self.recordbutton["text"] = "start recording"
            self.recordbutton.update()
            #stop the recording
            self.stoprecording()

        #elif it is currently recording and not gettwing a call from the button
        elif self.recordbutton["text"] == "stop recording" and not from_button:
            #add the newest frames from the stream to the list
            self.frames.append(self.stream.read(1024))
            #go back to the start
            self.recordswitch()





def Main():
    #makes a window
    window = tkinter.Tk()
    #set the window size
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
    #run the program
    Main()

#make a way to transcribe, maybe have a popup to tell person that they are recording, or have pause/continue buttons
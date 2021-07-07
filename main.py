import time

import pyaudio
import wave
import tkinter
import itertools as it

# making a class for stuff related to recording
class Recording:


    # make a class for all the things for recording controls
    class Recordcontrols():
        # initialize
        def __init__(self, window, stream):
            # carry over the audio stream
            self.stream = stream
            # get the GUI window
            self.window = window

            # get the photo for the pause button and downsize
            pausephoto = tkinter.PhotoImage(file=(r"C:\Users\Sebastien\PycharmProjects\Journaling\assets\pause.png"))
            self.window.pausephoto = pausephoto.subsample(3, 3)
            # get the photo for the play button and downsize
            playphoto = tkinter.PhotoImage(file=(r"C:\Users\Sebastien\PycharmProjects\Journaling\assets\play.png"))
            self.window.playphoto = playphoto.subsample(5, 5)

            # make the pause button
            self.pausebutton = tkinter.Button(self.window, image=self.window.pausephoto, text="pause", compound="bottom", command=self.Pause)
            # save a copy of the image so that it displays properly
            self.pausebutton.image = pausephoto

            # get the restart photo and downsize
            stopphoto = tkinter.PhotoImage(file=(r"C:\Users\Sebastien\PycharmProjects\Journaling\assets\stop.png"))
            stopphoto = stopphoto.subsample(3, 3)

            # make the stop button
            self.stopbutton = tkinter.Button(self.window, image=stopphoto, text="restart", compound="bottom")
            # save a copy of the image
            self.stopbutton.image = stopphoto

        # destroys buttons at end of recording
        def EndRecording(self):
            self.pausebutton.destroy()
            self.stopbutton.destroy()

        # things to do when the pause button is pressed
        def Pause(self):
            # if the button says "pause"
            if self.pausebutton["text"] == "pause":
                # get the photo for the play button
                playphoto = self.window.playphoto
                # save a copy to display correctly
                self.window.playphoto = playphoto
                # change the photo
                self.pausebutton.configure(image=playphoto)
                # change the text
                self.pausebutton["text"] = "continue"
                # pause the stream
                self.stream.stop_stream()
                #update the window
                self.window.update()

            elif self.pausebutton["text"] == "continue":
                # get the photo for the play button
                pausephoto = self.window.pausephoto
                # save a copy to display correctly
                self.window.pausephoto = pausephoto
                # change the photo
                self.pausebutton.configure(image=pausephoto)
                # change the text
                self.pausebutton["text"] = "pause"
                # restart the stream
                self.stream.start_stream()
                #update the window
                self.window.update()



    # initialize the variables
    def __init__(self, recordbutton, window):
        # self.window takes the place of tk.Tk()
        self.window = window
        # recordbutton is what you press to start/stop recordings
        self.recordbutton = recordbutton
        # audio recording variable
        self.audio = pyaudio.PyAudio()
        # list of frames
        self.frames = []

    # starts recording
    def startrecording(self):
        # starts the recording
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        # make the record controls
        self.recordcontrols = self.Recordcontrols(self.window, self.stream)
        # display the buttons
        self.recordcontrols.pausebutton.pack(side="left")
        self.recordcontrols.stopbutton.pack(side="right")
        # change the window size
        self.window.geometry("400x200")
        # go back to the start so that the frames can be saved
        self.recordswitch()

    #stops recording
    def stoprecording(self):
        # stops the audio stream
        self.stream.stop_stream()
        # closes the audio stream
        self.stream.close()
        # closes the audio window
        self.audio.terminate()
        # open a file to writing
        sound_file = wave.open("test.wav", "wb")
        # set the number of channels
        sound_file.setnchannels(1)
        # the "width" (presumably the type of file)
        sound_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        # sets framerate
        sound_file.setframerate(44100)
        # actually writes the file
        sound_file.writeframes(b"".join(self.frames))
        # closes the file
        sound_file.close()
        # clears frames list for any more recordings
        self.frames = []

        print("stopped")

    # switches the recording
    def recordswitch(self, from_button=False):

        # update the window
        self.window.update()

        # if the text is "start recording" and the press comes from the button
        if self.recordbutton["text"] == "start recording" and from_button:
            # update the text
            self.recordbutton["text"] = "stop recording"
            self.recordbutton.update()
            # start recording
            self.startrecording()


        # elif the text is "stop[ recording" and the press comes from the button
        elif self.recordbutton["text"] == "stop recording" and from_button:
            print("stopped")
            # update the text
            self.recordbutton["text"] = "start recording"
            self.recordbutton.update()
            # destroy the buttons
            self.recordcontrols.EndRecording()
            # save the files
            self.stoprecording()

        # elif it is currently recording and not gettwing a call from the button
        elif self.recordbutton["text"] == "stop recording" and not from_button and self.stream.is_active():
            # add the newest frames from the stream to the list
            self.frames.append(self.stream.read(1024))
            # go back to the start
            self.recordswitch()

        #if the stream is paused, wait a bit and restart the loop
        time.sleep(.1)
        self.recordswitch()





def Main():
    # makes a window
    window = tkinter.Tk()
    # set the window size
    window.geometry("200x100")
    # make a record button
    recordbutton = tkinter.Button(window, text="start recording", padx=10, pady=15)
    recordbutton.pack(side="top")

    # start a recording class
    record = Recording(recordbutton, window)
    # configure the recordbutton
    recordbutton.configure(command=lambda : record.recordswitch(from_button=True))
    recordbutton.pack(side="top")
    # mainloop
    window.mainloop()

if __name__ == '__main__':
    # run the program
    Main()

# make a way to transcribe, maybe have a popup to tell person that they are recording, or have pause/continue buttons
# needs to end/pause/restart recording
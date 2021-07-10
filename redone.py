import os
import time

import pyaudio
import wave
import tkinter



def initialize():
    global audio
    audio = pyaudio.PyAudio()
    global window
    window = tkinter.Tk()
    # set the window size
    window.geometry("200x100")
    # make a record button
    window.recordbutton = tkinter.Button(window, text="start recording", padx=10, pady=15)
    window.recordbutton.pack(side="top")
    # configure the recordbutton
    window.recordbutton.configure(command=lambda : recordswitch(from_button=True))
    window.recordbutton.pack(side="top")
    # get the photo for the pause button and downsize
    window.pausephoto = tkinter.PhotoImage(file=(r"C:\Users\Sebastien\PycharmProjects\Journaling\assets\pause.png"))
    window.pausephoto = window.pausephoto.subsample(3, 3)
    # get the photo for the play button and downsize
    window.playphoto = tkinter.PhotoImage(file=(r"C:\Users\Sebastien\PycharmProjects\Journaling\assets\play.png"))
    window.playphoto = window.playphoto.subsample(5, 5)

    # make the pause button
    window.pausebutton = tkinter.Button(window, image=window.pausephoto, text="pause", compound="bottom", command=lambda : pause())
    # save a copy of the image so that it displays properly
    window.pausebutton.image = window.pausephoto

    # get the restart photo and downsize
    window.stopphoto = tkinter.PhotoImage(file=(r"C:\Users\Sebastien\PycharmProjects\Journaling\assets\stop.png"))
    window.stopphoto = window.stopphoto.subsample(3, 3)

    # make the stop button
    window.restartbutton = tkinter.Button(window, image=window.stopphoto, text="restart", compound="bottom")
    # save a copy of the image
    window.restartbutton.image = window.stopphoto
    # mainloop
    window.mainloop()

def recordswitch(from_button = False):
    # update the window
    window.update()

    # if the text is "start recording" and the press comes from the button
    if window.recordbutton["text"] == "start recording" and from_button:
        # update the text
        window.recordbutton["text"] = "stop recording"
        window.recordbutton.update()
        # start recording
        global audio
        audio = startrecording()


    # elif the text is "stop[ recording" and the press comes from the button
    elif window.recordbutton["text"] == "stop recording" and from_button:
        print("stopped")
        # update the text
        window.recordbutton["text"] = "start recording"
        window.recordbutton.update()
        # save the files
        stoprecording()

'''def restartrecording():
    stoprecording()
    os.remove("temp.wav")'''

# stops recording
def stoprecording():
    # stops the audio stream
    audio.stream.stop_stream()
    # closes the audio stream
    audio.stream.close()
    # closes the audio window
    audio.terminate()
    # open a file to writing
    sound_file = wave.open("temp.wav", "wb")
    # set the number of channels
    sound_file.setnchannels(1)
    # the "width" (presumably the type of file)
    sound_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    # sets framerate
    sound_file.setframerate(44100)
    # actually writes the file
    sound_file.writeframes(b"".join(audio.frames))
    # closes the file
    sound_file.close()
    # clears frames list for any more recordings
    audio.frames = []
    window.pausebutton.forget()
    window.restartbutton.forget()

def pause():
    global audio
    print(audio.stream.is_stopped())
    if window.pausebutton["text"] == "pause":
        # get the photo for the play button
        window.playphoto = window.playphoto
        # save a copy to display correctly
        window.playphoto = window.playphoto
        # change the photo
        window.pausebutton.configure(image=window.playphoto)
        # change the text
        window.pausebutton["text"] = "continue"
        # pause the stream
        audio.stream.stop_stream()
        # update the window

    elif window.pausebutton["text"] == "continue":
        # get the photo for the play button
        window.pausephoto = window.pausephoto
        # save a copy to display correctly
        window.pausephoto = window.pausephoto
        # change the photo
        window.pausebutton.configure(image=window.pausephoto)
        # change the text
        window.pausebutton["text"] = "pause"
        # restart the stream
        audio.stream.start_stream()
        # update the window

def whilerecording():
    global audio
    while audio.stream.is_active():
        audio.frames.append(audio.stream.read(1024))
        window.update()
    else:
        if audio.stream.is_stopped():
            time.sleep(.2)
            window.update()
            whilerecording()

    # starts recording
def startrecording():
    # starts the recording
    audio.stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    # make the record controls
    audio.frames = []
    # display the buttons
    window.pausebutton.pack(side="left")
    window.restartbutton.pack(side="right")
    # change the window size
    window.geometry("400x200")
    # go back to the start so that the frames can be saved
    whilerecording()

initialize()

#need to get errors when stopping. They dont affect anything, but they are annoying
#need to get pause/play going
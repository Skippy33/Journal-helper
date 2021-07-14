import os
import time
import pyaudio
import wave
import tkinter
import sys


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
    window.restartbutton = tkinter.Button(window, image=window.stopphoto, text="restart", compound="bottom", command=restartrecording)
    # save a copy of the image
    window.restartbutton.image = window.stopphoto

    window.deletebutton = tkinter.Button(window, image=window.stopphoto, text="delete recording", compound="bottom", command=deleterecording)

    window.deletebutton.image = window.stopphoto

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

def restartrecording():
    # stops the audio stream
    audio.stream.stop_stream()
    # closes the audio stream
    audio.stream.close()
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
    os.remove("temp.wav")
    window.recordbutton["text"] = "start recording"
    window.geometry("200x100")


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
    window.recordbutton.forget()
    endscreen()

# what to do when pause button is pressed
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

#what to do while recording
def whilerecording():
    global audio
    # while the stream is active
    while audio.stream.is_active():
        # add the frames to the list
        audio.frames.append(audio.stream.read(1024))
        # update the window
        window.update()
    # when the while loop ends
    else:
        # if the stream is stopped
        if audio.stream.is_stopped():
            # wait a short time
            time.sleep(.5)
            # update the window
            window.update()
            # recursively go to this function
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

# starts the screen after recording
def endscreen():
    global window
    # pack the deletebutton
    window.deletebutton.pack(side="top")

# what to do when delete button is pressed
def deleterecording():
    global window
    # delete the temp file
    os.remove("temp.wav")
    #destroy the window
    window.destroy()
    #restart
    initialize()


initialize()

#need to get errors when stopping. They dont affect anything, but they are annoying
#need to implement a way to add PS
#name file to date (d-m-y) and location (such as d-m-y Location)
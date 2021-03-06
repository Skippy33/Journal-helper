import os
import time
import pyaudio
from wave import open as waveopen
import tkinter
from datetime import datetime

import speech_recognition
from requests import get
import speech_recognition as sr
from sys import exit as sysexit
from textwrap import fill
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
    window.pausephoto = tkinter.PhotoImage(file=(resourcepath(r"assets\pause.png")))
    window.pausephoto = window.pausephoto.subsample(3, 3)
    # get the photo for the play button and downsize
    window.playphoto = tkinter.PhotoImage(file=(resourcepath(r"assets\play.png")))
    window.playphoto = window.playphoto.subsample(5, 5)

    # make the pause button
    window.pausebutton = tkinter.Button(window, image=window.pausephoto, text="pause", compound="bottom", command=lambda : pause())
    # save a copy of the image so that it displays properly
    window.pausebutton.image = window.pausephoto

    # get the restart photo and downsize
    window.stopphoto = tkinter.PhotoImage(file=(resourcepath(r"assets\stop.png")))
    window.stopphoto = window.stopphoto.subsample(3, 3)

    # make the stop button
    window.restartbutton = tkinter.Button(window, image=window.stopphoto, text="restart", compound="bottom", command=restartrecording)
    # save a copy of the image
    window.restartbutton.image = window.stopphoto

    # makes button to delte recording when done
    window.deletebutton = tkinter.Button(window, image=window.stopphoto, text="delete recording", compound="bottom", command=deleterecording)
    # save the image copy
    window.deletebutton.image = window.stopphoto

    window.PSphoto = tkinter.PhotoImage(file=(resourcepath(resourcepath(r"assets\PS.png"))))
    window.PSphoto = window.PSphoto.subsample(2, 2)
    window.PSbutton = tkinter.Button(window, image=window.PSphoto, text="add PS", compound="bottom", command=PS)
    window.PSbutton.image = window.PSphoto

    window.finalizephoto = tkinter.PhotoImage(file=(resourcepath(r"assets\finalize.png")))
    window.finalizephoto = window.finalizephoto.subsample(2, 2)

    window.finalizebutton = tkinter.Button(window, image=window.finalizephoto, text="finalize", compound="bottom", command=finalizerecording)
    window.finalizebutton.image = window.finalizephoto

    window.savenamelabel = tkinter.Label(window, text="Name to save the files by")
    location = get("http://ip-api.com/json/" + get('https://api.ipify.org').text).json()
    now = datetime.now()
    preentry = tkinter.StringVar(window, now.strftime("%D").replace("/", "-") + " " + location["city"] + ", " + location["regionName"])
    window.savenamebox = tkinter.Entry(window, textvariable=preentry)

    window.savephoto = tkinter.PhotoImage(file=(resourcepath(r"assets\save.png")))
    window.savephoto = window.savephoto.subsample(4, 4)

    window.savebutton = tkinter.Button(window, image=window.savephoto, text="save files", compound="bottom", command=saverecording)
    window.savebutton.image = window.finalizephoto

    window.textfilebox = tkinter.Text(window, width=60, height=13)

    window.filelocationlabel = tkinter.Label(window, text="location to save files")
    window.filelocationbox = tkinter.Entry(window)
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)
    config_path = os.path.join(application_path, "save variables.txt")
    window.filelocationbox.insert(-1, open(config_path, "r").read())
    # mainloop
    window.wm_title("journaler")
    window.mainloop()

#converts relative paths from the EXE to absolute paths
def resourcepath(relative_path):
    is_frozen = getattr(sys, 'frozen', False)
    if is_frozen:
        base_path = getattr(sys, '_MEIPASS', '')
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def Popup(message):# makes popup to tell user what is correct formatting
    #make a new window
    popup = tkinter.Tk()
    #gives window title (top bar)
    popup.wm_title("!")
    #make a label
    label = tkinter.Label(popup, text=message, font=("Helvetica", 10))
    #put it on screen
    label.pack(side="top", fill="x", pady=10)
    #make a button that destroys the popup
    B1 = tkinter.Button(popup, text="Okay", command=popup.destroy)
    #put the button on screen
    B1.pack()
    #mainloop it
    popup.mainloop()

def recordswitch(from_button=False):
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
    sound_file = waveopen(resourcepath(r"assets\temp.wav"), "wb")
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
    os.remove(resourcepath(r"assets\temp.wav"))
    window.recordbutton["text"] = "start recording"
    window.geometry("200x100")


# stops recording
def stoprecording():
    # stops the audio stream
    audio.stream.stop_stream()
    window.pausebutton.forget()
    window.restartbutton.forget()
    window.recordbutton.forget()
    endscreen()

# what to do when pause button is pressed
def pause():
    global audio
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
    # pack the postscript button
    window.PSbutton.pack()
    # pack the finalize button
    window.finalizebutton.pack()
    window.geometry("400x600")

# what to do when delete button is pressed
def deleterecording():
    global window
    # delete the temp file
    audio.frames = []
    # destroy the window
    window.destroy()
    # restart
    initialize()

def PS():
    global window
    global audio
    # if the button text is "add PS"
    if window.PSbutton["text"] == "add PS":
        # change the text - this is a standard toggle button
        window.PSbutton["text"] = "stop PS"
        # restart the stream
        audio.stream.start_stream()
        # go back to the "while recording" loop
        whilerecording()

    # else
    elif window.PSbutton["text"] == "stop PS":
        # change the text - standard toggle button stuff
        window.PSbutton["text"] = "add PS"
        # stop the stream
        audio.stream.stop_stream()

def finalizerecording():
    global audio
    global window
    Popup("processing audio for transcription. \n Depending on length of audio, could take \n some time.")
    # set the window size
    window.geometry("600x400")
    # remove the buttons from earlier
    window.finalizebutton.forget()
    window.PSbutton.forget()
    window.deletebutton.forget()
    # closes the audio stream
    audio.stream.close()
    # closes the audio window
    audio.terminate()
    # open a file to writing
    sound_file = waveopen(resourcepath(r"assets\temp.wav"), "wb")
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

    # start a speech recognizer
    r = sr.Recognizer()
    # with the audiofile as the var "source"
    try:
        with sr.AudioFile(resourcepath(r"assets\temp.wav")) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
    except speech_recognition.UnknownValueError:
        text = "something unrecognizable"

    #deletes the temp file
    os.remove(resourcepath(r"assets\temp.wav"))

    # load the text into the box for the user to check
    window.textfilebox.insert(1.0, text)
    # display the GUI elements
    window.textfilebox.pack()
    window.savenamelabel.pack()
    window.savenamebox.pack(ipadx=50)
    window.filelocationlabel.pack()
    window.filelocationbox.pack(ipadx=50)
    window.savebutton.pack()
    # mainloop
    window.mainloop()

# what to do when the button to save is pressed
def saverecording():
    # open the file to save the location the file should have
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)
    config_path = os.path.join(application_path, "save variables.txt")

    open(config_path, "w").write(window.filelocationbox.get())
    #tests if the input directory is valid
    if not os.path.isdir(window.filelocationbox.get()):
        Popup("invalid folder name, \n try the full path")
        return
    # open a file to writing
    sound_file = waveopen(window.filelocationbox.get() + "\\" + window.savenamebox.get() + ".wav", "wb")
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

    # create the text file with the transcription
    open(window.filelocationbox.get() + "\\" + window.savenamebox.get() + ".txt", "w").write(fill(window.textfilebox.get("1.0", "end"), 60))

    # stop the program
    sysexit(1)

# start the whole program
initialize()

#need to add newline characters to the transcription
#remember to disable antivirus when converting to EXE
#use pyinstaller journaler.spec to make EXE, you can also use other options
#good references for pyinstaller:
#https://hackernoon.com/the-one-stop-guide-to-easy-cross-platform-python-freezing-part-1-c53e66556a0a
#https://pyinstaller.readthedocs.io/en/stable/spec-files.html

#commands to use
#pyi-makespec main.py -n journaler --noconsole --onefile --icon=icon.ico  makes the spec, remove --noconsole to get output

#put this in spec file, set data to this
#def get_resources():
#    data_files = []
#    for file_name in os.listdir('assets'):
#        data_files.append((os.path.join('assets', file_name), 'assets'))
#    return data_files

#to compile type:
#pyinstaller journaler.spec
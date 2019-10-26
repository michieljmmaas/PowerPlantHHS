from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter.ttk import Progressbar
from train import train
from multiprocessing import Process, Value, Manager
import multiprocessing as mp
from ctypes import c_char_p
import GUI.GUIFunctions as fn
import GUI.GUIFileReader as fr
from tkinter import font as fontMaker


def makeButton(GUI, fileString, frameHolder, FramePlacer, text, function, arg):
    ButtonIcon = makeIcon(fileString, frameHolder)

    LabelWidth = 150
    LabelHeight = 50

    compoundImage = LEFT
    ButtonAnchor = W
    ButtonRelief = GROOVE
    ButtonCursor = "hand1"
    helv36 = fontMaker.Font(family='Helvetica', size=15, weight='bold')

    if not arg:
        RunButton = Button(FramePlacer, width=LabelWidth, height=LabelHeight, command=function,
                           relief=ButtonRelief, image=ButtonIcon, text=text, compound=compoundImage,
                           anchor=ButtonAnchor, font=helv36, cursor=ButtonCursor)
        return RunButton
    else:
        RunButton = Button(FramePlacer, width=LabelWidth, height=LabelHeight, command=lambda: function(GUI),
                           relief=ButtonRelief, image=ButtonIcon, text=text, compound=compoundImage,
                           anchor=ButtonAnchor, font=helv36, cursor=ButtonCursor)
        return RunButton
    return


def makeIcon(fileString, frameHolder):
    ButtonIcon = PhotoImage(file=fileString)
    IconLabel = Label(frameHolder, image=ButtonIcon)
    IconLabel.image = ButtonIcon
    return ButtonIcon

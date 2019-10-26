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

textPrespace = "  "

def makeButton(GUI, fileString, frameHolder, FramePlacer, text, function, arg):
    ButtonIcon = makeIcon(fileString, frameHolder)

    LabelWidth = 150
    LabelHeight = 50

    compoundImage = LEFT
    ButtonAnchor = W
    ButtonRelief = RAISED
    ButtonCursor = "hand1"

    if not arg:
        RunButton = Button(FramePlacer, width=LabelWidth, height=LabelHeight, command=function,
                           relief=ButtonRelief, image=ButtonIcon, text=text, compound=compoundImage,
                           anchor=ButtonAnchor, font=GUI.ButtonFont, cursor=ButtonCursor)
        return RunButton
    else:
        RunButton = Button(FramePlacer, width=LabelWidth, height=LabelHeight, command=lambda: function(GUI),
                           relief=ButtonRelief, image=ButtonIcon, text=text, compound=compoundImage,
                           anchor=ButtonAnchor, font=GUI.ButtonFont, cursor=ButtonCursor)
        return RunButton
    return


def makeIcon(fileString, frameHolder):
    ButtonIcon = PhotoImage(file=fileString)
    IconLabel = Label(frameHolder, image=ButtonIcon)
    IconLabel.image = ButtonIcon
    return ButtonIcon


def HeaderRow(text1, text2, text3, text4, frameHolder, HFont):
    LabelWidth = 20
    LabelHeight = 3
    text1 = textPrespace + text1
    text2 = textPrespace + text2
    text3 = textPrespace + text3
    text4 = textPrespace + text4
    Label1 = Label(frameHolder, text=text1, width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID, font=HFont)
    Label2 = Label(frameHolder, text=text2, width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID, font=HFont)
    Label3 = Label(frameHolder, text=text3, width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID, font=HFont)
    Label4 = Label(frameHolder, text=text4, width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID, font=HFont)
    Tuple = (Label1, Label2, Label3, Label4)
    return Tuple


def LabelRow(text, frameHolder, HFont, ColFont):
    LabelWidth = 20
    LabelHeight = 3
    text = textPrespace + text
    Label1 = Label(frameHolder, text=text, width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID, font=HFont)
    Label2 = Label(frameHolder, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN)
    Label3 = Label(frameHolder, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN)
    Label4 = Label(frameHolder, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN)
    Tuple = (Label1, Label2, Label3, Label4)
    return Tuple

def InfoItem(text, frameHolder, InfoFont, HFont):
    LabelWidth = 25
    LabelHeight = 3
    InfoGenerationLabel = Button(frameHolder, text=text, width=LabelWidth, height=LabelHeight, relief=SOLID, font=HFont)
    InfoGenerationEntry = Entry(frameHolder, font=InfoFont)
    InfoTuple = (InfoGenerationLabel, InfoGenerationEntry)
    return InfoGenerationEntry, InfoTuple

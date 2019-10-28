from tkinter import *

textPrespace = "  "
InfoLabelWidth = 20
InfoLabelHeight = 3


def makeButton(GUI, fileString, frameHolder, FramePlacer, text, function, arg):
    ButtonIcon = makeIcon(fileString, frameHolder)

    LabelWidth = 150
    LabelHeight = 50

    compoundImage = LEFT
    ButtonAnchor = W
    ButtonRelief = RAISED
    borderwidth = 5
    ButtonCursor = "hand1"

    if not arg:
        NewButton = Button(FramePlacer, width=LabelWidth, height=LabelHeight, command=function,
                           relief=ButtonRelief, image=ButtonIcon, text=text, compound=compoundImage,
                           anchor=ButtonAnchor, font=GUI.ButtonFont, cursor=ButtonCursor, borderwidth=borderwidth)
        return NewButton
    else:
        NewButton = Button(FramePlacer, width=LabelWidth, height=LabelHeight, command=lambda: function(GUI),
                           relief=ButtonRelief, image=ButtonIcon, text=text, compound=compoundImage,
                           anchor=ButtonAnchor, font=GUI.ButtonFont, cursor=ButtonCursor, borderwidth=borderwidth)
        return NewButton
    return


def GrafiekButton(GUI, fileString, frameHolder, FramePlacer, function, arg):
    ButtonIcon = makeIcon(fileString, frameHolder)

    LabelWidth = 65
    LabelHeight = 65

    ButtonAnchor = CENTER
    ButtonRelief = RAISED
    borderwidth = 5
    ButtonCursor = "hand1"

    if not arg:
        RunButton = Button(FramePlacer, width=LabelWidth, height=LabelHeight, command=lambda: function(GUI, False), relief=ButtonRelief,
                           image=ButtonIcon, anchor=ButtonAnchor, font=GUI.ButtonFont, cursor=ButtonCursor,
                           borderwidth=borderwidth)
        return RunButton
    else:
        RunButton = Button(FramePlacer, width=LabelWidth, height=LabelHeight, command=lambda: function(GUI),
                           relief=ButtonRelief, image=ButtonIcon, anchor=ButtonAnchor, font=GUI.ButtonFont,
                           cursor=ButtonCursor, borderwidth=borderwidth)
        return RunButton
    return


def makeIcon(fileString, frameHolder):
    ButtonIcon = PhotoImage(file=fileString)
    IconLabel = Label(frameHolder, image=ButtonIcon)
    IconLabel.image = ButtonIcon
    return ButtonIcon


def HeaderRow(text1, text2, text3, text4, frameHolder, HFont):
    text1 = textPrespace + text1
    text2 = textPrespace + text2
    text3 = textPrespace + text3
    text4 = textPrespace + text4
    Label1 = Label(frameHolder, text=text1, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SOLID,
                   font=HFont)
    Label2 = Label(frameHolder, text=text2, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SOLID,
                   font=HFont)
    Label3 = Label(frameHolder, text=text3, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SOLID,
                   font=HFont)
    Label4 = Label(frameHolder, text=text4, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SOLID,
                   font=HFont)
    Tuple = (Label1, Label2, Label3, Label4)
    return Tuple


def LabelRow(text, frameHolder, HFont, ColFont):
    text = textPrespace + text
    Label1 = Label(frameHolder, text=text, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SOLID,
                   font=HFont)
    Label2 = Label(frameHolder, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SUNKEN, font=ColFont)
    Label3 = Label(frameHolder, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SUNKEN, font=ColFont)
    Label4 = Label(frameHolder, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SUNKEN, font=ColFont)
    Tuple = (Label1, Label2, Label3, Label4)
    return Tuple


def InfoItem(text, frameHolder, InfoFont, HFont):
    LabelWidth = 25
    LabelHeight = 3
    InfoLabel = Button(frameHolder, text=text, width=LabelWidth, height=LabelHeight, relief=SOLID, font=HFont)
    InfoEntry = Entry(frameHolder, font=InfoFont)
    InfoTuple = (InfoLabel, InfoEntry)
    return InfoEntry, InfoTuple

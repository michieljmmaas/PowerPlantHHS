from tkinter import *

textPrespace = "  "  # Zo kan ik alles een beetje opschuiven voor leesbaarheid
InfoLabelWidth = 20  # Algemene breedte
InfoLabelHeight = 3  # Algemene hoogte

# Deze maakt een een van de grote knoppen voor boven het info veld
def makeButton(GUI, fileString, frameHolder, FramePlacer, text, function, arg):
    ButtonIcon = makeIcon(fileString, frameHolder) # Om een afbeelding te laten zien, moet er eerst een Icon van zijn

    LabelWidth = 150 # Deze hebben een andere breedte en hoogte
    LabelHeight = 50

    #Standaard waarden voor de opmaak van de itemss
    compoundImage = LEFT
    ButtonAnchor = W
    ButtonRelief = RAISED
    borderwidth = 5
    ButtonCursor = "hand1" # Vingertje die aangeeft dat je kan klikken

    # Er zijn twee opties voor de functies. Eentje die als paramter GUI heeft, en eentje niet. Je kan het niet direct mee geven als parameter
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

# Deze maakt een knop voor het grafiek veld
def GrafiekButton(GUI, fileString, frameHolder, FramePlacer, function, arg):
    ButtonIcon = makeIcon(fileString, frameHolder)  # Voordat je een plaatje kan toeveogen moet er eerst een Icon van zijn

    LabelWidth = 65
    LabelHeight = 65

    # Gestandardiseerde waarden
    ButtonAnchor = CENTER
    ButtonRelief = RAISED
    borderwidth = 5
    ButtonCursor = "hand1"

    # Verschil in de functie parameters
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

# Deze maakt een Icon die gebruikt voor om de afbeelding te laten zien
def makeIcon(fileString, frameHolder):
    ButtonIcon = PhotoImage(file=fileString)
    IconLabel = Label(frameHolder, image=ButtonIcon)
    IconLabel.image = ButtonIcon
    return ButtonIcon

# Deze maakt een rij met labels voor de Header van het info veld
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

# Deze maakt 4 Labels die gebruikt voor voor het overzicht van de waarden
def LabelRow(text, frameHolder, HFont, ColFont):
    text = textPrespace + text
    Label1 = Label(frameHolder, text=text, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SOLID,
                   font=HFont)
    Label2 = Label(frameHolder, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SUNKEN, font=ColFont)
    Label3 = Label(frameHolder, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SUNKEN, font=ColFont)
    Label4 = Label(frameHolder, width=InfoLabelWidth, height=InfoLabelHeight, anchor=W, relief=SUNKEN, font=ColFont)
    Tuple = (Label1, Label2, Label3, Label4)
    return Tuple

# Deze methode maakt een Laben en Entry koppel voor informatie invoer
def InfoItem(text, frameHolder, InfoFont, HFont):
    LabelWidth = 25
    LabelHeight = 3
    InfoLabel = Button(frameHolder, text=text, width=LabelWidth, height=LabelHeight, relief=SOLID, font=HFont)
    InfoEntry = Entry(frameHolder, font=InfoFont)
    InfoTuple = (InfoLabel, InfoEntry)
    return InfoEntry, InfoTuple

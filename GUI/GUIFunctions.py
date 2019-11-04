from math import ceil, log
from tkinter import *
from tkinter import messagebox
import GUI.GUIWidgetMaker as wm
import GUI.GUIFileReader as fr
import numpy as np
import ast
from scipy.signal import savgol_filter

NUMBEROFGRAPHS = 2


# Dit bestand houd alle functionaliteit die nodig is voor de GUI. Het zijn wat simpele functies meestal.
# Geef een limit aan het aantal generaties die de grafiek laat zien
def x_limit(array):
    a = len(array)
    if a > 101:
        a = 101
    return a - 1


# Kap een groot getal af voor makkelijke waarden
def ceil_power_of_10(n):
    exp = log(n, 10)
    exp = ceil(exp)
    return 10 ** exp


# Geef waarde bij de correcte windturbine
def defWindTurbineCost(wm_type, wm_number):
    if wm_type == 2:
        wm_cost = 1605000
    elif wm_type == 3:
        wm_cost = 5350000
    elif wm_type == 1:
        wm_cost = 535000
    elif wm_type == 4:
        wm_cost = 3210000
    else:
        wm_cost = 0

    return wm_cost, wm_cost * wm_number


# Format een groot E getal netjes
def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]


# Geef een popup
def ShowErrorBox(title, message):
    messagebox.showerror(title, message)

# Ga naar de vorige Grafiek. True wordt gebruikt om het overzicht te resetten
def previousChart(GUI, starting=True):
    if GUI.graphNumber != 0:
        GUI.graphNumber = GUI.graphNumber - 1
    else:
        GUI.graphNumber = (NUMBEROFGRAPHS-1)
    loadChart(GUI, starting)

# Ga naar de vorige Grafiek. True wordt gebruikt om het overzicht te resetten
def nextChart(GUI, starting=True):
    if GUI.graphNumber != (NUMBEROFGRAPHS-1):
        GUI.graphNumber = GUI.graphNumber + 1
    else:
        GUI.graphNumber = 0
    loadChart(GUI, starting)


# Laat de volgende grafiek zien
def loadChart(GUI, starting=True):
    GUI.a.clear()
    GUI.a.axis('auto')
    GUI.a.axis('on')
    if starting:  # Start bij de eeste
        GUI.graphNumber = 0

    # Instellingen voor de eerste grafiek: Minium Kosten
    if GUI.graphNumber == 0:
        Length = len(GUI.gens) - 1
        if Length < 20:
            GUI.a.plot(GUI.gens, GUI.minCost, color='blue', label="Laagste Kosten")
        else:
            GUI.a.plot(GUI.gens[Length-20:Length], GUI.minCost[Length-20:Length], color='blue', label="Laagste Kosten")
        GUI.a.set_yscale("log")
        GUI.a.set(ylabel="Bedrag in euro's (€)", xlabel="Generatie", title="Laagste Kosten")
        limit = x_limit(GUI.gens)

        if Length < 20:
            GUI.a.set_xlim(GUI.gens[0], GUI.gens[limit])
        else:
            GUI.a.set_xlim(GUI.gens[limit-20], GUI.gens[limit-1])
        GUI.a.legend()

    # Instellingen voor de tweede grafiek: Gemiddelde Kosten
    elif GUI.graphNumber == 1:
        Length = len(GUI.gens) - 1
        if(Length < 20):
            GUI.a.plot(GUI.gens, GUI.meanCost, color='red', label="Gemiddelde kosten")
        else:
            GUI.a.plot(GUI.gens[Length-20:Length], GUI.meanCost[Length-20:Length], color='red', label="Gemiddelde kosten")
        GUI.a.set_yscale("log")
        GUI.a.set(ylabel="Bedrag in euro's (€)", xlabel="Generatie", title="Gemiddelde kosten")
        limit = x_limit(GUI.gens)
        if Length < 20:
            GUI.a.set_xlim(GUI.gens[0], GUI.gens[limit])
        else:
            GUI.a.set_xlim(GUI.gens[limit-20], GUI.gens[limit-1])
        GUI.a.legend()

    # Instellingen voor de derde grafiek: Energie Productie
    elif GUI.graphNumber == 2:
        GUI.a.plot(GUI.kW_distribution, color='green', alpha=0.5, label="Geproduceerd")
        GUI.a.plot(GUI.consumption, color='red', label="Consumptie")
        GUI.a.set(ylabel="KWH", xlabel="Dagen", title="Energie geproduceerd")
        GUI.a.set_xlim(0, 365)
        GUI.a.legend()

    # Instellingen voor de vierde grafiek: Som van overproductie
    elif GUI.graphNumber == 3:
        GUI.a.plot(GUI.KW_sum, color='green', alpha=0.5, label="Som Energie surplus")
        GUI.a.plot(GUI.zeros, color='red', label="0 lijn")
        GUI.a.set(ylabel="KWH", xlabel="Dagen", title="Som van Energie geproduceerd")
        GUI.a.set_xlim(0, 365)
        GUI.a.legend()

    # Instellingen voor de 5de grafiek: Pie chart met verdeling van de energie productie
    elif GUI.graphNumber == 4:
        WindPerc = str(round(float((GUI.WindSum / (GUI.WindSum + GUI.SolarSum)) * 100), 2))
        SolarPerc = str(round(float((GUI.SolarSum / (GUI.WindSum + GUI.SolarSum)) * 100), 2))
        Labels = 'Wind Turbines - ' + WindPerc + '%', 'Zonnepanelen - ' + SolarPerc + '%'
        colors = ['gold', 'dodgerblue']
        patches, _ = GUI.a.pie([GUI.WindSum, GUI.SolarSum], colors=colors, startangle=90, frame=True)
        GUI.a.legend(patches, Labels, loc="best")
        GUI.a.axis('equal')  # Zorg er voor dat de PieChart Rond is
        GUI.a.axis('off')  # Zet de assen uit voor een plaatje

    GUI.canvas.draw()


# Haal de bestaande grafiek weg om verwarring te voorkomen, en laat een wit vlak zien met "Gegevens ophalen"
def clearGraph(GUI):
    GUI.a.clear()
    GUI.a.plot([0], [0])
    GUI.a.axis('off')
    GUI.a.set_title("Gegevens ophalen")
    GUI.canvas.draw()
    GUI.nextButton.config(state="disabled")
    GUI.previousButton.config(state="disabled")


# Als er een nieuwe generatie is roept hij dit aan
def updateGraph(directory, gen, PowerArraySting, GUI):
    csvFileName = directory + "best_" + str(gen - 1) + ".csv"  # Pak het goede CSV bestand
    fr.loadCsvFile(GUI, csvFileName)  # Laad deze in de vleden
    first = not gen > 1  # Als het de eerste generatie is, wil je geen grafiek, want het is een punt
    loggingFileName = directory + "log.txt"  # Pak het goede logging bestand
    fr.loadLoggingFile(GUI, first, loggingFileName)  # Laat het logging bestand is
    # setUpPower(PowerArraySting, GUI)  # Setup voor de derde grafiek

# Maak alle velden leeg
def clearFields(GUI):
    counter = 0
    empty = "  " + str(0)

    # Voor de zonnenpanelen moet wil je er doorheen loopen om het in te vullen
    iterSolar = iter(GUI.SolarTupleList)
    next(iterSolar)
    for tupleItem in iterSolar:
        iterTuple = iter(tupleItem)  # Sla de eerste over want dat is text
        next(iterTuple)
        for item in iterTuple:  # Vul de waarden en
            item.config(text=empty)
            counter += 1

    # Gegevens voor de windturbines
    entry = GUI.WTHeightTuple[1]
    entry.config(text=empty)

    cost = GUI.WTHeightTuple[2]
    cost.config(text=empty)

    total = GUI.WTHeightTuple[3]
    total.config(text=empty)

    GUI.TotalCost.config(text="  €0,00")

# Deze methode wordt gebruikt om de grafiek te maken met het energie productie/verbruik
def setUpPower(MultiListString, GUI):
    MultiList = ast.literal_eval(MultiListString)  # Verander string van list naar list
    WindArray = [item[1] for item in MultiList]  # Haal wind eruit
    SolarArray = [item[2] for item in MultiList]  # Haal Solar eruit
    PowerArrayPre = [sum(x) for x in zip(*[WindArray, SolarArray])]  # Voeg samen voor de sum
    GUI.WindSum = sum(WindArray)
    GUI.SolarSum = sum(SolarArray)

    PowerArray = np.mean(np.reshape(PowerArrayPre[:8760], (365, 24)), axis=1)  # Zet gegevens om naar dag
    PowerArray = savgol_filter(PowerArray, 51, 3)  # Smooth out line
    GUI.consumption = np.full(len(PowerArray), GUI.consumptionGrade)  # Maak de consumptie lijn
    GUI.kW_distribution = PowerArray
    GUI.KW_sum = np.cumsum(PowerArray - GUI.consumptionGrade)  # Maak de som van de energie
    GUI.zeros = np.zeros(len(PowerArray))  # Maak nul lijn


# Sluit het programma af en sluit de thread als hij runt
def exitProgram(GUI):
    try:
        GUI.parent.destroy()
        GUI.p1.kill()
    except AttributeError as e:
        print("Nog niet gestart")

# Deze methode opent het popup scherm met de instellingen
def openCostFunctionSettingWindow(GUI):
    GUI.NewWindow = Toplevel(GUI.parent)
    font = GUI.InfoFont
    settings = GUI.settingsDataFrame
    displayCostFunction(GUI.NewWindow, font, settings, GUI)

# Deze methode voegt de widgets toe aan het popup scherm
def displayCostFunction(NewWindow, font, settings, GUI):
    RowCounter = 0
    padx = 10
    pady = 10
    preSaveEntries = []
    for index, row in settings.iterrows():
        Tuple = createCostFunctionPair(NewWindow, row[1], row[2], font)
        Tuple[0].grid(row=RowCounter, column=0, padx=padx, pady=pady, sticky=N + S)
        Tuple[1].grid(row=RowCounter, column=1, padx=padx, pady=pady, sticky=N + S)
        preSaveEntries.append(Tuple[1])
        RowCounter = RowCounter + 1
    SaveButton = wm.makeButton(GUI, "GUI/icons/save.png", NewWindow, NewWindow, "Opslaan", SaveValues, True)
    SaveButton.grid(row=RowCounter, column=0, columnspan=2, pady=pady, padx=padx, sticky=N + S + E + W)
    GUI.preSave = preSaveEntries

# Deze methode maakt een paar van de widgets voor item in de instellingen list
def createCostFunctionPair(NewWindow, textValue, startingValue, font):
    LabelWidth = 30
    ItemLabel = Label(NewWindow, text=textValue, width=LabelWidth, font=font, anchor=W)
    ItemEntry = Entry(NewWindow)
    ItemEntry.insert(0, str(startingValue))
    Tuple = (ItemLabel, ItemEntry)
    return Tuple

# Deze methode slaat de gegeven van het popupscherm op
def SaveValues(GUI):
    EntryArray = GUI.preSave
    for x in range(len(EntryArray)):
        GUI.settingsDataFrame.loc[x, 'value'] = float(EntryArray[x].get())
    GUI.NewWindow.destroy()


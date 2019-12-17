import shutil
from math import ceil, log
from os import listdir
from os.path import join, isfile
from tkinter import *
from tkinter import messagebox
from . import GUIWidgetMaker as wm
import numpy as np
from scipy.signal import savgol_filter
from matplotlib import ticker
import babel.numbers as bb
import pandas as pd
from tkinter.filedialog import askopenfilename
import csv
import matplotlib.patches as mpatches
from math import log10, floor
import time

# Dit bestand geeft functies voor het inlezen van de bestanden en invullen van de velden
textPreSpace = "  "
NUMBEROFGRAPHS = 7


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
        GUI.graphNumber = (NUMBEROFGRAPHS - 1)
    loadChart(GUI, starting, GUI.fullGraph)


# Ga naar de vorige Grafiek. True wordt gebruikt om het overzicht te resetten
def nextChart(GUI, starting=True):
    if GUI.graphNumber != (NUMBEROFGRAPHS - 1):
        GUI.graphNumber = GUI.graphNumber + 1
    else:
        GUI.graphNumber = 0
    loadChart(GUI, starting, GUI.fullGraph)


def round_sig(x, sig=2):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


# Laat de volgende grafiek zien
def loadChart(GUI, starting=True, fullChart=False):
    if fullChart:
        GrafiekLengte = len(GUI.gens)
    else:
        GrafiekLengte = int(GUI.getValueFromSettingsByName("tickLimit"))
    GUI.a.clear()
    GUI.a.axis('auto')
    GUI.a.axis('on')
    titlePretext = GUI.locationTextVariable.get() + " - " + GUI.yearTextVariable.get() + "\n"
    if starting:  # Start bij de eeste
        GUI.graphNumber = 0

    # Instellingen voor de eerste grafiek: Minium Kosten
    if GUI.graphNumber == 0:
        Length = len(GUI.gens)
        if Length < GrafiekLengte:
            GUI.a.plot(GUI.gens, GUI.minCost, color='blue', label="Laagste Kosten")
        else:
            GUI.a.plot(GUI.gens[Length - GrafiekLengte:Length], GUI.minCost[Length - GrafiekLengte:Length],
                       color='blue', label="Laagste Kosten")
        GUI.a.set_yscale("log")
        GUI.a.set(ylabel="Bedrag in euro's (€)", xlabel="Generatie", title=titlePretext + "Laagste Kosten")
        limit = x_limit(GUI.gens)
        # GUI.a.tight_layout()

        if Length < GrafiekLengte:
            GUI.a.set_xlim(GUI.gens[0], GUI.gens[limit])
        else:
            GUI.a.set_xlim(GUI.gens[limit - GrafiekLengte + 1], GUI.gens[limit])
            xticks = ticker.MaxNLocator(20)
            GUI.a.xaxis.set_major_locator(xticks)
        GUI.a.legend()

    # Instellingen voor de tweede grafiek: Gemiddelde Kosten
    elif GUI.graphNumber == 1:
        Length = len(GUI.gens)
        if (Length < GrafiekLengte):
            GUI.a.plot(GUI.gens, GUI.meanCost, color='red',
                       label="Gemiddelde kosten van alle simulaties deze generatie")
        else:
            GUI.a.plot(GUI.gens[Length - GrafiekLengte:Length], GUI.meanCost[Length - GrafiekLengte:Length],
                       color='red', label="Gemiddelde kosten")
        GUI.a.set_yscale("log")
        GUI.a.set(ylabel="Bedrag in euro's (€)", xlabel="Generatie", title=titlePretext + "Gemiddelde kosten")
        limit = x_limit(GUI.gens)
        # GUI.a.tight_layout()
        if Length < GrafiekLengte:
            GUI.a.set_xlim(GUI.gens[0], GUI.gens[limit])
        else:
            GUI.a.set_xlim(GUI.gens[limit - GrafiekLengte + 1], GUI.gens[limit])
            xticks = ticker.MaxNLocator(20)
            GUI.a.xaxis.set_major_locator(xticks)
        GUI.a.legend()

    # Instellingen voor de derde grafiek: Energie Productie
    elif GUI.graphNumber == 2:
        GUI.a.plot(GUI.kW_distribution, color='green', alpha=0.5, label="Geproduceerd")
        GUI.a.plot(GUI.consumption, color='red', label="Consumptie")
        GUI.a.set(ylabel="kW", xlabel="Dagen", title=titlePretext + "Jaarlijks vermogen")
        GUI.a.set_xlim(0, 365)
        GUI.a.legend()

    # Instellingen voor de vierde grafiek: Som van overproductie
    elif GUI.graphNumber == 3:
        GUI.a.plot(GUI.KW_sum, color='green', alpha=0.5, label="Energie productie - vraag")
        GUI.a.plot(GUI.zeros, color='red', label="0 lijn")
        GUI.a.set(ylabel="MWh", xlabel="Dagen", title=titlePretext + "\u03A3(Energie productie - vraag)")
        GUI.a.set_xlim(0, 365)
        PowerPlantPower = GUI.getValueFromSettingsByName("powerplant_power") * 365 * 24 / 1000
        maxValue = np.max(GUI.KW_sum) + PowerPlantPower
        verdeling = "Vraag is " + str(round_sig((PowerPlantPower / maxValue) * 100)) + "% van totaal."
        balans = mpatches.Patch(color='green', label='Energie productie - vraag', linewidth=1)
        nul_line = mpatches.Patch(color='red', label='0 Lijn', linewidth=1)
        percentage = mpatches.Patch(alpha=0, label=verdeling)
        GUI.a.legend(handles=[balans, nul_line, percentage])

    # Instellingen voor de zesde grafiek: Gebruik van de accu's.
    elif GUI.graphNumber == 4:
        batteryCharge = []
        for x in range(2):
            if x == 0:
                batteryCharge = [int(GUI.cost_stats['total_storage'])]
            else:
                batteryCharge = [batteryCharge[-1]]
            PowerShortage = []
            for I in GUI.BatteryPower:
                batteryCharge.append(batteryCharge[-1] + I)
                if int(GUI.cost_stats['total_storage']) < batteryCharge[-1]:
                    batteryCharge[-1] = int(GUI.cost_stats['total_storage'])
                elif 0 > batteryCharge[-1]:
                    batteryCharge[-1] = 0
                    PowerShortage.append(len(batteryCharge) - 1)
        batteryChargePlot = np.mean(np.reshape(batteryCharge[:8760], (365, 24)),
                                    axis=1) / 1000  # Zet gegevens om naar dag
        GUI.a.plot(batteryChargePlot, color='green', alpha=0.5, label="Niveau van de accu")
        GUI.a.set(ylabel="MWh", xlabel="Uren", title=titlePretext + "Accu gebruik over het jaar")
        GUI.a.set_ylim(0, max(batteryChargePlot) * 1.1)
        GUI.a.set_xlim(0, 365)
        GUI.a.legend()

        # Instellingen voor de vijfde grafiek: Pie chart met verdeling van de energie productie
    elif GUI.graphNumber == 5:
        WindPerc = str(round(float((GUI.WindSum / (GUI.WindSum + GUI.SolarSum)) * 100), 2))
        SolarPerc = str(round(float((GUI.SolarSum / (GUI.WindSum + GUI.SolarSum)) * 100), 2))
        Labels = 'Wind Turbines - ' + WindPerc + '%', 'Zonnepanelen - ' + SolarPerc + '%'
        colors = ['dodgerblue', 'gold']
        patches, _ = GUI.a.pie([GUI.WindSum, GUI.SolarSum], colors=colors, startangle=90, frame=True)
        GUI.a.set_title(titlePretext + "Verdeling van energie bron")
        GUI.a.legend(patches, Labels, loc="upper right")
        GUI.a.axis('equal')  # Zorg er voor dat de PieChart Rond is
        GUI.a.axis('off')  # Zet de assen uit voor een plaatje

        # Instellingen voor de vijfde grafiek: Pie chart met verdeling van de energie productie
    elif GUI.graphNumber == 6:
        data, labels = calTotalCosts(GUI.cost_stats)
        patches, _ = GUI.a.pie([data], startangle=90, frame=True)
        GUI.a.set_title(titlePretext + "Kosten overzicht")
        GUI.a.legend(patches, labels=labels, loc="upper right")
        GUI.a.axis('equal')  # Zorg er voor dat de PieChart Rond is
        GUI.a.axis('off')  # Zet de assen uit voor een plaatje

    GUI.canvas.draw()


def RunSimulation(GUI):
    N_PANELS = 4
    N_SOLAR_FEATURES = N_PANELS * 3
    n_Turbines = round(float(GUI.csvData[-2]))
    turbine_height = round(float(GUI.csvData[-1]))
    sp_efficiency = GUI.getValueFromSettingsByName("solar_efficiency")

    for i in range(len(GUI.csvData)):
        GUI.csvData[i] = float(GUI.csvData[i])

    energy_production, energy_split = \
        GUI.simulator.calc_total_power(
            GUI.csvData[:N_SOLAR_FEATURES],
            list([n_Turbines, turbine_height]),
            sp_efficiency)
    GUI.Wind_Solar_Array = energy_split
    BatteryPowerPreShape = energy_production - 6000
    GUI.BatteryPower = BatteryPowerPreShape
    sp_sm = np.sum(GUI.csvData[0:N_SOLAR_FEATURES:3])
    wm_type = GUI.getValueFromSettingsByName("windturbine_type")
    GUI.cost_stats = GUI.CostCalulator.get_stats(energy_production, sp_sm, wm_type, n_Turbines)


def resetToDefaultSettings(GUI):
    defaultDataFrame = pd.read_csv("GUI/default_settings.csv")
    GUI.settingsDataFrame = defaultDataFrame
    GUI.settingsDataFrame.to_csv(GUI.fileName, index=None, header=True)
    chosenLocation = 'NEN'
    chosenYear = 2018
    GUI.setLocationYear(chosenLocation, chosenYear)
    GUI.NewWindow.destroy()
    GUI.settingsMenuOpen = False


def calTotalCosts(cost_stats):
    wind_cost = cost_stats['wind_cost']
    solar_cost = cost_stats['solar_cost']
    cable_cost = cost_stats['cable_cost']
    storage_cost = round(cost_stats['storage_cost'])
    deficit_cost = cost_stats['deficit_cost']
    sumOthers = wind_cost + solar_cost + cable_cost + storage_cost + deficit_cost
    data = [wind_cost, solar_cost, cable_cost, storage_cost, deficit_cost]
    labels = ["Windmolens", "Zonnepanelen", "Kabel", "Opslag", "Te kort"]
    for i in range(len(data)):
        percentage = (data[i] / sumOthers) * 100
        rounded_percentage = round(percentage, ndigits=2)
        euro_string = bb.format_currency(data[i], 'EUR', locale='en_US')
        labels[i] = labels[i] + ": " + euro_string + " - (" + str(rounded_percentage) + "%)"

    return data, labels


# Haal de bestaande grafiek weg om verwarring te voorkomen, en laat een wit vlak zien met "Gegevens ophalen"
def clearGraph(GUI):
    GUI.a.clear()
    GUI.a.plot([0], [0])
    GUI.a.axis('off')
    GUI.a.set_title("Gegevens inladen")
    GUI.RunButton.config(state="disabled", text="   Stop", image=GUI.StopIcon)  # Verander de tekst op de knop
    GUI.nextButton.config(state="disabled")
    GUI.previousButton.config(state="disabled")
    GUI.chartButton.config(state="disabled")
    GUI.canvas.draw()


# Als er een nieuwe generatie is roept hij dit aan
def ReadLogging(directory, gen, GUI):
    csvFileName = directory + "best_" + str(gen - 1) + ".csv"  # Pak het goede CSV bestand
    loadCsvFile(GUI, csvFileName)  # Laad deze in de vleden
    first = not gen > 1  # Als het de eerste generatie is, wil je geen grafiek, want het is een punt
    loggingFileName = directory + "log.txt"  # Pak het goede logging bestand
    loadLoggingFile(GUI, first, loggingFileName)  # Laat het logging bestand is


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
def setUpPower(GUI):
    WindArray = GUI.Wind_Solar_Array[0]  # Haal wind eruit
    SolarArray = GUI.Wind_Solar_Array[1]  # Haal Solar eruit
    PowerArrayPre = [x + y for x, y in zip(WindArray, SolarArray)]  # Voeg samen voor de sum
    GUI.WindSum = sum(WindArray)
    GUI.SolarSum = sum(SolarArray)

    # omzetten Array naar dag
    PowerArray = np.mean(np.reshape(PowerArrayPre[:8760], (365, 24)), axis=1)  # Zet gegevens om naar dag

    # Geproducueerd vs gebrijkte lijn
    PowerArray = savgol_filter(PowerArray, 51, 3)  # Smooth out line
    GUI.consumption = np.full(len(PowerArray), GUI.consumptionGrade)  # Maak de consumptie lijn
    GUI.kW_distribution = PowerArray

    # Sum of Overproduced Power
    GUI.KW_sum = np.cumsum(PowerArray - GUI.consumptionGrade)  # Maak de som van de energie
    GUI.zeros = np.zeros(len(PowerArray))  # Maak nul lijn


# Sluit het programma af en sluit de thread als hij runt
def exitProgram(GUI):
    try:
        GUI.parent.destroy()
        GUI.p1.kill()
        print(GUI.Directory.value)
        shutil.rmtree(GUI.Directory.value)

    except PermissionError as e:
        time.sleep(5)
        shutil.rmtree(GUI.Directory.value)
        print("Nog niet gestart")

    except AttributeError as e:
        print("Nog niet gestart")


def deleteSavedRunsFolder(filepath):
    file = filepath + "log.txt"


# Deze methode opent het popup scherm met de instellingen
def openCostFunctionSettingWindow(GUI):
    GUI.NewWindow = Toplevel(GUI.parent)
    percentage = 0.65
    screen_width = int(GUI.winfo_screenwidth() * percentage)
    aspect_ratio = 1600 / 500
    screen_height = int(screen_width / aspect_ratio)
    GUI.NewWindow.geometry(str(screen_width) + "x" + str(screen_height))
    font = GUI.InfoFont
    settings = GUI.settingsDataFrame
    GUI.NewWindow.grab_set()
    displayCostFunction(GUI.NewWindow, font, settings, GUI)


# Deze methode voegt de widgets toe aan het popup scherm
def displayCostFunction(NewWindow, font, settings, GUI):
    ColumnCounter = -2
    RowCounter = 8
    padx = 10
    pady = 10
    preSaveEntries = []
    headerCounter = 8
    LabelWidth = 30
    headerList = ["Instellingen voor het algortime", "Zonne- en windinstellingen", "Kabel, locatie, jaar en opslaan"]
    headerIndex = 0
    for index, row in settings.iterrows():
        if headerCounter - RowCounter == 0:
            ColumnCounter = ColumnCounter + 2
            costFunctionHeader(NewWindow, headerList[headerIndex], ColumnCounter, GUI, padx, pady)
            RowCounter = 1
            headerIndex += 1
        Tuple = createCostFunctionPair(NewWindow, row[1], row[2], font, LabelWidth)
        Tuple[0].grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N + S)
        Tuple[1].grid(row=RowCounter, column=ColumnCounter + 1, padx=padx, pady=pady, sticky=N + S)
        preSaveEntries.append(Tuple[1])
        RowCounter = RowCounter + 1

    GUI.yearOptionMenu = OptionMenu(NewWindow, GUI.yearStringVar, '')
    GUI.locationOptionMenu = OptionMenu(NewWindow, GUI.locationStringVar, *GUI.locationYearSheet.keys())

    locationLabel = Label(NewWindow, text="Locatie", width=30, font=font, anchor=W)
    locationLabel.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N + S)
    GUI.locationStringVar.set(GUI.savedLocation)
    GUI.locationOptionMenu.grid(row=RowCounter, column=ColumnCounter + 1, padx=padx, pady=pady, sticky=N + S + E + W)
    RowCounter = RowCounter + 1

    locationLabel = Label(NewWindow, text="Jaar", width=30, font=font, anchor=W)
    locationLabel.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N + S)
    GUI.yearOptionMenu.grid(row=RowCounter, column=ColumnCounter + 1, padx=padx, pady=pady, sticky=N + S + E + W)
    RowCounter = RowCounter + 1

    ResetButton = wm.makeButton(GUI, "GUI/icons/reset.png", NewWindow, NewWindow, "   Zet terug naar default",
                                resetToDefaultSettings, True)
    ResetButton.grid(row=RowCounter, column=ColumnCounter, columnspan=2, rowspan=2, pady=pady, padx=padx,
                     sticky=N + S + E + W)
    RowCounter = RowCounter + 2

    SaveButton = wm.makeButton(GUI, "GUI/icons/save.png", NewWindow, NewWindow, "   Opslaan", SaveValues, True)
    SaveButton.grid(row=RowCounter, column=ColumnCounter, columnspan=2, rowspan=2, pady=pady, padx=padx,
                    sticky=N + S + E + W)
    GUI.preSave = preSaveEntries
    GUI.setColumnRowConfigure([NewWindow])


def costFunctionHeader(NewWindow, Tekst, column, GUI, padx, pady):
    headerLabel = Label(NewWindow, text=Tekst, width=30, font=GUI.HFont, anchor=W)
    headerLabel.grid(row=0, column=column, padx=padx, pady=pady, sticky=N + S)


# Deze methode maakt een paar van de widgets voor item in de instellingen list
def createCostFunctionPair(NewWindow, textValue, startingValue, font, LabelWidth):
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
    GUI.settingsDataFrame.to_csv(GUI.fileName, index=None, header=True)
    chosenLocation = GUI.locationStringVar.get()
    chosenYear = GUI.yearStringVar.get()
    GUI.setLocationYear(chosenLocation, chosenYear)
    GUI.NewWindow.destroy()
    GUI.locationTextVariable.set(chosenLocation)
    GUI.yearTextVariable.set(chosenYear)
    GUI.settingsMenuOpen = False


def fullChart(GUI):
    if len(GUI.gens) > 1:
        GUI.fullGraph = not GUI.fullGraph
        loadChart(GUI, starting=False, fullChart=GUI.fullGraph)


# Deze methode opent het popup scherm met de instellingen
def displayLowestFindWindow(GUI):
    GUI.lowestFind = Toplevel(GUI.parent)
    font = GUI.InfoFont
    settings = GUI.settingsDataFrame
    fillLowestFindWindow(GUI.lowestFind, font, settings, GUI)


# Deze methode voegt de widgets toe aan het popup scherm
def fillLowestFindWindow(NewWindow, font, settings, GUI):
    lowestGen = GUI.minCost.index(min(GUI.minCost))
    if lowestGen != len(GUI.minCost) - 1:
        GUI.lowestGeneration = str(lowestGen + 1)
        generationText = "De laagste is niet gelijk aan de laatste. Dit was de " + GUI.lowestGeneration + "e generatie"
        continueText = "Wilt u overspringen naar de laagst en de bijbehorende waarden zien?"
        generationLabel = Label(NewWindow, text=generationText, anchor=W, font=font)
        generationLabel.pack(padx=10, pady=10)
        continueLabel = Label(NewWindow, text=continueText, anchor=W, font=font)
        continueLabel.pack(padx=10, pady=10)
        JumpButton = wm.makeButton(GUI, "GUI/icons/previous.png", NewWindow, NewWindow, "   Terug", loadPreviousGen,
                                   True)
        JumpButton.pack(padx=10, pady=10)
    else:
        textCorrect = "Het algoritme is klaar met berekenen. De gegevens op het scherm geven de de goedkoopste opstelling aan."
        textCorrectLabel = Label(NewWindow, text=textCorrect, anchor=W, font=font)
        textCorrectLabel.pack(padx=10, pady=10)
        CloseButton = wm.makeButton(GUI, "GUI/icons/tick.png", NewWindow, NewWindow, "   Akkoord", closeFinishedPopup,
                                    True)
        CloseButton.pack(padx=10, pady=10)


def loadPreviousGen(GUI):
    lg = GUI.lowestGeneration
    ReadLogging(GUI.Directory.value, int(lg), GUI)
    RunSimulation(GUI)
    setUpPower(GUI)
    closeFinishedPopup(GUI)
    GUI.minCost = GUI.minCost[0:int(lg)]
    GUI.meanCost = GUI.meanCost[0:int(lg)]
    GUI.gens = GUI.gens[0:int(lg)]
    GUI.generationTextVariable.set(GUI.setGenString(lg))
    loadChart(GUI)


def closeFinishedPopup(GUI):
    GUI.lowestFind.destroy()


# Dit bestand laad het loggin bestand in
def loadLoggingFile(GUI, first=None, filename=None):
    f = ""
    try:
        if filename is None:
            filename = askopenfilename()  # Dit gebeurd als je de knop indrukt, laat hij hem pakken
        if filename != '':  # Zolang het een normaal bestand is
            f = open(filename, "r")
            f1 = f.readlines()  # Lees het bestand
            genArray = []
            meanCostArray = []
            minCostArray = []

            for x in f1:  # Voor elke regel in het bestand, vul de arrays aan
                info = x.split(" ")
                info[5] = info[5].replace('\n', '')
                gen = int(info[1]) + 1
                genArray.append(str(gen))
                mean = round(float(info[3]), 2)
                minCost = round(float(info[5]), 2)
                meanCostArray.append(mean)
                minCostArray.append(minCost)

            # Geef de arrays terug aan de UI
            GUI.gens = genArray
            GUI.meanCost = meanCostArray
            GUI.minCost = minCostArray

            # Geef total cost in euro
            totalCostNumber = bb.format_currency(minCostArray[-1], 'EUR', locale='en_US')
            GUI.TotalCost.config(text=textPreSpace + str(totalCostNumber))

            # Zolang er meer dan twee waarden zijn, laat hij je naar de volgende grafiek gaan
            if not first:
                loadChart(GUI, False, GUI.fullGraph)
                GUI.nextButton.config(state="normal")
                GUI.previousButton.config(state="normal")
                GUI.chartButton.config(state="normal")
                GUI.RunButton.config(state="normal")

    except Exception as e:
        print(e)
        ShowErrorBox("Foutmelding verkeerd bestand",
                     "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")

    finally:
        f.close()


# Deze functie leest een CSV file in
def loadCsvFile(GUI, filename=None):
    try:
        if filename is None:
            filename = askopenfilename()  # Als je direct op de knop drukt laat hij je kiezen
        if filename != '':
            with open(filename, newline='') as csvfile:  # Lees het bestand in, in een array
                dataList = list(csv.reader(csvfile))
                GUI.csvData = dataList[0]
                counter = 0

                # Voor de zonnenpanelen moet wil je er doorheen loopen om het in te vullen
                iterSolar = iter(GUI.SolarTupleList)
                next(iterSolar)
                for tupleItem in iterSolar:
                    iterTuple = iter(tupleItem)  # Sla de eerste over want dat is text
                    next(iterTuple)
                    for item in iterTuple:  # Vul de waarden en
                        info = round(float(GUI.csvData[counter]), 2)
                        item.config(text=textPreSpace + str(info))
                        counter += 1

                # Gegevens voor de windturbines
                n_WindTurbines = round(float(GUI.csvData[-2]))
                h_WindTurbines = round(float(GUI.csvData[-1]))
                t_WindTurbines = round(float(GUI.getValueFromSettingsByName("windturbine_type")))

                entry = GUI.WTHeightTuple[1]
                entry.config(text=textPreSpace + str(n_WindTurbines))

                cost = GUI.WTHeightTuple[2]
                cost.config(text=textPreSpace + str(h_WindTurbines))

                total = GUI.WTHeightTuple[3]
                total.config(text=textPreSpace + str(t_WindTurbines))
    except Exception as e:
        print(e)
        ShowErrorBox("Foutmelding verkeerd bestand",
                     "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")

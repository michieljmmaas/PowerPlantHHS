from math import ceil, log
from tkinter import messagebox
import GUI.GUIFileReader as fr
import numpy as np
import ast
from scipy.signal import savgol_filter


# Dit bestand houd alle functionaliteit die nodig is voor de GUI. Het zijn wat simpele functies meestal.
# Geef een limit aan het aantal generaties die de grafiek laat zien
def x_limit(array):
    a = len(array)
    if a > 21:
        a = 21
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


# Laat de volgende grafiek zien
def nextChart(GUI, starting=True):
    GUI.a.clear()
    # GUI.a.axes.Axes.set_aspect('auto')  # resets
    GUI.a.axis('auto')
    GUI.a.axis('on')
    if starting:  # Start bij de eeste
        GUI.graphNumber = 0

    # Instellingen voor de eerste grafiek: Minium Kosten
    if GUI.graphNumber == 0:

        GUI.a.plot(GUI.gens, GUI.minCost, color='blue', label="Laagste Kosten")
        GUI.a.set_yscale("log")
        GUI.a.set(ylabel="Bedrag in euro's (€)", xlabel="Generatie", title="Laagste Kosten")
        limit = x_limit(GUI.gens)
        GUI.a.set_xlim(GUI.gens[0], GUI.gens[limit])
        GUI.a.legend()
        GUI.graphNumber = 1  # Als je nog een keer klikt krijg je de andere

    # Instellingen voor de tweede grafiek: Gemiddelde Kosten
    elif GUI.graphNumber == 1:
        GUI.a.plot(GUI.gens, GUI.meanCost, color='red', label="Gemiddelde kosten")
        GUI.a.set_yscale("log")
        GUI.a.set(ylabel="Bedrag in euro's (€)", xlabel="Generatie", title="Gemiddelde kosten")
        limit = x_limit(GUI.gens)
        GUI.a.set_xlim(GUI.gens[0], GUI.gens[limit])
        GUI.a.legend()
        GUI.graphNumber = 2  # Als je nog een keer klikt krijg je de andere

    # Instellingen voor de derde grafiek: Energie Productie
    elif GUI.graphNumber == 2:
        GUI.a.plot(GUI.kW_distribution, color='green', alpha=0.5, label="Geproduceerd")
        GUI.a.plot(GUI.consumption, color='red', label="Consumptie")
        GUI.a.set(ylabel="KWH", xlabel="Dagen", title="Energie geproduceerd")
        GUI.a.set_xlim(0, 365)
        GUI.a.legend()
        GUI.graphNumber = 3  # Als je nog een keer klikt krijg je de andere

    # Instellingen voor de vierde grafiek: Som van overproductie
    elif GUI.graphNumber == 3:
        GUI.a.plot(GUI.KW_sum, color='green', alpha=0.5, label="Som Energie surplus")
        GUI.a.plot(GUI.zeros, color='red', label="0 lijn")
        GUI.a.set(ylabel="KWH", xlabel="Dagen", title="Som van Energie geproduceerd")
        GUI.a.set_xlim(0, 365)
        GUI.a.legend()
        GUI.graphNumber = 4  # Als je nog een keer klikt krijg je de andere

    # Instellingen voor de 5de grafiek: Pie chart met verdeling van de energie productie
    elif GUI.graphNumber == 4:
        WindPerc = str(round(float((GUI.WindSum / (GUI.WindSum + GUI.SolarSum))*100), 2))
        SolarPerc = str(round(float((GUI.SolarSum / (GUI.WindSum + GUI.SolarSum)) * 100), 2))
        Labels = 'Wind Turbines - ' + WindPerc + '%', 'Zonnepanelen - ' + SolarPerc + '%'
        colors = ['gold', 'dodgerblue']
        patches, _ = GUI.a.pie([GUI.WindSum, GUI.SolarSum], colors=colors, startangle=90, frame=True)
        GUI.a.legend(patches, Labels, loc="best")
        GUI.a.axis('equal')  # Zorg er voor dat de PieChart Rond is
        GUI.a.axis('off')  # Zet de assen uit voor een plaatje
        GUI.graphNumber = 0  # Als je nog een keer klikt krijg je de andere

    GUI.canvas.draw()


# Haal de bestaande grafiek weg om verwarring te voorkomen, en laat een wit vlak zien met "Gegevens ophalen"
def clearGraph(GUI):
    GUI.a.clear()
    GUI.a.plot([0], [0])
    GUI.a.axis('off')
    GUI.a.set_title("Gegevens ophalen")
    GUI.canvas.draw()
    GUI.nextButton.config(state="disabled")


# Als er een nieuwe generatie is roept hij dit aan
def updateGraph(directory, gen, PowerArraySting, GUI):
    csvFileName = directory + "best_" + str(gen - 1) + ".csv"  # Pak het goede CSV bestand
    fr.loadCsvFile(GUI, csvFileName)  # Laad deze in de vleden
    first = not gen > 1  # Als het de eerste generatie is, wil je geen grafiek, want het is een punt
    loggingFileName = directory + "log.txt"  # Pak het goede logging bestand
    fr.loadLoggingFile(GUI, first, loggingFileName)  # Laat het logging bestand is
    setUpPower(PowerArraySting, GUI)  # Setup voor de derde grafiek


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


def setUpPower(MultiListString, GUI):
    MultiList = ast.literal_eval(MultiListString)  # Verander string van list naar list
    WindArray = [item[1] for item in MultiList]  # Haal wind eruit
    SolarArray = [item[2] for item in MultiList]  # Haal Solar eruit
    PowerArrayPre = [sum(x) for x in zip(*[WindArray, SolarArray])] # Voeg samen voor de sum
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
    GUI.parent.destroy()
    GUI.p1.kill()


# Deze functie laad standaard waarden in voor het genetische algortime
def fillEntries(GUI):
    GUI.InfoGenerationEntry.insert(0, '100')
    GUI.InfoPoolEntry.insert(0, '10')
    GUI.InfoMutationEntry.insert(0, '50')
    GUI.InfoPowerPlantEntry.insert(0, '6000')

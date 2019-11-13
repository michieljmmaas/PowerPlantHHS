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
import GUI.GUIWidgetMaker as wm
import calculate_cost as cc
import pandas as pd

DELAY1 = 20
DELAY2 = 1000


# Dit is de module voor de UI. Zat alle veldjes neer en runt de thread voor de funcites
# noinspection PyAttributeOutsideInit,PyUnresolvedReferences
class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, name="frame")
        self.parent = parent
        self.defineValues()
        self.SetSettings()
        self.makeFonts()
        self.initUI()  # Maak de UI
        self.grid()  # Het is een grid field
        self.parent.title("Danone Powerplant")  # Titel van het scherm
        # Vul standaard waarden in
        fn.clearFields(self)

    # Fonts die gebruikt woorden in de widgets
    def makeFonts(self):
        fontFamily = 'Helvetica'
        self.ButtonFont = fontMaker.Font(family=fontFamily, size=15, weight='bold')
        self.InfoFont = fontMaker.Font(family=fontFamily, size=10)
        self.HFont = fontMaker.Font(family=fontFamily, size=10, weight='bold')
        self.ColFont = fontMaker.Font(family=fontFamily, size=10)

    # Instellingen voor het aanroepen van Train. Dit gaat allemaal in een grote Dataframe die in het bestandje GUI/settings.csv staat. Als je iets toevoegd aan
    # InfoSet komt er ook een invul set van
    def SetSettings(self):
        self.fileName = "GUI/settings.csv"
        df = pd.read_csv(self.fileName)
        self.settingsDataFrame = df

    def defineValues(self):
        # Onderstaande waardes zijn allemaal de voor de grafieken
        self.gens = []  # X-as met de genertaties
        self.minCost = []  # Y-as met de minium cost
        self.meanCost = []  # Y-as met de mean cost
        self.settingsMenuOpen = False

        self.days = []  # Dagen in het jaar
        self.Uren = []  # Uren in het jaar
        self.kW_distribution = []  # Power opgewekt
        self.consumption = []  # Hoeveel de consumptie is van de fabriek
        self.consumptionGrade = 0  # Constante Vraag aan consumptie
        self.KW_sum = []  # Som van de KW Overproductie
        self.zeros = []  # Nul lijn
        self.SolarSum = 0  # Som van alle Solar Energie productie
        self.WindSum = 0  # Som van alle Wind Energie productie

        # Deze drie waarden zijn er om de grafiek te updaten
        self.counter = 0
        self.counterCheck = 0
        self.running = 0
        self.fullGraph = False

        self.preSave = []  # Deze wordt gebruikt om de Entry velden voor de instellingen in op te slaan.
        self.cb_cost_table = pd.DataFrame(
            {'area': [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400,
                      600, 1000, 1250, 1600, 2000, 3000, 5000, 8000, 10000, 12000, 15000,
                      18000, 22000, 25000, 30000, 40000, 50000],
             'cost': [0.002, 0.003, 0.008, 0.013, 0.014, 0.016, 0.025, 0.035, 0.075, 0.1, 0.15,
                      0.22, 0.3, 0.39, 0.49, 0.5, 0.62, 0.8, 1.25, 1.6, 2, 2.5, 3.5, 6, 9, 11,
                      13, 17.5, 20, 30, 40, 50, 60, 72]})

    def initUI(self):
        # Maakt de drie Frames aan van de GUI
        # Frame Grafiek Buttons, links boven met de knoppen
        FrameGrafiekButtons = Frame(self.parent)
        FrameGrafiekButtons.grid(row=0, column=0, columnspan=4, sticky=W + E + N + S)

        # Grafieken veld links
        FrameGrafiek = Frame(self.parent)
        FrameGrafiek.grid(row=1, column=0, rowspan=5, columnspan=4, sticky=W + E + N + S)

        # Rechter paneel met waarden
        ItemFrame = Frame(self.parent)
        ItemFrame.grid(row=0, column=6, rowspan=6, columnspan=2, sticky=W + E + N + S)

        # Hier onder worden de instellen van de grafiek gezet
        self.graphNumber = 0  # Wisselen tussen grafieken
        self.f = Figure(figsize=(8, 6), dpi=100)  # Maakt figuur waar de grafiek in komt
        self.a = self.f.add_subplot(111)  # Maakt grafiek
        self.a.plot([0], [0])  # Maak een standaard grafiek (dit geeft een leeg veld)
        self.a.axis('off')  # Laat assen niet zien voor een leeg scherm

        # Grafiek Buttons
        settingButton = wm.GrafiekButton(self, "GUI/icons/settings.png", FrameGrafiekButtons, FrameGrafiekButtons,
                                         fn.openCostFunctionSettingWindow, True)
        self.previousButton = wm.GrafiekButton(self, "GUI/icons/previous.png", FrameGrafiekButtons, FrameGrafiekButtons,
                                               fn.previousChart, False)
        self.previousButton.config(state='disabled')
        self.nextButton = wm.GrafiekButton(self, "GUI/icons/next.png", FrameGrafiekButtons, FrameGrafiekButtons,
                                           fn.nextChart, False)
        self.nextButton.config(state='disabled')
        self.chartButton = wm.GrafiekButton(self, "GUI/icons/chart.png", FrameGrafiekButtons, FrameGrafiekButtons,
                                            fn.fullChart, True)
        self.chartButton.config(state='disabled')

        # Voeg de knoppen toe
        settingButton.grid(row=0, column=0)
        self.previousButton.grid(row=0, column=1)
        self.nextButton.grid(row=0, column=2, pady=5)
        self.chartButton.grid(row=0, column=3, pady=5)

        # Hier onder worden de instellen van de grafiek gezet
        self.graphNumber = 0  # Wisselen tussen grafieken
        self.f = Figure(figsize=(8, 6), dpi=100)  # Maakt figuur waar de grafiek in komt
        self.a = self.f.add_subplot(111)  # Maakt grafiek

        self.a.plot([0], [0])  # Maak een standaard grafiek (dit geeft een leeg veld)
        self.a.axis('off')  # Laat assen niet zien voor een leeg scherm

        self.canvas = FigureCanvasTkAgg(self.f, FrameGrafiek)  # Plaats grafiek in UI
        self.canvas.get_tk_widget().pack(fill=BOTH)  # Spreid het over de ruimte die het heeft

        # Dit is de laad balk en de knop volgende grafiek. De knop staat uit want hij wisselt naar niets
        self.pbar = Progressbar(FrameGrafiek, mode='indeterminate')
        self.pbar.pack(fill=BOTH)

        # Maak de buttons aan
        self.RunButton = wm.makeButton(self, "GUI/icons/run-arrow.png", FrameGrafiek, ItemFrame, "   Run",
                                       self.runSimulation,
                                       False)
        LoadCSVButton = wm.makeButton(self, "GUI/icons/csv-file.png", FrameGrafiek, ItemFrame, " Laad CSV",
                                      fr.loadCsvFile,
                                      True)
        LoadTXTBButton = wm.makeButton(self, "GUI/icons/txt-file.png", FrameGrafiek, ItemFrame, " Laad TXT",
                                       fr.loadLoggingFile, True)
        ExitButton = wm.makeButton(self, "GUI/icons/error.png", FrameGrafiek, ItemFrame, " Afsluiten", fn.exitProgram,
                                   True)
        ActionTuple = (self.RunButton, LoadCSVButton, LoadTXTBButton, ExitButton)

        self.RunIcon = wm.makeIcon("GUI/icons/run-arrow.png",
                                   FrameGrafiek)  # Deze zijn nodig om te wissel van plaatje op de Run/Stop knop
        self.StopIcon = wm.makeIcon("GUI/icons/stop-button.png",
                                    FrameGrafiek)  # Deze zijn nodig om te wissel van plaatje op de Run/Stop knop

        # Rechterpaneel
        # Dit zijn standaard waarden die er voor zorgen dat alles even lang en breed is
        padx = 10
        pady = 10

        ColumnCounter = 0
        for Item in ActionTuple:
            Item.grid(row=0, column=ColumnCounter, padx=padx, pady=pady + 5, sticky=N + S)
            ColumnCounter = ColumnCounter + 1

        # Hier onder zijn alle rijen beschreven. Eerst worden alle widgets aangemaakt, en daarna in een Tuple gestopt.
        # De tuple wordt gebruikt om makkelijk in te lezen
        # Colom namen
        headerTuple = wm.HeaderRow("Onderwerp", "Aantal", "Factor", "Kosten", ItemFrame, self.HFont)

        # Energie Surplus: TO DO
        PWDSurplusTuple = wm.LabelRow("Energie Overschot", ItemFrame, self.HFont, self.ColFont)

        # Energie Deficit: TO DO
        PWDeficitTuple = wm.LabelRow("Energie Tekort", ItemFrame, self.HFont, self.ColFont)

        # Windturbine aantal
        self.WTHeightTuple = wm.LabelRow("Wind Turbine - Aantal", ItemFrame, self.HFont, self.ColFont)

        # Deze loop voegt alle boven aangemaakte Tuples toe aan het overzicht.
        # LabelTupleList = [ActionTuple, headerTuple, PWDSurplusTuple, PWDeficitTuple, self.WTHeightTuple]
        LabelTupleList = [headerTuple, self.WTHeightTuple]
        RowCounter = 1
        for Tuple in LabelTupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N + S)
                ColumnCounter = ColumnCounter + 1
            RowCounter = RowCounter + 1

        # Solar Panels info
        SPHeaderTuple = wm.HeaderRow("Zonnepaneel Nummer", "Oppervlakte (m\u00b2)", "Hoek in graden",
                                     "Oriëntatie t.o.v. Zuiden", ItemFrame, self.HFont)

        # Solar Panel 1
        SP1HeaderTuple = wm.LabelRow("Zonnepaneel 1", ItemFrame, self.HFont, self.ColFont)
        SP2HeaderTuple = wm.LabelRow("Zonnepaneel 2", ItemFrame, self.HFont, self.ColFont)
        SP3HeaderTuple = wm.LabelRow("Zonnepaneel 3", ItemFrame, self.HFont, self.ColFont)
        SP4HeaderTuple = wm.LabelRow("Zonnepaneel 4", ItemFrame, self.HFont, self.ColFont)

        self.SolarTupleList = [SPHeaderTuple, SP1HeaderTuple, SP2HeaderTuple, SP3HeaderTuple, SP4HeaderTuple]

        # Deze loop voegt alle Solarpanels toe
        for Tuple in self.SolarTupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N + S)
                ColumnCounter = ColumnCounter + 1
            RowCounter = RowCounter + 1

        # Dit maakt het overzicht van de totale kosten
        TotalLabel = Label(ItemFrame, text="Totale Kosten", height=2, relief=SOLID, font=("Helvetica", 20))
        TotalLabel.grid(row=RowCounter + 2, column=0, padx=padx, pady=pady, columnspan=2, sticky=W + E)

        self.TotalCost = Label(ItemFrame, width=20, height=2, anchor=W, relief=SUNKEN, font=("Helvetica", 20))
        self.TotalCost.grid(row=RowCounter + 2, column=2, columnspan=2, padx=padx, pady=pady, sticky=W + E)

    # Deze methode is er om het genetisch algoritme aan te roepen en de dingen in te stellen.
    def runSimulation(self):
        if self.running == 1:  # Als het genetisch algoritme aan het runnen is
            self.endSimulation()

            return
        else:  # Als de algoritme nog niet aan het trainen is. begin nu.
            try:
                # Haal de waarden op uit de velden. Met passende meldingen
                GenInfo = int(self.getValueFromSettingsByName("gens"))
                PoolInfo = int(self.getValueFromSettingsByName("pool"))
                MutationInfo = int(self.getValueFromSettingsByName("mutate_percentage"))
                PowerPlantInfo = int(self.getValueFromSettingsByName("powerplant_power"))
                infoArray = [GenInfo, PoolInfo, MutationInfo, PowerPlantInfo]
                self.consumptionGrade = PowerPlantInfo

            except ValueError:
                fn.ShowErrorBox("Invoerfout", "Controller of de getallen goed zijn ingevoerd")
                return

            if PoolInfo < 10:
                fn.ShowErrorBox("Waarschuwing",
                                "Voor een optimaal resultaat wordt het aangeraden om een Pool die groter is dan 10 mee te geven")
                return

            if GenInfo < 5:
                fn.ShowErrorBox("Waarschuwing",
                                "Voor een optimaal resultaat wordt het aangeraden om voor meer dan 10 generaties te draaien")
                return

            if MutationInfo > 100 or MutationInfo < 0:
                fn.ShowErrorBox("Waarschuwing",
                                "Het mutatie percentage moet tussen de 0 en de 100 liggen. Het wordt aangeraden om het het boven de 25% te houden.")
                return

            # Verwijder de bestaande grafiek
            fn.clearGraph(self)
            fn.clearFields(self)
            self.RunButton.config(text="   Stop", image=self.StopIcon)  # Verander de tekst op de knop
            self.manager = Manager()  # Dit is een manager die the Process waarden kan geven die je dan kan uitlezen.
            self.counter = Value('i',
                                 0)  # Dit is een waarde die ik van de andere thread kan uitlezen. Geeft aan welke generatie we zitten
            self.Directory = self.manager.Value(c_char_p, "first")  # Geef de manager een String die ik kan uitlezen
            self.PowerArray = self.manager.Value(c_char_p, "test")  # Geef de manager een String die ik kan uitlezen
            CostCalulator = self.getCostCalculator()
            surface_min = self.getValueFromSettingsByName("surface_min")
            surface_max = self.getValueFromSettingsByName("surface_max")
            windTurbineType = self.getValueFromSettingsByName("windturbine_type")
            solar_eff = int(self.getValueFromSettingsByName("solar_efficiency"))
            terrain_value = float(self.getValueFromSettingsByName("terrain"))
            windTurbineMax = self.getValueFromSettingsByName("windturbine_max")
            self.p1 = Process(target=runTrain, args=(
                self.counter, self.Directory, infoArray, self.PowerArray, CostCalulator, surface_min, surface_max,
                windTurbineType, windTurbineMax, terrain_value,
                solar_eff))  # Maak een thread aan die runTrain aanroept.

            self.p1.start()  # Start de thread
            self.pbar.start(DELAY1)  # Wacht even voor lag
            self.running = 1  # Zeg dat het algoritme aan het draaien is
            self.after(DELAY2, self.onGetValue)  # Start met het pollen van de de thread
            return

    def getValueFromSettingsByName(self, name):
        row = self.settingsDataFrame.loc[self.settingsDataFrame['name'] == name]
        return row.iloc[0, 2]

    # Deze functie polt de Thread om te kijken of hij al een generatie verder is. Als het nieuwe waarden heeft wordt de grafiek aangepast en de waarden ingevuld
    def onGetValue(self):
        if self.p1.is_alive():  # Zolang het proces draait
            if self.counter.value != self.counterCheck:  # En er is een nieuwe generatie
                self.counterCheck = self.counter.value
                fn.updateGraph(self.Directory.value, self.counterCheck, self.PowerArray.value, self)  # Update
            self.after(DELAY2, self.onGetValue)  # Check na een Delay nog een keer
            return
        else:  # Als de thread dood is, houd dan op met checken en stop de laadbalk.
            if self.running == 1:
                fn.updateGraph(self.Directory.value, self.counterCheck, self.PowerArray.value, self)  # Update
            print("Klaar")
            self.endSimulation()

    # Deze methode maakt een Cost Calculator met de waarden die ingesteld zijn op het scherm
    def getCostCalculator(self):
        CostCalculator = cc.CostCalculator(self.getValueFromSettingsByName("surface_area_costs"),
                                           self.getValueFromSettingsByName("storage_costs"),
                                           self.getValueFromSettingsByName("powerplant_power"),
                                           self.getValueFromSettingsByName("deficit_cost"), self.cb_cost_table,
                                           self.getValueFromSettingsByName("cable_length"),
                                           self.getValueFromSettingsByName("cable_voltage"))
        return CostCalculator

    def endSimulation(self):
        self.p1.kill()  # Stop de thread die traint
        self.running = 0  # Zet waarde naar niet meer running
        self.pbar.stop()  # Stop de progress bar met bewegen
        self.RunButton.config(text="    Run", image=self.RunIcon)  # Zet de text van de knop weer naar run
        self.counterCheck = 0  # Resest update check
        self.counter = 0  # Reset update check

        # Als er meer dan twee generaties zijn geweest, dan moet je nog kunnen wissel tussen de grafieken
        if len(self.gens) > 1:
            self.nextButton.config(state="normal")
            self.previousButton.config(state="normal")
            self.chartButton.config(state="normal")

        if len(self.gens) == self.getValueFromSettingsByName("gens"):
            fn.displayLowestFindWindow(self)


# Run de trainfunctie met mijn eigen waarden
def runTrain(counter, directory, array, PowerArray, CostCalculator, minSurface, maxSurface, windturbineType,
             windturbineMax, tr_rating, sp_eff):
    train(array[0], array[1], minSurface, maxSurface, 0, 90, 0, 359, model_name=None, load=False, counter=counter,
          directory=directory, mutationPercentage=array[2], target_kw=array[3], EnergyArray=PowerArray,
          cost_calculator=CostCalculator, windturbineType=windturbineType,
          N_WIND_MAX=windturbineMax, tr_rating=tr_rating, sp_efficiency=sp_eff)


# Maak en open een interface window
def main():
    root = Tk()
    app = Application(root)
    root.wm_iconbitmap("GUI/icons/icon.ico")
    root.mainloop()


if __name__ == '__main__':
    main()

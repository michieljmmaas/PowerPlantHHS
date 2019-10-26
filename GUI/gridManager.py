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

DELAY1 = 20
DELAY2 = 5000


# Dit is de module voor de UI. Zat alle veldjes neer en runt de thread voor de funcites
# noinspection PyAttributeOutsideInit,PyUnresolvedReferences
class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, name="frame")
        self.parent = parent
        self.defineValues()
        self.makeFonts()
        self.initUI()  # Maak de UI
        self.grid()  # Het is een grid field
        self.parent.title("Danone Powerplant")  # Titel van het scherm
        # Vul standaard waarden in
        fn.fillEntries(self)
        fn.clearFields(self)

    def makeFonts(self):
        fontFamily = 'Helvetica'
        self.ButtonFont = fontMaker.Font(family=fontFamily, size=15, weight='bold')
        self.InfoFont = fontMaker.Font(family=fontFamily, size=10)
        self.HFont = fontMaker.Font(family=fontFamily, size=10, weight='bold')
        self.ColFont = fontMaker.Font(family=fontFamily, size=10)

    def defineValues(self):
        # Onderstaande waardes zijn allemaal de voor de grafieken
        self.gens = []  # X-as met de genertaties
        self.minCost = []  # Y-as met de minium cost
        self.meanCost = []  # Y-as met de mean cost

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

    def initUI(self):
        # Maakt de drie velden aan
        # Grafieken
        Frame1 = Frame(self.parent)
        Frame1.grid(row=0, column=0, rowspan=5, columnspan=4, sticky=W + E + N + S)

        # Rechter paneel met waarden
        ItemFrame = Frame(self.parent)
        ItemFrame.grid(row=0, column=6, rowspan=6, columnspan=2, sticky=W + E + N + S)

        # Onderpaneel met items
        FrameBottom = Frame(self.parent)
        FrameBottom.grid(row=5, column=0, columnspan=4, rowspan=2, sticky=W + E + N + S)

        # Hier onder worden de instellen van de grafiek gezet
        self.graphNumber = 0  # Wisselen tussen grafieken
        self.f = Figure(figsize=(8, 5), dpi=100)  # Maakt figuur waar de grafiek in komt
        self.a = self.f.add_subplot(111)  # Maakt grafiek

        self.a.plot([0], [0])  # Maak een standaard grafiek (dit geeft een leeg veld)
        self.a.axis('off')  # Laat assen niet zien voor een hleeg scherm

        self.canvas = FigureCanvasTkAgg(self.f, Frame1)  # Plaats grafiek in UI
        self.canvas.get_tk_widget().pack(fill=BOTH)  # Spreid het over de ruimte die het heeft

        # Dit is de laad balk en de knop volgende grafiek. De knop staat uit want hij wisselt naar niets
        self.pbar = Progressbar(Frame1, mode='indeterminate')
        self.pbar.pack(fill=BOTH)
        self.nextButton = Button(Frame1, text="Volgende Grafiek", command=lambda: fn.nextChart(self, False),
                                 state="disabled")
        self.nextButton.pack()

        # Buttons
        self.RunButton = wm.makeButton(self, "GUI/icons/run-arrow.png", Frame1, ItemFrame, "   Run", self.runSimulation,
                                       False)
        LoadCSVButton = wm.makeButton(self, "GUI/icons/csv-file.png", Frame1, ItemFrame, " Laad CSV", fr.loadCsvFile,
                                      True)
        LoadTXTBButton = wm.makeButton(self, "GUI/icons/txt-file.png", Frame1, ItemFrame, " Laad TXT",
                                       fr.loadLoggingFile, True)
        ExitButton = wm.makeButton(self, "GUI/icons/error.png", Frame1, ItemFrame, " Afsluiten", fn.exitProgram, True)
        ActionTuple = (self.RunButton, LoadCSVButton, LoadTXTBButton, ExitButton)

        self.RunIcon = wm.makeIcon("GUI/icons/run-arrow.png", Frame1)
        self.StopIcon = wm.makeIcon("GUI/icons/stop-button.png", Frame1)

        # Rechterpaneel
        # Dit zijn standaard waarden die er voor zorgen dat alles even lang en breed is
        padx = 10
        pady = 10

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
        LabelTupleList = [ActionTuple, headerTuple, self.WTHeightTuple]
        RowCounter = 0
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

        # Hieronder worden de invul velden voor de genetisch algoritme gemaakt.
        self.InfoGenerationEntry, InfoGenerationTuple = wm.InfoItem("Generations", FrameBottom, self.InfoFont, self.HFont)
        self.InfoPoolEntry, InfoPoolTuple = wm.InfoItem("Pool", FrameBottom, self.InfoFont, self.HFont)
        self.InfoMutationEntry, InfoMutationTuple = wm.InfoItem("Mutation Rate (%)", FrameBottom, self.InfoFont, self.HFont)
        self.InfoPowerPlantEntry, InfoPowerPlantTuple = wm.InfoItem("PowerPlant Energie (KW)", FrameBottom, self.InfoFont, self.HFont)

        InfoTupleList = [InfoGenerationTuple, InfoPoolTuple, InfoMutationTuple, InfoPowerPlantTuple]

        # Deze loop voegt de Infotuples toe
        ColumnCounter = 0
        for Tuple in InfoTupleList:
            RowCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=W + E + N + S)
                RowCounter = RowCounter + 1
            ColumnCounter = ColumnCounter + 1

    # Deze methode is er om het genetisch algoritme aan te roepen en de dingen in te stellen.
    def runSimulation(self):
        if self.running == 1:  # Als het genetisch algoritme aan het runnen is
            self.p1.kill()  # Stop de thread die traint
            self.running = 0  # Zet waarde naar niet meer running
            self.pbar.stop()  # Stop de progress bar met bewegen
            self.RunButton.config(text="    Run", image=self.RunIcon)  # Zet de text van de knop weer naar run
            self.counterCheck = 0  # Resest update check
            self.counter = 0  # Reset update check

            # Als er meer dan twee generaties zijn geweest, dan moet je nog kunnen wissel tussen de grafieken
            if len(self.gens) > 1:
                self.nextButton.config(state="normal")

            return
        else:  # Als de algoritme nog niet aan het trainen is. begin nu.
            try:
                # Haal de waarden op uit de velden. Met passende meldingen
                GenInfo = int(self.InfoGenerationEntry.get())
                PoolInfo = int(self.InfoPoolEntry.get())
                MutationInfo = int(self.InfoMutationEntry.get())
                PowerPlantInfo = int(self.InfoPowerPlantEntry.get())
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
            self.manager = Manager()  # Dit is een manager die the Process waarden kan geven die je dan kan uitlezen.
            self.counter = Value('i',
                                 0)  # Dit is een waarde die ik van de andere thread kan uitlezen. Geeft aan welke generatie we zitten
            self.Directory = self.manager.Value(c_char_p, "test")  # Geef de manager een String die ik kan uitlezen
            self.PowerArray = self.manager.Value(c_char_p, "test")  # Geef de manager een String die ik kan uitlezen
            self.p1 = Process(target=runTrain, args=(
                self.counter, self.Directory, infoArray, self.PowerArray))  # Maak een thread aan die runTrain aanroept.
            self.p1.start()  # Start de thread
            self.pbar.start(DELAY1)  # Wacht even voor lag
            self.running = 1  # Zeg dat het algoritme aan het draaien is
            self.RunButton.config(text="   Stop", image=self.StopIcon)  # Verander de tekst op de knop
            self.after(DELAY2, self.onGetValue)  # Start met het pollen van de de thread
            return

    # Deze functie polt de Thread om te kijken of hij al een generatie verder is. Als het nieuwe waarden heeft wordt de grafiek aangepast en de waarden ingevuld
    def onGetValue(self):
        if self.p1.is_alive():  # Zolang het proces draait
            print("Checking")
            print("Counter: " + str(self.counter.value))
            if self.counter.value != self.counterCheck:  # En er is een nieuwe generatie
                self.counterCheck = self.counter.value
                fn.updateGraph(self.Directory.value, self.counterCheck, self.PowerArray.value,
                               self)  # Update de grafieken
            self.after(DELAY2, self.onGetValue)  # Check na een Delay nog een keer
            return
        else:  # Als de thread dood is, houd dan op met checken en stop de laadbalk.
            print("Klaar")
            self.pbar.stop()


# Run de trainfunctie met mijn eigen waarden
def runTrain(counter, directory, array, PowerArray):
    train(array[0], array[1], 0, 10000000, 0, 90, 0, 359, model_name=None, load=False, counter=counter,
          directory=directory, mutationPercentage=array[2], target_kw=array[3], EnergyArray=PowerArray)


# Maak en open een interface window
def main():
    root = Tk()
    app = Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()

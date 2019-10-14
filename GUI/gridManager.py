from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter.ttk import Progressbar
from train import train
from multiprocessing import Process, Value, Manager
from ctypes import c_char_p
import GUI.GUIFunctions as fn
import GUI.GUIFileReader as fr

DELAY1 = 20
DELAY2 = 5000


# noinspection PyAttributeOutsideInit,PyUnresolvedReferences
class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, name="frame")
        self.parent = parent
        self.initUI()
        self.grid()
        self.parent.title("Danone Powerplant")
        self.counter = 0
        self.counterCheck = 0
        self.running = 0
        fn.fillEntries(self)

    def initUI(self):
        Frame1 = Frame(self.parent)
        Frame1.grid(row=0, column=0, rowspan=5, columnspan=4, sticky=W + E + N + S)
        ItemFrame = Frame(self.parent)
        ItemFrame.grid(row=0, column=4, rowspan=6, columnspan=2, sticky=W + E + N + S)
        FrameBottom = Frame(self.parent)
        FrameBottom.grid(row=5, column=0, columnspan=4, rowspan=2, sticky=W + E + N + S)

        self.graphNumber = 0

        self.f = Figure(figsize=(5, 5), dpi=100)

        self.a = self.f.add_subplot(111)

        self.gens = []
        self.minCost = []
        self.meanCost = []

        self.a.plot([0], [0])
        self.a.axis('off')

        self.canvas = FigureCanvasTkAgg(self.f, Frame1)
        self.canvas.get_tk_widget().pack(fill=BOTH)

        self.pbar = Progressbar(Frame1, mode='indeterminate')
        self.pbar.pack(fill=BOTH)

        self.nextButton = Button(Frame1, text="Volgende Grafiek", command=lambda: fn.nextChart(self, False), state="disabled")
        self.nextButton.pack()

        padx = 10
        pady = 10
        LabelWidth = 20
        LabelHeight = 2

        LoadCSVButton = Button(ItemFrame, text="Laad Csv", width=LabelWidth, height=LabelHeight,
                            command=lambda: fr.loadCsvFile(self), relief=SOLID)
        LoadTXTBButton = Button(ItemFrame, text="Laad Logging", width=LabelWidth, height=LabelHeight,
                           command=lambda: fr.loadLoggingFile(self), relief=SOLID)
        self.RunButton = Button(ItemFrame, text="Run", width=LabelWidth, height=LabelHeight, command=self.runSimulation, relief=SOLID)
        ExitButton = Button(ItemFrame, text="Afsluiten", width=LabelWidth, height=LabelHeight,
                              command=lambda: fn.exitProgram(self), relief=SOLID)
        ActionTuple = (LoadCSVButton, LoadTXTBButton, self.RunButton, ExitButton)

        ItemLabel = Label(ItemFrame, text="Onderwerp", width=LabelWidth, height=LabelHeight, relief=SOLID)
        NumberLabel = Label(ItemFrame, text="Aantal", width=LabelWidth, height=LabelHeight, relief=SOLID)
        FactorLabel = Label(ItemFrame, text="Factor", width=LabelWidth, height=LabelHeight, relief=SOLID)
        CostLabel = Label(ItemFrame, text="Kosten", width=LabelWidth, height=LabelHeight, relief=SOLID)
        headerTuple = (ItemLabel, NumberLabel, FactorLabel, CostLabel)

        PWSurplusLabel = Label(ItemFrame, text="Energie Overschot", width=LabelWidth, height=LabelHeight, anchor=W,
                               relief=SOLID)
        PWSurplusEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                               bg="white")
        PWSurplusFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                bg="white")
        PWDSurplusCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                               bg="white")
        PWDSurplusTuple = (PWSurplusLabel, PWSurplusEntry, PWSurplusFactor, PWDSurplusCost)

        PWDeficitLabel = Label(ItemFrame, text="Energie Tekort", width=LabelWidth, height=LabelHeight, anchor=W,
                               relief=SOLID)
        PWDeficitEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                               bg="white")
        PWDeficitFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                bg="white")
        PWDeficitCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                              bg="white")
        PWDeficitTuple = (PWDeficitLabel, PWDeficitEntry, PWDeficitFactor, PWDeficitCost)

        WTNumberLabel = Label(ItemFrame, text="Wind Turbine - Aantal", width=LabelWidth, height=LabelHeight, anchor=W,
                              relief=SOLID)
        WTNumberEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                              bg="white")
        WTNumberFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                               bg="white")
        WTNumberCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                             bg="white")
        self.WTHeightTuple = (WTNumberLabel, WTNumberEntry, WTNumberFactor, WTNumberCost)

        LabelTupleList = [ActionTuple, headerTuple, PWDSurplusTuple, PWDeficitTuple, self.WTHeightTuple]
        RowCounter = 0
        for Tuple in LabelTupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N + S)
                ColumnCounter = ColumnCounter + 1
            RowCounter = RowCounter + 1

        # Solar Panels info
        SPNameLabel = Label(ItemFrame, text="Zonnepaneel Nummer", width=LabelWidth, height=LabelHeight, anchor=W,
                            relief=SOLID)
        SPSurfaceLabel = Label(ItemFrame, text="Oppervlakte (m\u00b2)", width=LabelWidth, height=LabelHeight, anchor=W,
                               relief=SOLID)
        SPAngleLabel = Label(ItemFrame, text="Hoek in graden", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SPOrientationLabel = Label(ItemFrame, text="Oriëntatie t.o.v. Zuiden", width=LabelWidth, height=LabelHeight,
                                   anchor=W, relief=SOLID)
        SPHeaderTuple = (SPNameLabel, SPSurfaceLabel, SPAngleLabel, SPOrientationLabel)

        # Solar Panel 1
        SP1NameLabel = Label(ItemFrame, text="Zonnepaneel 1", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SP1SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP1AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP1OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        SP1HeaderTuple = (SP1NameLabel, SP1SurfaceLabel, SP1AngleLabel, SP1OrientationLabel)

        # Solar Panel 2
        SP2NameLabel = Label(ItemFrame, text="Zonnepaneel 2", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SP2SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP2AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP2OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        SP2HeaderTuple = (SP2NameLabel, SP2SurfaceLabel, SP2AngleLabel, SP2OrientationLabel)

        # Solar Panel 3
        SP3NameLabel = Label(ItemFrame, text="Zonnepaneel 3", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SP3SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP3AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP3OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        SP3HeaderTuple = (SP3NameLabel, SP3SurfaceLabel, SP3AngleLabel, SP3OrientationLabel)

        # Solar Panel 4
        SP4NameLabel = Label(ItemFrame, text="Zonnepaneel 4", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SP4SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP4AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP4OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        SP4HeaderTuple = (SP4NameLabel, SP4SurfaceLabel, SP4AngleLabel, SP4OrientationLabel)

        self.SolarTupleList = [SPHeaderTuple, SP1HeaderTuple, SP2HeaderTuple, SP3HeaderTuple, SP4HeaderTuple]

        for Tuple in self.SolarTupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N + S)
                ColumnCounter = ColumnCounter + 1
            RowCounter = RowCounter + 1

        TotalLabel = Label(ItemFrame, text="Totale Kosten", height=5, relief=SOLID)
        TotalLabel.grid(row=RowCounter + 2, column=0, padx=padx, pady=pady, columnspan=3, sticky=W + E)

        self.TotalCost = Label(ItemFrame, width=20, height=5, anchor=W, relief=SUNKEN, bg="white")
        self.TotalCost.grid(row=RowCounter + 2, column=3, padx=padx, pady=pady, sticky=E)

        # Bottom info
        InfoGenerationLabel = Button(FrameBottom, text="Generations", width=LabelWidth, height=LabelHeight,
                                     relief=SOLID)
        self.InfoGenerationEntry = Entry(FrameBottom, font=("Helvetica", 10))
        # self.InfoGenerationEntry.tag_configure(justify='center')
        InfoGenerationTuple = (InfoGenerationLabel, self.InfoGenerationEntry)

        InfoPoolLabel = Button(FrameBottom, text="Pool", width=LabelWidth, height=LabelHeight, relief=SOLID)
        self.InfoPoolEntry = Entry(FrameBottom, font=("Helvetica", 10))
        InfoPoolTuple = (InfoPoolLabel, self.InfoPoolEntry)

        InfoMutationLabel = Button(FrameBottom, text="Mutation Rate (%)", width=LabelWidth, height=LabelHeight, relief=SOLID)
        self.InfoMutationEntry = Entry(FrameBottom, font=("Helvetica", 10))
        InfoMutationTuple = (InfoMutationLabel, self.InfoMutationEntry)

        InfoPowerPlantLabel = Button(FrameBottom, text="PowerPlant Energie (KW)", width=LabelWidth, height=LabelHeight,
                                     relief=SOLID)
        self.InfoPowerPlantEntry = Entry(FrameBottom, font=("Helvetica", 10))
        InfoPowerPlantTuple = (InfoPowerPlantLabel, self.InfoPowerPlantEntry)

        InfoTupleList = [InfoGenerationTuple, InfoPoolTuple, InfoMutationTuple, InfoPowerPlantTuple]

        ColumnCounter = 0
        for Tuple in InfoTupleList:
            RowCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=W + E + N + S)
                RowCounter = RowCounter + 1
            ColumnCounter = ColumnCounter + 1

    def runSimulation(self):
        if self.running == 1:
            self.p1.kill()
            self.running = 0
            self.pbar.stop()
            self.RunButton.config(text="Run")
            self.counterCheck = 0
            if len(self.gens) > 1:
                self.nextButton.config(state="normal")

            return
        else:
            try:
                GenInfo = int(self.InfoGenerationEntry.get())
                PoolInfo = int(self.InfoPoolEntry.get())
                MutationInfo = int(self.InfoMutationEntry.get())
                PowerPlantInfo = int(self.InfoPowerPlantEntry.get())
                infoArray = [GenInfo, PoolInfo, MutationInfo, PowerPlantInfo]

            except ValueError:
                fn.ShowErrorBox("Invoerfout", "Controller of de getallen goed zijn ingevoerd")
                return

            if PoolInfo < 10:
                fn.ShowErrorBox("Waarschuwing", "Voor een optimaal resultaat wordt het aangeraden om een Pool die groter is dan 10 mee te geven")
                return

            if GenInfo < 5:
                fn.ShowErrorBox("Waarschuwing", "Voor een optimaal resultaat wordt het aangeraden om voor meer dan 10 generaties te draaien")
                return

            if MutationInfo > 100 or MutationInfo < 0:
                fn.ShowErrorBox("Waarschuwing", "Het mutatie percentage moet tussen de 0 en de 100 liggen. Het wordt aangeraden om het het boven de 25% te houden.")
                return

            fn.clearGraph(self, True)
            self.counter = Value('i', 0)
            self.manager = Manager()
            self.Directory = self.manager.Value(c_char_p, "test")
            self.p1 = Process(target=runTrain, args=(self.counter, self.Directory, infoArray))
            self.p1.start()
            self.pbar.start(DELAY1)
            self.running = 1
            self.RunButton.config(text="Stop Simulatie")
            self.after(DELAY2, self.onGetValue)
            return

    def onGetValue(self):
        if self.p1.is_alive():
            print("Checking")
            print("Counter: " + str(self.counter.value))
            if self.counter.value != self.counterCheck:
                self.counterCheck = self.counter.value
                fn.updateGraph(self.Directory.value, self.counterCheck, self)
            self.after(DELAY2, self.onGetValue)
            return
        else:
            print("Klaar")
            self.pbar.stop()

def runTrain(counter, directory, array):
    train(array[0], array[1], 0, 10000000, 0, 90, 0, 359, model_name=None, load=False, counter=counter,
          directory=directory, mutationPercentage=array[2], target_kw=array[3])

def main():
    root = Tk()
    app = Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()

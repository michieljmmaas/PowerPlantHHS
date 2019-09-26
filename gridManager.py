from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import csv
import matplotlib.ticker as ticker


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Grid Manager")

        Frame1 = Frame(master, bg="red")
        Frame1.grid(row=0, column=0, rowspan=5, columnspan=4, sticky=W + E + N + S)
        ItemFrame = Frame(master, bg="green")
        ItemFrame.grid(row=0, column=4, rowspan=6, columnspan=2, sticky=W + E + N + S)
        FrameBottom = Frame(master, bg="blue")
        FrameBottom.grid(row=5, column=0, columnspan=4, rowspan=2, sticky=W + E + N + S)

        self.f = Figure(figsize=(5, 5), dpi=100)

        self.a = self.f.add_subplot(111)

        self.gens = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                     '18',
                     '19', '20', '21']
        # gens = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21];
        self.minCost = [1380645658.15, 617306363.53, 617306363.53, 469239361.71, 387622002.09, 365128241.34,
                        339966956.2,
                        309698761.48, 299455088.99, 245330372.63, 195903759.14, 175981177.33, 165490209.14,
                        153228772.75,
                        143520525.91, 143520525.91, 143387063.52, 122981391.73, 122169797.53, 112646841.61,
                        103483553.47,
                        93272310.59]
        self.meanCost = [8355564463.45, 5718371715.88, 3785891878.45, 3714357126.25, 3906800065.12, 3612190931.48,
                         2791057630.57, 3705114859.47, 3172927935.13, 3343982297.42, 2962651477.14, 3055757633.03,
                         2652876157.8, 35474765696.12, 61564067417.33, 136305909177.47, 73743742623.81, 173286460864.29,
                         52274403390.2, 107164182267.39, 114232925026.51, 3450067013.72]

        # gens, minCost, meanCost = loadLoggingFile()

        self.a.plot(self.gens, self.minCost, color='blue', label="Minimum Cost")
        # a.plot(gens, meanCost, color='red', label="Mean Cost")

        scale_y = 1e6
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
        self.a.yaxis.set_major_formatter(ticks_y)
        # a.set_yscale('log')

        self.a.set_ylim(0, max(self.minCost) * 1.1)

        self.a.set_xlim(self.gens[0], self.gens[20])

        self.a.legend()
        self.canvas = FigureCanvasTkAgg(self.f, Frame1)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH)

        nextButton = Button(Frame1, text="text", command=lambda: nextChart(self))
        nextButton.pack()

        padx = 10
        pady = 10
        LabelWidth = 20
        LabelHeight = 2

        LoadButton = Button(ItemFrame, text="Load", width=LabelWidth, height=LabelHeight,
                            command=lambda: loadCsvFile(SolarTupleList))
        RunButton = Button(ItemFrame, text="Run", width=LabelWidth, height=LabelHeight,
                           command=lambda: loadLoggingFile())
        NextButton = Button(ItemFrame, text="Next", width=LabelWidth, height=LabelHeight)
        ExportButton = Button(ItemFrame, text="Export", width=LabelWidth, height=LabelHeight)
        ActionTuple = (LoadButton, RunButton, NextButton, ExportButton)

        ItemLabel = Label(ItemFrame, text="Item", width=LabelWidth, height=LabelHeight, relief=SOLID)
        NumberLabel = Label(ItemFrame, text="Number", width=LabelWidth, height=LabelHeight, relief=SOLID)
        FactorLabel = Label(ItemFrame, text="Factor", width=LabelWidth, height=LabelHeight, relief=SOLID)
        CostLabel = Label(ItemFrame, text="Cost", width=LabelWidth, height=LabelHeight, relief=SOLID)
        headerTuple = (ItemLabel, NumberLabel, FactorLabel, CostLabel)

        PWSurplusLabel = Label(ItemFrame, text="Energy Surplus", width=LabelWidth, height=LabelHeight, anchor=W,
                               relief=SOLID)
        PWSurplusEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                               bg="white")
        PWSurplusFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                bg="white")
        PWDSurplusCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                               bg="white")
        PWDSurplusTuple = (PWSurplusLabel, PWSurplusEntry, PWSurplusFactor, PWDSurplusCost)

        PWDeficitLabel = Label(ItemFrame, text="Energy Deficit", width=LabelWidth, height=LabelHeight, anchor=W,
                               relief=SOLID)
        PWDeficitEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                               bg="white")
        PWDeficitFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                bg="white")
        PWDeficitCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                              bg="white")
        PWDeficitTuple = (PWDeficitLabel, PWDeficitEntry, PWDeficitFactor, PWDeficitCost)

        WTHeightLabel = Label(ItemFrame, text="Wind Turbine - Heigth", width=LabelWidth, height=LabelHeight, anchor=W,
                              relief=SOLID)
        WTHeightEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                              bg="white")
        WTHeightFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                               bg="white")
        WTHeightCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                             bg="white")
        WTHeightTuple = (WTHeightLabel, WTHeightEntry, WTHeightFactor, WTHeightCost)

        LabelTupleList = [ActionTuple, headerTuple, PWDSurplusTuple, PWDeficitTuple, WTHeightTuple]
        RowCounter = 0
        for Tuple in LabelTupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N + S)
                ColumnCounter = ColumnCounter + 1
            RowCounter = RowCounter + 1

        # Solar Panels info
        SPNameLabel = Label(ItemFrame, text="Solar Panel Number", width=LabelWidth, height=LabelHeight, anchor=W,
                            relief=SOLID)
        SPSurfaceLabel = Label(ItemFrame, text="Surface", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        SPAngleLabel = Label(ItemFrame, text="Hoek in graden", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SPOrientationLabel = Label(ItemFrame, text="Orientatie in graden", width=LabelWidth, height=LabelHeight,
                                   anchor=W, relief=SOLID)
        SPHeaderTuple = (SPNameLabel, SPSurfaceLabel, SPAngleLabel, SPOrientationLabel)

        # Solar Panel 1
        SP1NameLabel = Label(ItemFrame, text="Solar Panel 1", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SP1SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP1AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP1OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        SP1HeaderTuple = (SP1NameLabel, SP1SurfaceLabel, SP1AngleLabel, SP1OrientationLabel)

        # Solar Panel 2
        SP2NameLabel = Label(ItemFrame, text="Solar Panel 2", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SP2SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP2AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP2OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        SP2HeaderTuple = (SP2NameLabel, SP2SurfaceLabel, SP2AngleLabel, SP2OrientationLabel)

        # Solar Panel 3
        SP3NameLabel = Label(ItemFrame, text="Solar Panel 3", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SP3SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP3AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP3OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        SP3HeaderTuple = (SP3NameLabel, SP3SurfaceLabel, SP3AngleLabel, SP3OrientationLabel)

        # Solar Panel 4
        SP4NameLabel = Label(ItemFrame, text="Solar Panel 4", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SP4SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP4AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP4OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        SP4HeaderTuple = (SP4NameLabel, SP4SurfaceLabel, SP4AngleLabel, SP4OrientationLabel)

        SolarTupleList = [SPHeaderTuple, SP1HeaderTuple, SP2HeaderTuple, SP3HeaderTuple, SP4HeaderTuple]

        for Tuple in SolarTupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N + S)
                ColumnCounter = ColumnCounter + 1
            RowCounter = RowCounter + 1

        TotalLabel = Label(ItemFrame, text="Total Cost", height=5)
        TotalLabel.grid(row=RowCounter + 2, column=0, padx=padx, pady=pady, columnspan=3, sticky=W + E)

        TotalCost = Label(ItemFrame, text="", width=20, height=5)
        TotalCost.grid(row=RowCounter + 2, column=3, padx=padx, pady=pady, sticky=E)

        # Bottom info
        InfoGenerationLabel = Button(FrameBottom, text="Generations", width=LabelWidth, height=LabelHeight,
                                     relief=SOLID, command=lambda: fillBox(InfoGenerationEntry))
        InfoGenerationEntry = Label(FrameBottom, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        InfoGenerationTuple = (InfoGenerationLabel, InfoGenerationEntry)

        InfoPoolLabel = Button(FrameBottom, text="Pool", width=LabelWidth, height=LabelHeight, relief=SOLID,
                               command=lambda: fillBox(InfoPoolEntry))
        InfoPoolEntry = Label(FrameBottom, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        InfoPoolTuple = (InfoPoolLabel, InfoPoolEntry)

        InfoMutationLabel = Button(FrameBottom, text="MutationRate", width=LabelWidth, height=LabelHeight, relief=SOLID,
                                   command=lambda: fillBox(InfoMutationEntry))
        InfoMutationEntry = Label(FrameBottom, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                  bg="white")
        InfoMutationTuple = (InfoMutationLabel, InfoMutationEntry)

        InfoPowerPlantLabel = Button(FrameBottom, text="PowerPlant Energy", width=LabelWidth, height=LabelHeight,
                                     relief=SOLID, command=lambda: fillBox(InfoPowerPlantEntry))
        InfoPowerPlantEntry = Label(FrameBottom, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    bg="white")
        InfoPowerPlantTuple = (InfoPowerPlantLabel, InfoPowerPlantEntry)

        InfoTupleList = [InfoGenerationTuple, InfoPoolTuple, InfoMutationTuple, InfoPowerPlantTuple]

        ColumnCounter = 0
        for Tuple in InfoTupleList:
            RowCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=W + E + N + S)
                RowCounter = RowCounter + 1
            ColumnCounter = ColumnCounter + 1


# Misschien hier panda's toevoegen met cvs
def loadCsvFile(SolarTupleList):
    try:
        filename = askopenfilename()
        with open(filename, newline='') as csvfile:
            dataList = list(csv.reader(csvfile))
            data = dataList[0]
            counter = 0

            iterSolar = iter(SolarTupleList)
            next(iterSolar)
            for tupleItem in iterSolar:
                iterTuple = iter(tupleItem)
                next(iterTuple)
                for item in iterTuple:
                    info = round(float(data[counter]), 2)
                    item.config(text=info)
                    counter += 1
    except:
        ShowErrorBox("Foutmelding verkeerd bestand",
                     "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")


def loadLoggingFile():
    try:
        filename = askopenfilename()
        f = open(filename, "r")
        f1 = f.readlines()
        genArray = []
        meanCostArray = []
        minCostArray = []

        for x in f1:
            info = x.split(" ")
            info[5] = info[5].replace('\n', '')
            genArray.append(str(info[1]))
            meanCostArray.append(round(float(info[3]), 2))
            minCostArray.append(round(float(info[5]), 2))

        return genArray, minCostArray, meanCostArray

    except Exception as e:
        print(e)
        ShowErrorBox("Foutmelding verkeerd bestand",
                     "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")


def fillBox(box):
    d = MyDialog(root)
    root.wait_window(d.top)
    box.config(text=d.value)


def ShowErrorBox(title, message):
    messagebox.showerror(title, message)


def nextChart(self):
    self.a.clear()
    b = self.f.add_subplot(111)
    b.plot(self.gens, self.meanCost, color='red')
    self.canvas.draw()


class MyDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        Label(top, text="Value").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        try:
            self.value = int(self.e.get())
            self.top.destroy()
        except ValueError:
            ShowErrorBox("Foute Invoer", "Dit veld verwacht een geheel getal")
            self.value = int(0)
            self.top.destroy()


root = Tk()
app = Application(master=root)
app.mainloop()

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import csv


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

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, Frame1)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH)

        padx = 10
        pady = 10
        LabelWidth = 20
        LabelHeight = 2

        LoadButton = Button(ItemFrame, text="Load", width=LabelWidth, height=LabelHeight,
                            command=lambda: loadCsvFile(SolarTupleList))
        RunButton = Button(ItemFrame, text="Run", width=LabelWidth, height=LabelHeight)
        NextButton = Button(ItemFrame, text="Next", width=LabelWidth, height=LabelHeight)
        ExportButton = Button(ItemFrame, text="Export", width=LabelWidth, height=LabelHeight)
        ActionTuple = (LoadButton, RunButton, NextButton, ExportButton)

        ItemLabel = Label(ItemFrame, text="Item", width=LabelWidth, height=LabelHeight, relief=SOLID)
        NumberLabel = Label(ItemFrame, text="Number", width=LabelWidth, height=LabelHeight, relief=SOLID)
        FactorLabel = Label(ItemFrame, text="Factor", width=LabelWidth, height=LabelHeight, relief=SOLID)
        CostLabel = Label(ItemFrame, text="Cost", width=LabelWidth, height=LabelHeight, relief=SOLID)
        headerTuple = (ItemLabel, NumberLabel, FactorLabel, CostLabel)

        PWSurplusLabel = Label(ItemFrame, text="Energy Surplus", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        PWSurplusEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        PWSurplusFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        PWDSurplusCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        PWDSurplusTuple = (PWSurplusLabel, PWSurplusEntry, PWSurplusFactor, PWDSurplusCost)

        PWDeficitLabel = Label(ItemFrame, text="Energy Deficit", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        PWDeficitEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        PWDeficitFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        PWDeficitCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        PWDeficitTuple = (PWDeficitLabel, PWDeficitEntry, PWDeficitFactor, PWDeficitCost)

        WTHeightLabel = Label(ItemFrame, text="Wind Turbine - Heigth", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        WTHeightEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        WTHeightFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        WTHeightCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
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
        SPNameLabel = Label(ItemFrame, text="Solar Panel Number", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        SPSurfaceLabel = Label(ItemFrame, text="Surface", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        SPAngleLabel = Label(ItemFrame, text="Hoek in graden", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        SPOrientationLabel = Label(ItemFrame, text="Orientatie in graden", width=LabelWidth, height=LabelHeight,
                                   anchor=W, relief=SOLID)
        SPHeaderTuple = (SPNameLabel, SPSurfaceLabel, SPAngleLabel, SPOrientationLabel)

        # Solar Panel 1
        SP1NameLabel = Label(ItemFrame, text="Solar Panel 1", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        SP1SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP1AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP1OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP1HeaderTuple = (SP1NameLabel, SP1SurfaceLabel, SP1AngleLabel, SP1OrientationLabel)

        # Solar Panel 2
        SP2NameLabel = Label(ItemFrame, text="Solar Panel 2", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        SP2SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP2AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP2OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP2HeaderTuple = (SP2NameLabel, SP2SurfaceLabel, SP2AngleLabel, SP2OrientationLabel)

        # Solar Panel 3
        SP3NameLabel = Label(ItemFrame, text="Solar Panel 3", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        SP3SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP3AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP3OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP3HeaderTuple = (SP3NameLabel, SP3SurfaceLabel, SP3AngleLabel, SP3OrientationLabel)

        # Solar Panel 4
        SP4NameLabel = Label(ItemFrame, text="Solar Panel 4", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        SP4SurfaceLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP4AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
        SP4OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
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
        InfoGenerationLabel = Label(FrameBottom, text="Generations", width=LabelWidth, height=LabelHeight, relief=SOLID)
        InfoGenerationEntry = Label(FrameBottom, width=LabelWidth, height=LabelHeight, command=lambda: loadCsvFile(SolarTupleList))
        InfoGenerationTuple = (InfoGenerationLabel, InfoGenerationEntry)

        InfoPoolLabel = Label(FrameBottom, text="Pool", width=LabelWidth, height=LabelHeight, relief=SOLID)
        InfoPoolEntry = Text(FrameBottom, width=LabelWidth, height=LabelHeight)
        InfoPoolTuple = (InfoPoolLabel, InfoPoolEntry)

        InfoMutationLabel = Label(FrameBottom, text="MutationRate", width=LabelWidth, height=LabelHeight, relief=SOLID)
        InfoMutationEntry = Text(FrameBottom, width=LabelWidth, height=LabelHeight)
        InfoMutationTuple = (InfoMutationLabel, InfoMutationEntry)

        InfoPowerPlantLabel = Label(FrameBottom, text="PowerPlant Energy", width=LabelWidth, height=LabelHeight, relief=SOLID)
        InfoPowerPlantEntry = Text(FrameBottom, width=LabelWidth, height=LabelHeight)
        InfoPowerPlantTuple = (InfoPowerPlantLabel, InfoPowerPlantEntry)

        InfoTupleList = [InfoGenerationTuple, InfoPoolTuple, InfoMutationTuple, InfoPowerPlantTuple]

        ColumnCounter = 0
        for Tuple in InfoTupleList:
            RowCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=W + E + N + S)
                RowCounter = RowCounter + 1
            ColumnCounter = ColumnCounter + 1


def EditHyperParameters(box):
    if messagebox.askyesno("Bewerken Hyper Parameter", "Pas op! Wilt u deze hyper paramter aanpassen?"):
        print(box)
    else:
        return

def ShowErrorBox(title, message):
    messagebox.showerror(title, message)

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

root = Tk()
app = Application(master=root)
app.mainloop()

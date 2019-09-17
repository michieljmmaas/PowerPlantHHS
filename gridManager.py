import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Grid Manager")

        Frame1 = Frame(master, bg="red")
        Frame1.grid(row = 0, column = 0, rowspan = 4, columnspan = 4, sticky = W+E+N+S)
        ItemFrame = Frame(master, bg="green")
        ItemFrame.grid(row = 0, column = 4, rowspan = 6, columnspan = 2, sticky = W+E+N+S)
        FrameBottom = Frame(master, bg="blue")
        FrameBottom.grid(row=4, column=0, columnspan=4, rowspan=2, sticky= W+E+N+S)


        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, Frame1)
        canvas.draw()
        canvas.get_tk_widget().pack()

        padx = 10
        pady = 10
        LabelWidth = 20
        LabelHeight = 2

        RunButton = Button(ItemFrame, text="Run", width=LabelWidth, height=LabelHeight)
        NextButton  = Button(ItemFrame, text="Next", width=LabelWidth, height=LabelHeight)
        ExportButton = Button(ItemFrame, text="Export", width=LabelWidth, height=LabelHeight)

        RunButton.grid(row=0, column=0, padx=padx, pady=pady)
        NextButton.grid(row=0, column=1, padx=padx, pady=pady)
        ExportButton.grid(row=0, column=2, padx=padx, pady=pady)

        ItemLabel = Label(ItemFrame, text="Item", width=LabelWidth, height=LabelHeight)
        NumberLabel = Label(ItemFrame, text="Number", width=LabelWidth, height=LabelHeight)
        CostLabel = Label(ItemFrame, text="Cost", width=LabelWidth, height=LabelHeight)

        ItemLabel.grid(row=1, column=0, padx=padx, pady=pady)
        NumberLabel.grid(row=1, column=1, padx=padx, pady=pady)
        CostLabel.grid(row=1, column=2, padx=padx, pady=pady)

        PWSurplusLabel = Label(ItemFrame, text="Energy Surplus", width=LabelWidth, height=LabelHeight, anchor=W)
        PWSurplusEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        PWDSurplusCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        PWDSurplusTuple = (PWSurplusLabel, PWSurplusEntry, PWDSurplusCost)

        PWDeficitLabel = Label(ItemFrame, text="Energy Deficit", width=LabelWidth, height=LabelHeight, anchor=W)
        PWDeficitEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        PWDeficitCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        PWDeficitTuple = (PWDeficitLabel, PWDeficitEntry, PWDeficitCost)

        WTHeightLabel = Label(ItemFrame, text="Wind Turbine - Heigth", width=LabelWidth, height=LabelHeight, anchor=W)
        WTHeightEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        WTHeightCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        WTHeightTuple = (WTHeightLabel, WTHeightEntry, WTHeightCost)

        LabelTupleList = [PWDSurplusTuple, PWDeficitTuple, WTHeightTuple]
        RowCounter = 2
        for Tuple in LabelTupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N+S)
                ColumnCounter = ColumnCounter +1
            RowCounter = RowCounter + 1

        ###Solar Panels
        #Solar Panels info
        SPNameLabel = Label(ItemFrame, text="Solar Panel Number", width=LabelWidth, height=LabelHeight, anchor=W)
        SPAngleLabel = Label(ItemFrame, text="Agnle in Graden", width=LabelWidth, height=LabelHeight, anchor=W)
        SPOrientationLabel = Label(ItemFrame, text="Orentatie in Graden", width=LabelWidth, height=LabelHeight, anchor=W)
        SPCostLabel = Label(ItemFrame, text="Cost", width=LabelWidth, height=LabelHeight, anchor=W)
        SPHeaderTuple = (SPNameLabel, SPAngleLabel, SPOrientationLabel, SPCostLabel)

        #Solar Panel 1
        SP1NameLabel = Label(ItemFrame, text="Solar Panel 1", width=LabelWidth, height=LabelHeight, anchor=W)
        SP1AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP1OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP1CostLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP1HeaderTuple = (SP1NameLabel, SP1AngleLabel, SP1OrientationLabel, SP1CostLabel)

        #Solar Panel 2
        SP2NameLabel = Label(ItemFrame, text="Solar Panel 2", width=LabelWidth, height=LabelHeight, anchor=W)
        SP2AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP2OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP2CostLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP2HeaderTuple = (SP2NameLabel, SP2AngleLabel, SP2OrientationLabel, SP2CostLabel)

        #Solar Panel 3
        SP3NameLabel = Label(ItemFrame, text="Solar Panel 3", width=LabelWidth, height=LabelHeight, anchor=W)
        SP3AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP3OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP3CostLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP3HeaderTuple = (SP3NameLabel, SP3AngleLabel, SP3OrientationLabel, SP3CostLabel)

        #Solar Panel 4
        SP4NameLabel = Label(ItemFrame, text="Solar Panel 4", width=LabelWidth, height=LabelHeight, anchor=W)
        SP4AngleLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP4OrientationLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP4CostLabel = Label(ItemFrame, width=LabelWidth, height=LabelHeight, anchor=W)
        SP4HeaderTuple = (SP4NameLabel, SP4AngleLabel, SP4OrientationLabel, SP4CostLabel)

        SolarTupleList = [SPHeaderTuple, SP1HeaderTuple, SP2HeaderTuple, SP3HeaderTuple, SP4HeaderTuple]

        for Tuple in SolarTupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=N+S)
                ColumnCounter = ColumnCounter +1
            RowCounter = RowCounter + 1


        totalwidth = LabelWidth + LabelWidth + (padx/2)

        TotalLabel = Label(ItemFrame, text="Total Cost", height=5)
        TotalLabel.grid(row=RowCounter+2, column=0, padx=padx, pady=pady, columnspan=2, sticky=W+E)

        TotalCost = Label(ItemFrame, text="", width=20, height=5)
        TotalCost.grid(row=RowCounter + 2, column=2, padx=padx, pady=pady, sticky=E)

        #Bottom info

        InfoGenerationLabel = Label(FrameBottom, text="Generations", width=LabelWidth, height=LabelHeight)
        InfoGenerationEntry = Text(FrameBottom, width=LabelWidth, height=LabelHeight)
        InfoGenerationTuple = (InfoGenerationLabel, InfoGenerationEntry)

        InfoPoolLabel = Label(FrameBottom, text="Pool", width=LabelWidth, height=LabelHeight)
        InfoPoolEntry = Text(FrameBottom, width=LabelWidth, height=LabelHeight)
        InfoPoolTuple = (InfoPoolLabel, InfoPoolEntry)

        InfoMutationLabel = Label(FrameBottom, text="MutationRate", width=LabelWidth, height=LabelHeight)
        InfoMutationEntry = Text(FrameBottom, width=LabelWidth, height=LabelHeight)
        InfoMutationTuple = (InfoMutationLabel, InfoMutationEntry)

        InfoPowerPlantLabel = Label(FrameBottom, text="PowerPlant Energy", width=LabelWidth, height=LabelHeight)
        InfoPowerPlantEntry = Text(FrameBottom, width=LabelWidth, height=LabelHeight)
        InfoPowerPlantTuple = (InfoPowerPlantLabel, InfoPowerPlantEntry)

        InfoTupleList = [InfoGenerationTuple, InfoPoolTuple, InfoMutationTuple, InfoPowerPlantTuple]

        ColumnCounter = 0
        for Tuple in InfoTupleList:
            RowCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady, sticky=W+E+N+S)
                RowCounter = RowCounter + 1
            ColumnCounter = ColumnCounter + 1


def doNothing():
    print("doNothing")


root = Tk()

ToolBar = Menu(root)
root.config(menu=ToolBar)
subMenu = Menu(ToolBar)
ToolBar.add_cascade(label="Options", menu=subMenu)
subMenu.add_command(label="Load", command=doNothing)


app = Application(master=root)
app.mainloop()

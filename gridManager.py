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

        PWDeficitLabel = Label(ItemFrame, text="Energy Deficit", width=LabelWidth, height=LabelHeight, anchor=W)
        PWDeficitEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        PWDeficitCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        PWDeficitTuple = (PWDeficitLabel, PWDeficitEntry, PWDeficitCost)

        SPSurfaceAreaLabel = Label(ItemFrame, text="Solar Panel - Surface Area", width=LabelWidth, height=LabelHeight, anchor=W)
        SPSurfaceAreaEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        SPSurfaceAreaCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        SPSurfaceAreaTuple = (SPSurfaceAreaLabel, SPSurfaceAreaEntry, SPSurfaceAreaCost)

        SPAngleLabel = Label(ItemFrame, text="Solar Panel - Angle", width=LabelWidth, height=LabelHeight, anchor=W)
        SPAngleEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        SPAngleLCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        SPAngleTuple = (SPAngleLabel, SPAngleEntry, SPAngleLCost)

        SPOrientationLabel = Label(ItemFrame, text="Solar Panel - Orientation", width=LabelWidth, height=LabelHeight, anchor=W)
        SPOrientationEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        SPOrientationCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        SPOrientationTuple = (SPOrientationLabel, SPOrientationEntry, SPOrientationCost)

        WTHeightLabel = Label(ItemFrame, text="Wind Turbine - Heigth", width=LabelWidth, height=LabelHeight, anchor=W)
        WTHeightEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        WTHeightCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W)
        WTHeightTuple = (WTHeightLabel, WTHeightEntry, WTHeightCost)

        LabelTupleList = [PWDeficitTuple, SPSurfaceAreaTuple, SPAngleTuple, SPOrientationTuple, WTHeightTuple]

        RowCounter = 2
        for Tuple in LabelTupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady)
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


root = Tk()
app = Application(master=root)
app.mainloop()

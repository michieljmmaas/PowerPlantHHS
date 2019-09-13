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
        Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        ItemFrame = Frame(master, bg="green")
        ItemFrame.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)

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

        TupleList = [PWDeficitTuple, SPSurfaceAreaTuple, SPAngleTuple, SPOrientationTuple, WTHeightTuple]

        RowCounter = 2
        for Tuple in TupleList:
            ColumnCounter = 0
            for Item in Tuple:
                Item.grid(row=RowCounter, column=ColumnCounter, padx=padx, pady=pady)
                ColumnCounter = ColumnCounter +1
            RowCounter = RowCounter + 1

root = Tk()
app = Application(master=root)
app.mainloop()

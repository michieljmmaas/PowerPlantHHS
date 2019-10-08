from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import numpy as np
import csv
import matplotlib.ticker as ticker
import sys
from math import ceil, log
from train import train
import threading
import logging
import time


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Grid Manager")

        print(sys.path);

        Frame1 = Frame(master, bg="red")
        Frame1.grid(row=0, column=0, rowspan=5, columnspan=4, sticky=W + E + N + S)
        ItemFrame = Frame(master, bg="green")
        ItemFrame.grid(row=0, column=4, rowspan=6, columnspan=2, sticky=W + E + N + S)
        FrameBottom = Frame(master, bg="blue")
        FrameBottom.grid(row=5, column=0, columnspan=4, rowspan=2, sticky=W + E + N + S)

        self.graphNumber = 0

        self.f = Figure(figsize=(5, 5), dpi=100)

        self.a = self.f.add_subplot(111)

        self.gens = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.minCost = [1380645658.15, 617306363.53, 617306363.53, 469239361.71, 387622002.09, 365128241.34,
                        339966956.2, 309698761.48, 299455088.99, 245330372.63, 195903759.14]

        self.meanCost = [4611297453.12, 4296382782.98, 3945328950.50, 3400852428.68, 2928522993.03, 2441527183.68,
                         5259124454.19, 2685947243.92, 2258377078.39, 1750162255.54, 1800532731.67]

        # self.gens, self.minCost, self.meanCost = loadLoggingFile()

        self.canvas = FigureCanvasTkAgg(self.f, Frame1)
        nextChart(self)
        self.canvas.get_tk_widget().pack(fill=BOTH)

        nextButton = Button(Frame1, text="Volgende Grafiek", command=lambda: nextChart(self))
        nextButton.pack()

        padx = 10
        pady = 10
        LabelWidth = 20
        LabelHeight = 2

        LoadButton = Button(ItemFrame, text="Load", width=LabelWidth, height=LabelHeight,
                            command=lambda: loadCsvFile(SolarTupleList, WTHeightTuple))
        RunButton = Button(ItemFrame, text="Run", width=LabelWidth, height=LabelHeight,
                           command=lambda: loadLoggingFile())
        NextButton = Button(ItemFrame, text="Next", width=LabelWidth, height=LabelHeight, command=lambda: runSimulation(InfoGenerationEntry, InfoPoolEntry))
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

        WTNumberLabel = Label(ItemFrame, text="Wind Turbine - Aantal", width=LabelWidth, height=LabelHeight, anchor=W,
                              relief=SOLID)
        WTNumberEntry = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                              bg="white")
        WTNumberFactor = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                               bg="white")
        WTNumberCost = Label(ItemFrame, text="", width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                             bg="white")
        WTHeightTuple = (WTNumberLabel, WTNumberEntry, WTNumberFactor, WTNumberCost)

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
        SPSurfaceLabel = Label(ItemFrame, text="Surface (m\u00b2)", width=LabelWidth, height=LabelHeight, anchor=W, relief=SOLID)
        SPAngleLabel = Label(ItemFrame, text="Hoek in graden", width=LabelWidth, height=LabelHeight, anchor=W,
                             relief=SOLID)
        SPOrientationLabel = Label(ItemFrame, text="Orientatie t.o.v. Zuiden", width=LabelWidth, height=LabelHeight,
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
        # InfoGenerationEntry = Label(FrameBottom, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN,
                                    # bg="white")
        InfoGenerationEntry = Entry(FrameBottom, width=LabelWidth)
        InfoGenerationTuple = (InfoGenerationLabel, InfoGenerationEntry)

        InfoPoolLabel = Button(FrameBottom, text="Pool", width=LabelWidth, height=LabelHeight, relief=SOLID,
                               command=lambda: fillBox(InfoPoolEntry))
        InfoPoolEntry = Entry(FrameBottom, width=LabelWidth)
        # InfoPoolEntry = Label(FrameBottom, width=LabelWidth, height=LabelHeight, anchor=W, relief=SUNKEN, bg="white")
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
def loadCsvFile(SolarTupleList, WTHeightTuple):
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
            #
            # wm_cost, windTurbineTotalCost = defWindTurbineCost(int(4), int(data[-1]));
            #
            # entry = WTHeightTuple[1];
            # entry.config(text=data[-1]);
            #
            # cost = WTHeightTuple[2];
            # cost.config(text=wm_cost);
            #
            # total = WTHeightTuple[3];
            # total.config(text=windTurbineTotalCost);
    except Exception as e:
        print(e);
        ShowErrorBox("Foutmelding verkeerd bestand",
                     "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")


def runSimulation(GenerationEntry, GroupSizeEntry):
    generations = int(GenerationEntry.get())
    GroupSize = int(GroupSizeEntry.get());
    x = threading.Thread(target=callTrain(generations, GroupSize), args=(1,))
    logging.info("Main    : before running thread")
    x.start()


def callTrain(generations, GroupSize):
    train(generations, GroupSize, 0, 10000000, 0, 90, 0, 359, model_name=None, load=False)


def x_limit(array):
    a = len(array)
    if a > 21:
        a = 21
    return a - 1;


def ceil_power_of_10(n):
    exp = log(n, 10)
    exp = ceil(exp)
    return 10**exp


def defWindTurbineCost(wm_type, wm_number):
    if (wm_type == 2):
        wm_cost = 1605000
    elif (wm_type == 3):
        wm_cost = 5350000
    elif (wm_type == 1):
        wm_cost = 535000
    elif (wm_type == 4):
        wm_cost = 3210000
    else:
        wm_cost = 0

    return wm_cost, wm_cost * wm_number;


def loadLoggingFile():
    # try:
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
            mean = round(float(info[3]), 2);
            minCost = round(float(info[5]), 2);
            meanCostArray.append(mean);
            minCostArray.append(minCost)

        return genArray, minCostArray, meanCostArray

    # except Exception as e:
    #     print(e)
    #     ShowErrorBox("Foutmelding verkeerd bestand",
    #                  "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")


def fillBox(box):
    d = MyDialog(root)
    root.wait_window(d.top)
    box.config(text=d.value)

def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

def ShowErrorBox(title, message):
    messagebox.showerror(title, message)


def nextChart(self):
    self.a.clear()
    b = self.f.add_subplot(111)
    if self.graphNumber == 0:
        self.a.plot(self.gens, self.minCost, color='blue', label="Minimum Cost")

        scale_y = ceil_power_of_10(np.mean(self.minCost)/5);
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
        self.a.yaxis.set_major_formatter(ticks_y)
        self.a.set(ylabel="Bedrag in " + str(format_e(scale_y)), xlabel="Generatie", title="Minimum Cost")
        self.a.set_ylim(0, max(self.minCost) * 1.1)
        limit = x_limit(self.gens)
        self.a.set_xlim(self.gens[0], self.gens[limit])

        self.a.legend()
        self.graphNumber = 1

    elif self.graphNumber == 1:
        self.a.plot(self.gens, self.meanCost, color='red', label="Mean Cost")
        scale_y = ceil_power_of_10(np.mean(self.meanCost)/5);
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
        self.a.set(ylabel="Bedrag in " + str(format_e(scale_y)), xlabel="Generatie", title="Mean Cost")
        self.a.yaxis.set_major_formatter(ticks_y)
        self.a.set_ylim(0, max(self.meanCost) * 1.1)
        limit = x_limit(self.gens)
        self.a.set_xlim(self.gens[0], self.gens[limit])
        self.a.legend()
        self.graphNumber = 0

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


class Worker(threading.Thread):
    def run(self):
        # long process goes here
        time.sleep(10)

w = Worker()
w.start()
ShowErrorBox("Work Started", "OK started working")
root.update()
w.join()
ShowErrorBox("Work Complete", "OK Done")
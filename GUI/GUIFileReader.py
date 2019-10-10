from tkinter.filedialog import askopenfilename
import csv

# class GUIFileReader:
    # def __init__(self):
    #     self.name = "kaas"

def loadLoggingFile(GUI, filename=None):
    try:
        if filename is None:
            filename = askopenfilename()
        print("Filename: " + filename)
        if (filename != ''):
            f = open(filename, "r")
            f1 = f.readlines()
            genArray = []
            meanCostArray = []
            minCostArray = []

            for x in f1:
                info = x.split(" ")
                info[5] = info[5].replace('\n', '')
                genArray.append(str(info[1]))
                mean = round(float(info[3]), 2)
                minCost = round(float(info[5]), 2)
                meanCostArray.append(mean)
                minCostArray.append(minCost)

            GUI.gens = genArray
            GUI.meanCost = meanCostArray
            GUI.minCost = minCostArray
            GUI.functions.nextChart(GUI)

    except Exception as e:
        print(e)
        GUI.ShowErrorBox("Foutmelding verkeerd bestand",
                          "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")

# Misschien hier panda's toevoegen met cvs
def loadCsvFile(GUI, filename=None):
    try:
        if filename is None:
            filename = askopenfilename()
        if (filename != ''):
            with open(filename, newline='') as csvfile:
                dataList = list(csv.reader(csvfile))
                data = dataList[0]
                counter = 0

                iterSolar = iter(GUI.SolarTupleList)
                next(iterSolar)
                for tupleItem in iterSolar:
                    iterTuple = iter(tupleItem)
                    next(iterTuple)
                    for item in iterTuple:
                        info = round(float(data[counter]), 2)
                        item.config(text=info)
                        counter += 1
                #
                # wm_cost, windTurbineTotalCost = defWindTurbineCost(int(4), int(data[-1]))
                #
                # entry = WTHeightTuple[1]
                # entry.config(text=data[-1])
                #
                # cost = WTHeightTuple[2]
                # cost.config(text=wm_cost)
                #
                # total = WTHeightTuple[3]
                # total.config(text=windTurbineTotalCost)
    except Exception as e:
        print(e)
        GUI.functions.ShowErrorBox("Foutmelding verkeerd bestand",
                     "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")
from tkinter.filedialog import askopenfilename
import csv
import GUI.GUIFunctions as fn
import babel.numbers as bb


def loadLoggingFile(GUI, first, filename=None):
    try:
        if filename is None:
            filename = askopenfilename()
        print("Filename: " + filename)
        if filename != '':
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

            totalCostNumber = bb.format_currency(minCostArray[-1], 'EUR', locale='en_US')
            GUI.TotalCost.config(text=totalCostNumber)
            if not first:
                fn.nextChart(GUI)
                GUI.nextButton.config(state="normal")

    except Exception as e:
        print(e)
        fn.ShowErrorBox("Foutmelding verkeerd bestand",
                          "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")


# Misschien hier panda's toevoegen met cvs
def loadCsvFile(GUI, filename=None):
    try:
        if filename is None:
            filename = askopenfilename()
        if filename != '':
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

                windData = round(float(data[-1]))
                wm_cost, windTurbineTotalCost = fn.defWindTurbineCost(int(4), windData)

                entry = GUI.WTHeightTuple[1]
                entry.config(text=windData)

                cost = GUI.WTHeightTuple[2]
                cost.config(text=wm_cost)

                total = GUI.WTHeightTuple[3]
                total.config(text=windTurbineTotalCost)
    except Exception as e:
        print(e)
        fn.ShowErrorBox("Foutmelding verkeerd bestand",
                     "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")
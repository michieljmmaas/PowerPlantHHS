from tkinter.filedialog import askopenfilename
import csv
import GUI.GUIFunctions as fn
import babel.numbers as bb

# Dit bestand geeft functies voor het inlezen van de bestanden en invullen van de velden
textPreSpace = "  "

# Dit bestand laad het loggin bestand in
def loadLoggingFile(GUI, first=None, filename=None):
    print("kaas")
    try:
        if filename is None:
            filename = askopenfilename() #Dit gebeurd als je de knop indrukt, laat hij hem pakken
        if filename != '': # Zolang het een normaal bestand is
            f = open(filename, "r")
            f1 = f.readlines() # Lees het bestand
            genArray = []
            meanCostArray = []
            minCostArray = []

            for x in f1: #Voor elke regel in het bestand, vul de arrays aan
                info = x.split(" ")
                info[5] = info[5].replace('\n', '')
                gen = int(info[1]) + 1
                genArray.append(str(gen))
                mean = round(float(info[3]), 2)
                minCost = round(float(info[5]), 2)
                meanCostArray.append(mean)
                minCostArray.append(minCost)

            # Geef de arrays terug aan de UI
            GUI.gens = genArray
            GUI.meanCost = meanCostArray
            GUI.minCost = minCostArray

            #Geef total cost in euro
            totalCostNumber = bb.format_currency(minCostArray[-1], 'EUR', locale='en_US')
            GUI.TotalCost.config(text=textPreSpace + str(totalCostNumber))

            #Zolang er meer dan twee waarden zijn, laat hij je naar de volgende grafiek gaan
            if not first:
                fn.loadChart(GUI, False, GUI.fullGraph)
                GUI.nextButton.config(state="normal")
                GUI.previousButton.config(state="normal")
                GUI.chartButton.config(state="normal")

    except Exception as e:
        print(e)
        fn.ShowErrorBox("Foutmelding verkeerd bestand",
                          "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")


# Deze functie leest een CSV file in
def loadCsvFile(GUI, filename=None):
    print("kaas")
    try:
        if filename is None:
            filename = askopenfilename() # Als je direct op de knop drukt laat hij je kiezen
        if filename != '':
            with open(filename, newline='') as csvfile: # Lees het bestand in, in een array
                dataList = list(csv.reader(csvfile))
                data = dataList[0]
                counter = 0

                # Voor de zonnenpanelen moet wil je er doorheen loopen om het in te vullen
                iterSolar = iter(GUI.SolarTupleList)
                next(iterSolar)
                for tupleItem in iterSolar:
                    iterTuple = iter(tupleItem) #Sla de eerste over want dat is text
                    next(iterTuple)
                    for item in iterTuple: # Vul de waarden en
                        info = round(float(data[counter]), 2)
                        item.config(text=textPreSpace + str(info))
                        counter += 1

                #Gegevens voor de windturbines
                windData = round(float(data[-2]))
                wm_cost, windTurbineTotalCost = fn.defWindTurbineCost(int(4), windData)

                entry = GUI.WTHeightTuple[1]
                entry.config(text=textPreSpace + str(windData))

                cost = GUI.WTHeightTuple[2]
                cost.config(text=textPreSpace + str(wm_cost))

                total = GUI.WTHeightTuple[3]
                total.config(text=textPreSpace + str(windTurbineTotalCost))
    except Exception as e:
        print(e)
        fn.ShowErrorBox("Foutmelding verkeerd bestand",
                     "Dit bestand kan niet worden ingeladen. Kijk of een goed logging bestand is gekozen.")
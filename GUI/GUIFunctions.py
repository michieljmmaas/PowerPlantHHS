from math import ceil, log
from tkinter import messagebox
import GUI.GUIFileReader as fr

def x_limit(array):
    a = len(array)
    if a > 21:
        a = 21
    return a - 1

def ceil_power_of_10(n):
    exp = log(n, 10)
    exp = ceil(exp)
    return 10 ** exp

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

    return wm_cost, wm_cost * wm_number

def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

def ShowErrorBox(title, message):
    messagebox.showerror(title, message)

def nextChart(GUI, starting=True):
    GUI.a.clear()
    if starting:
        GUI.graphNumber = 0
    if GUI.graphNumber == 0:
        GUI.a.plot(GUI.gens, GUI.minCost, color='blue', label="Minimum Cost")

        GUI.a.set_yscale("log")
        GUI.a.set(ylabel="Bedrag in euro's (€)", xlabel="Generatie", title="Minimum Cost")
        limit = x_limit(GUI.gens)
        GUI.a.set_xlim(GUI.gens[0], GUI.gens[limit])

        GUI.a.legend()
        GUI.graphNumber = 1

    elif GUI.graphNumber == 1:
        GUI.a.plot(GUI.gens, GUI.meanCost, color='red', label="Mean Cost")
        GUI.a.set(ylabel="Bedrag in euro's (€)", xlabel="Generatie", title="Mean Cost")
        GUI.a.set_yscale("log")
        limit = x_limit(GUI.gens)
        GUI.a.set_xlim(GUI.gens[0], GUI.gens[limit])
        GUI.a.legend()
        GUI.graphNumber = 0

    GUI.canvas.draw()

def updateGraph(directory, gen, GUI):
    csvFileName = directory + "best_" + str(gen - 1) + ".csv"
    fr.loadCsvFile(GUI, csvFileName)
    loggingFileName = directory + "log.txt"
    fr.loadLoggingFile(GUI, loggingFileName)

def exitProgram(GUI):
    GUI.parent.destroy()
    GUI.p1.kill()

def fillEntries(GUI):
    GUI.InfoGenerationEntry.insert(0, '100')
    GUI.InfoPoolEntry.insert(0, '10')
    GUI.InfoMutationEntry.insert(0, '50')
    GUI.InfoPowerPlantEntry.insert(0, '6000')

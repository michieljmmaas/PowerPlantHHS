from train import train
import GUI.GUIFunctions as fn
import GUI.GUIFileReader as fr


DELAY1 = 20
DELAY2 = 5000

def runSimulation(self):
    if self.running == 1:
        self.p1.kill()
        self.running = 0
        self.pbar.stop()

        return
    else:
        infoArray = [100, 10]

        try:
            GenInfo = int(self.InfoGenerationEntry.get())
            PoolInfo = int(self.InfoPoolEntry.get())
            # MutationInfo = float(self.InfoMutationEntry.get())
            # PowerPlantInfo = int(self.InfoPowerPlantEntry.get())
            infoArray = [GenInfo, PoolInfo]
            # infoArray = [GenInfo, PoolInfo, MutationInfo, PowerPlantInfo]

        except ValueError:
            fn.ShowErrorBox("Invoerfout", "Controller of de getallen goed zijn ingevoerd")
            return

        self.counter = Value('i', 0)
        self.manager = Manager()
        self.Directory = self.manager.Value(c_char_p, "test")
        self.p1 = Process(target=runTrain, args=(self.counter, self.Directory, infoArray))
        self.p1.start()
        self.pbar.start(DELAY1)
        self.running = 1
        self.after(DELAY2, self.onGetValue)
        return

def onGetValue(self):
    if self.p1.is_alive():
        print("Checking")
        print("Counter: " + str(self.counter.value))
        if self.counter.value != self.counterCheck:
            self.counterCheck = self.counter.value
            print("DirectoryPath: " + self.Directory.value)
            fn.updateGraph(self.Directory.value, self.counterCheck, self)
        self.after(DELAY2, self.onGetValue)
        return
    else:
        print("Klaar")
        self.pbar.stop()

def runTrain(counter, directory, array):
    train(array[0], array[1], 0, 10000000, 0, 90, 0, 359, model_name=None, load=False, counter=counter,
          directory=directory)



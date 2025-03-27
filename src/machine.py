class Machine:
    def __init__(self, ID, OS, Disk, Cores):
        self.ID = ID
        self.OS = OS
        self.Disk = Disk
        self.Cores = Cores

    def InstanceToDict(self):
        return {"ID" : self.ID, "OS": self.OS, "Disk": self.Disk, "Cores": self.Cores}

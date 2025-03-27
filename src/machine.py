
class Machine:
    def __init__(self, ID, OS, Disk, Ram, Cores):
        self.ID = ID
        self.OS = OS
        self.Disk = Disk
        self.Ram = Ram
        self.Cores = Cores

    def InstanceToDict(self):
        return {
            "ID" : self.ID,
            "OS": self.OS,
            "Disk": self.Disk,
            "Ram" : self.Ram,
            "Cores": self.Cores}
    
# import logging

# class Machine:
#     def __init__(self, ID, OS, Disk, Cores):
#         self.ID = ID
#         self.OS = OS
#         self.Disk = Disk
#         self.Cores = Cores
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(logging.INFO)
#         self.logger.addHandler(logging.FileHandler('Logs/provisioning.log'))
    
#     def InstanceToDict(self):
#         return {"ID" : self.ID, "OS": self.OS, "Disk": self.Disk, "Cores": self.Cores}
    
#     def create(self):
#         machine_conf = self.InstanceToDict()
#         self.logger.info(f"Created machine: {self.ID}")
#         JsonWrite(machine_conf, MACHINES_CONF)
#         return machine_conf

# def CreateMachine():
#     ids, Os, Disk, Ram, Cores = GetParams()  
#     NewMachines = {}  # Dictionary to store instances
#     for id in ids: #Sets each id as an instance with the parsed params.
#         NewMachines[id] = Machine(id, Os, Disk, Ram, Cores)
#         machine_conf = NewMachines[id].create()
#         print(f"Created machine: {id}")
#     print(f"Created the new machines: {list(NewMachines.keys())}")

import logging

class Machine:
    # Create a class-level logger
    logger = logging.getLogger("MachineLogger")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('Logs/provisioning.log', mode='a')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s - %(name)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def __init__(self, ID, OS, Disk, Ram, Cores):
        self.ID = ID
        self.OS = OS
        self.Disk = Disk
        self.Ram = Ram
        self.Cores = Cores
        
        Machine.logger.info(f"Created a new machine: {self.ID}")

    def InstanceToDict(self):
        return {
            "ID" : self.ID,
            "OS": self.OS,
            "Disk": self.Disk,
            "Ram" : self.Ram,
            "Cores": self.Cores}
    

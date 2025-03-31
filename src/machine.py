import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='Logs/provisioning.log',
    filemode='a',
    format='%(levelname)s - %(asctime)s - %(message)s')

class Machine:
    def __init__(self, ID, OS, Disk, Ram, Cores):
        self.ID = ID
        self.OS = OS
        self.Disk = Disk
        self.Ram = Ram
        self.Cores = Cores

        logging.info(f"Created a new machine: {self.ID}") #Didnt implement self.logger because there is only a single class.

    def InstanceToDict(self):
        return {
            "ID" : self.ID,
            "OS": self.OS,
            "Disk": self.Disk,
            "Ram" : self.Ram,
            "Cores": self.Cores}
    


            # self.logger = logging.basicConfig(
            # level=logging.WARNING,
            # filename='Logs/provisioning.log',
            # filemode='a',
            # format='%(levelname)s - %(asctime)s - %(message)s')
import logging
import os
LOG_PATH = "Logs/provisioning.log"

class Machine:

    #Handles the logging setup: Ensure file exsistence, configure logging parameters + REQUIRED in order to create a class level loger
    def LOG_Handler(): 
        try:   #Validates the log file exist, if not it creates it.
            directory = os.path.dirname(LOG_PATH)
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created the log folder: {directory}")

            if not os.path.exists(LOG_PATH):
                with open(LOG_PATH, "w") as file:
                    file.write("")
                print(f"Created the log file: {LOG_PATH}")

        except OSError:
            print(f"Failed to create the log folder: {os.path.dirname(LOG_PATH)}")
            exit(2)

        # Create a class-level logger
        logger = logging.getLogger("MachineLogger")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('Logs/provisioning.log', mode='a')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s - %(name)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    LOG_Handler()

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
    

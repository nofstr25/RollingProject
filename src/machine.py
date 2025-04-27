import logging
import os

LOG_PATH = "Logs/provisioning.log"

class Machine:

    @classmethod
    def LOG_Handler(cls): 
        try:
            directory = os.path.dirname(LOG_PATH)
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created the log folder: {directory}")

            if not os.path.exists(LOG_PATH):
                with open(LOG_PATH, "w") as file:
                    file.write("")
                print(f"Created the log file: {LOG_PATH}")

        except OSError:
            print(f"Failed to create the log folder: {directory}")
            exit(2)

        # Create a class-level logger
        cls.logger = logging.getLogger("MachineLogger")
        cls.logger.setLevel(logging.DEBUG)

        if not cls.logger.handlers:  # Prevent adding multiple handlers
            handler = logging.FileHandler(LOG_PATH, mode='a')
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s - %(name)s')
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)

    def __init__(self, ID, OS, Disk, Ram, Cores):
        self.ID = ID
        self.OS = OS
        self.Disk = Disk
        self.Ram = Ram
        self.Cores = Cores

        Machine.logger.info(f"Created a new machine: {self.ID}")

    def InstanceToDict(self):
        return {
            "ID": self.ID,
            "OS": self.OS,
            "Disk": self.Disk,
            "Ram": self.Ram,
            "Cores": self.Cores
        }

# Initialize logging setup
Machine.LOG_Handler()

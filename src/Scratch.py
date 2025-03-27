


from cerberus import Validator

# Define the schema for validation
schema = {
    'disk_size': {
        'type': 'integer',
        'min': MinDisk,
        'max': MaxDisk
    },
    'ram_size': {
        'type': 'integer',
        'min': MinRam,
        'max': MaxRam
    },
    'core_count': {
        'type': 'integer',
        'min': MinCores,
        'max': MaxCores
    }
}

validator = Validator(schema)

def get_valid_input(prompt, field):
    """Function to validate input immediately using Cerberus."""
    while True:
        user_input = input(prompt)
        if user_input in QUITVALS:
            exit(1)
        try:
            value = int(user_input)
        except ValueError:
            print(f"Invalid input for {field}. Please enter a number.")
            continue

        # Validate using Cerberus
        if validator.validate({field: value}):
            return value
        else:
            print(f"Invalid {field} value. Please enter a number between {schema[field]['min']} and {schema[field]['max']}.")

# Example usage:
disk_size = get_valid_input("Enter disk space (bytes): ", 'disk_size')






import json
from sys import argv as argv
CONFIG_PATH = "config.json"
MACHINES_CONF = "Machines.json"
QUITVALS = ["q", "Q", "quit", "Quit", "QUIT", "--quit", "--Quit", "--QUIT"]


def JsonLoad(file_path):
    #Used for loading a Json (config.json or machines.json) as a dict (this is why it use passed arg)
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except(FileNotFoundError):
        raise(Exception("File was passed, but it doesn't exsist"))

def JsonWrite(machine, file_path):
    #Pushes a machine dict into machines.json
    conf = JsonLoad(file_path) 
    conf[machine["ID"]] = machine     #Sets a key named by the given machine ID, with the machine dict itslef as its value
    with open(file_path, "w") as file:
        json.dump(conf, file)




def GetParams():
    machines = JsonLoad(MACHINES_CONF) #Get all machins for validating the ID
    config = JsonLoad(CONFIG_PATH) # Load configuration for valid params
    #Simplify the configured params with short variables
    MinDisk, MaxDisk = config["MinDisk"], config["MaxDisk"]
    MinRam, MaxRam = config["MinRam"], config["MaxRam"]
    MinCores, MaxCores = config["MinCores"], config["MaxCores"]
    OsList = config["OsList"]
 
    #This section validates all of the params

    #Get And Validate The IDs
    while True:
        ids = input("What Machine id's do you want to create?\n").split()
        if ids[0] in QUITVALS:
            exit(1)
        for id in ids:
            
            if id in machines:
                print(f"The given id {id} already exsists")
                continue
            else:
                pass
        break
    #Get And Validate Vhe OS
    while True:
        Os = input("What operating system do you want to run on the machines?\n")
        if Os in QUITVALS:
            exit(1)  
        elif Os.lower() not in OsList:
            print(f"Unsupported operating system: {Os}\n")
            continue
        else:
            break

    #Get And Validate The Disk
    while True:
        Disk = input("How much disk space would you like to assign?")
        if Disk in QUITVALS:
            exit(1)
        if Disk.isdigit():
            Disk = int(Disk)
        else:
            print("Disk size must be a number")
            continue

        if MinDisk > Disk or Disk > MaxDisk:
            print(f"Disk size must be between {MinDisk}-{MaxDisk} bytes")
            continue
        else:
            break

    #Get And Validate The Ram
    while True:
        Ram = input("How much Ram space would you like to assign?")
        if Ram in QUITVALS:
            exit(1)
        if Ram.isdigit():
            Ram = int(Ram)
        else:
            print("Ram size must be a number")
            continue

        if MinRam > Ram or Ram > MaxRam:
            print(f"Ram size must be between {MinRam}-{MaxRam} bytes")
            continue
        else:
            break



    #Get And Validate The Cores
    while True:
        Cores = input("How much Cores space would you like to assign?")
        if Cores in QUITVALS:
            exit(1)
        if Cores.isdigit():
            Cores = int(Cores)
        else:
            print("Cores size must be a number")
            continue

        if MinCores > Cores or Cores > MaxCores:
            print(f"Cores size must be between {MinCores}-{MaxCores} bytes")
            continue
        else:
            break

def CreateMachine(ids, Os, Disk, Cores):    
    NewMachines = {}  # Dictionary to store instances
    for id in ids: #Sets each id as an instance with the parsed params.
        NewMachines[id] = Machine(id, Os, Disk, Cores)
        instance = NewMachines[id]
        machine_conf = instance.InstanceToDict() #converts all self.param to a dict
        JsonWrite(machine_conf, MACHINES_CONF)
    print(f"Created the new machines: {list(NewMachines.keys())}")

def MachineUpdate(ids=None): #Depricated - Didn't have time to finish, isn't a project goal
    Allmachines = JsonLoad(MACHINES_CONF)
    if ids == None:
        ids = input("What Machine id's do you want to update?").split()
    Key = input("What Key would you like to update?")
    Value = input("What is the new value? ")
    for id in ids:
        machine = Allmachines[id]
        machine[Key] = Value
        JsonWrite[machine, MACHINES_CONF]

def StartMachine():
    ActiveMachines = {}
    machines  = JsonLoad(MACHINES_CONF)
    requests = input("What machines would you like to start? (-a for all)").split
    if "-a" in requests.lower() or "--all" in requests.lower():
        #Was desided it's safer to check if -a is in the answer and just operate on all to prevent machines named -a or --All.
        #although possible to handle, unessasery anoing
        for machine in machines:
            ActiveMachines[machine["ID"]] = Machine(machine["ID"], machine["Os"], machine["Disk"], machine["Cores"])
    else:
        for id in requests: 
            try:
                machine = machines[id]
                ActiveMachines[machine["ID"]] = Machine(machine["ID"], machine["Os"], machine["Disk"], machine["Cores"])
            except:
                raise(Exception(f"the machine: {machine} doesn't exsist"))
            
#LIST IMPLEMENTATION:
# def StartMachineL():
#     MachinesList = []
#     machines  = JsonLoad(MACHINES_CONF)
#     requests = input("What machines would you like to start? (-a for all)").split
#     if "-a" in requests.lower() or "--all" in requests.lower():
#         #Was desided it's safer to check if -a is in the answer and just operate on all to prevent machines named -a or --All.
#         #although possible to handle, unessasery anoing
#         for machine in machines:
#             instanse =  Machine(machine["ID"], machine["Os"], machine["Disk"], machine["Cores"])
#             MachinesList.append(instanse)
#     else:
#         for id in requests: 
#             try:
#                 instanse =  Machine(machine["ID"], machine["Os"], machine["Disk"], machine["Cores"])
#                 MachinesList.append(instanse)
#             except:
#                 raise(Exception(f"the machine: {machine} doesn't exsist"))

def Welcome():
    print("Hello! ")
    while True:
        Action = input("What action would you like to perform next?\nfor help use --help").lower()
        if Action == "--startmachine" or Action == "--start":
            StartMachine()
        elif Action == "--createmachine" or Action == "--create":
            CreateMachine()
        elif Action in QUITVALS:
            print("Good By")
            exit(0)
        else: 
            print("Invalid action, please try again")
            continue


class Machine:
    def __init__(self, ID, OS, Disk, Cores):
        self.ID = ID
        self.OS = OS
        self.Disk = Disk
        self.Cores = Cores

    def InstanceToDict(self):
        return {"ID" : self.ID, "OS": self.OS, "Disk": self.Disk, "Cores": self.Cores}

    

def Main():
    # config = JsonLoad(CONFIG_PATH)
    ids = input("ID?").split()
    Os = "windows"
    Disk = 900
    Cores = 3
    CreateMachine(ids, Os, Disk, Cores)


    # Windows.ParsedStart(parser)
    # ArgsValidate(args, config)


    # print(args)
    # print(f"The OS is {args.operationalSystem}")
    # print(f"The Mode is {args.Mode}")
    # print(f"The Disk is {args.DiskSpace}")
    # print(f"The Ram is {args.Ram}")
    # print(f"The Cores is {args.Cores}")


Main()
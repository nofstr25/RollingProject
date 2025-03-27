import json
from machine import Machine
import logging
import subprocess
import jsonschema # Full library is required for working with its exceptions 
CONFIG_PATH = "configs/config.json"
MACHINES_CONF = "configs/instances.json"
README_PATH = "README.MD"
QUITVALS = ["--quit," "--Quit", "--QUIT", "-q", "-Q", "--q", "--Q"] #using one of those will quite the progrem
HELPVALS = ["--help", "--Help", "--HELP", "-h", "-H", "--h", "--H"] #using one of those will display the README.MD

# FOR AI TO KNOW THE CLASS I USED
# class Machine:
#     def __init__(self, ID, OS, Disk, Ram, Cores):
#         self.ID = ID
#         self.OS = OS
#         self.Disk = Disk
#         self.Ram = Ram
#         self.Cores = Cores

#     def InstanceToDict(self):
#         return {
#             "ID" : self.ID,
#             "OS": self.OS,
#             "Disk": self.Disk,
#             "Ram" : self.Ram,
#             "Cores": self.Cores}

# Opens the read me file and print it
def ReadMe():
    with open(README_PATH, "r") as file:
        print(file.read())
    input("Press Enter to continue...")
        
#Used for loading a Json (config.json or machines.json) as a dict (this is why it use passed arg)
def JsonLoad(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except(FileNotFoundError):
        print(f"The file: {file_path} doesn't exsist")
        exit(2)
    
#Pushes a machine dict into machines.json
def JsonWrite(machine, file_path):
    conf = JsonLoad(file_path) 
    conf[machine["ID"]] = machine     #Sets a key named by the given machine ID, with the machine dict itslef as its value
    with open(file_path, "w") as file:
        json.dump(conf, file)

def validate_jsons(path):
    if path == CONFIG_PATH:
        schema = {
        "type": "object",
        "properties": {
            "MinDisk": {"type": "integer"},
            "MaxDisk": {"type": "integer"},
            "DefaultDisk": {"type": "integer"},
            "MinRam": {"type": "integer"},
            "MaxRam": {"type": "integer"},
            "DefaultRam": {"type": "integer"},
            "MinCores": {"type": "integer"},
            "MaxCores": {"type": "integer"},
            "DefaultCores": {"type": "integer"},
            "OsList": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["MinDisk", "MaxDisk", "DefaultDisk", 
                     "MinRam", "MaxRam", "DefaultRam",
                    "MinCores", "MaxCores", "DefaultCores",
                    "OsList"]
                   }
    elif path == MACHINES_CONF:
        schema = {
        "type": "object",
        "patternProperties": {
            ".*": {
                "type": "object",
                "properties": {
                    "ID": {"type": "string"},
                    "OS": {"type": "string"},
                    "Disk": {"type": "integer"},
                    "Ram": {"type": "integer"},
                    "Cores": {"type": "integer"}
                },
                "required": ["ID", "OS", "Disk", "Ram", "Cores"]
                    }
                },
            }

    Json = JsonLoad(path)
    try:
        jsonschema.validate(instance=Json, schema=schema)
        print(f"{path} is valid.")
    except jsonschema.exceptions.ValidationError as err:
        print(f"The file {path} isn't in a vlaid json format:\n", err)
        exit(3)



        
#Used for validating numaric machine params.
def validate_numeric_input(param, min_val, max_val, defaultVal):
    while True:
        value = input(f"please asign the desired {param} (default: {defaultVal})")
        
        #If the user didn't input anything, the default value will be used
        if not value: 
            value = int(defaultVal)
            print(f"Default value: {value} was choosen")
            break

        #Checks if the value is a quit or help
        if value in QUITVALS: 
            exit(1)
        elif value in HELPVALS:
            ReadMe()
            continue
        
        #Actual data validation
        elif not value.isdigit():
            print("Input must be a number")
            continue  
        else:
            value = int(value)
        if value < min_val or value > max_val:
            print(f"Value must be between {min_val}-{max_val}\n")
            continue
        else:
            break
    print(f"Value: {value} was choosen")
    return value
    
def GetParams():
    machines = JsonLoad(MACHINES_CONF) #Get all machins for validating the ID
    config = JsonLoad(CONFIG_PATH) # Load configuration for valid params
    #Assign configured values to variables
    DefaultDisk, MinDisk, MaxDisk = config["DefaultDisk"], config["MinDisk"], config["MaxDisk"]
    DefaultRam, MinRam, MaxRam = config["DefaultRam"], config["MinRam"], config["MaxRam"]
    DefaultCores, MinCores, MaxCores = config["DefaultCores"], config["MinCores"], config["MaxCores"]
    OsList = config["OsList"]
 
    #This section validates all of the params

    #Get And Validate The IDs
    while True:
        ids = input("Please name all machines you want to create\n").split()
        if not ids:
            continue
        if ids[0] in QUITVALS:
            exit(1)
        elif ids[0] in HELPVALS:
            ReadMe()
            continue
        for id in ids:
            if id in machines:
                print(f"The given id {id} already exsists")
                continue
        break

    #Setting params for the machines:
    print("\nNotice:\nThe BulkBuilder \"--createMachine\" command creates multiple machines with the same configuration.\n"
          "assigend parameters will be used for all mentioned machines:\n\n")
    #Get And Validate Vhe OS
    while True:
        Os = input("What operating system do you want to asign for  the machines?\n")
        if Os.lower() in QUITVALS:
            exit(1)  
        elif Os.lower() not in OsList:
            print(f"Unsupported operating system: {Os}\n")
            continue
        else:
            break

    #Get And Validate The Disk
    Disk = validate_numeric_input("Disk", MinDisk, MaxDisk, DefaultDisk)
    #Get And Validate The Ram
    Ram = validate_numeric_input("Ram", MinRam, MaxRam, DefaultRam)
    #Get And Validate The Cores
    Cores = validate_numeric_input("Cores", MinCores, MaxCores, DefaultCores)
    return ids, Os, Disk, Ram, Cores

#Same function as CreateMachine but with logging
def CreateMachineLog():
    ids, Os, Disk, Ram, Cores = GetParams()  
    NewMachines = {}  # Dictionary to store instances
    for id in ids: #Sets each id as an instance with the parsed params.
        NewMachines[id] = Machine(id, Os, Disk, Ram, Cores)
        instance = NewMachines[id]
        machine_conf = instance.InstanceToDict() #converts all self.param to a dict
        JsonWrite(machine_conf, MACHINES_CONF)
        # logging.info(f"Created machine: {id}")
    print(f"Created the new machines: {list(NewMachines.keys())}")

def CreateMachine():
    ids, Os, Disk, Ram, Cores = GetParams()  
    NewMachines = {}  # Dictionary to store instances
    for id in ids: #Sets each id as an instance with the parsed params.
        NewMachines[id] = Machine(id, Os, Disk, Ram, Cores)
        instance = NewMachines[id]
        subprocess.run(["bash", "scripts/Install_machines.sh", id, Os, str(Disk), str(Ram), str(Cores)])
        machine_conf = instance.InstanceToDict() #converts all self.param to a dict
        JsonWrite(machine_conf, MACHINES_CONF)

    print(f"Created the new machines: {list(NewMachines.keys())}\n")


#Starts desired machines based on their configuration in instances.json
def StartMachine():
    ActiveMachines = {}
    machines  = JsonLoad(MACHINES_CONF)
    requests = input("What machines would you like to start? (-a for all)\n").split()
    if "-a" in requests or "--all" in requests or "-A" in requests or "--ALL" in requests:
        #Was desided it's safer to check if -a is IN the answer and not THE answer to prevent machines named -a or --All.
        for machine in machines.values():
            ActiveMachines[machine["ID"]] = Machine(machine["ID"], machine["OS"], machine["Disk"], machine["Ram"], machine["Cores"])
            print(f"Started machine: {machine['ID']}")
        print(f"All machines are now running: {ActiveMachines.keys()}")
    else:
        for id in requests: 
            try:
                machine = machines[id]
                ActiveMachines[machine["ID"]] = Machine(machine["ID"], machine["OS"], machine["Disk"], machine["Ram"], machine["Cores"])
            except KeyError:
                print(f"The machine: {id} doesn't exist")
#subprocess that passes a variable into and start a bash script:


def Welcome():
    print("Hello!\nWelcome to BulkBuilder\n"
          "BultBuilder is a simple tool that lets you create and run multiple virtual machines at once..\n"
          "At any time for help use --help\n"
          )
    while True:
        Action = input("What action would you like to perform next?\n"
                    "--start or --startmachines for starting machines\n"
                    "--create or --createmachines for creating machines\n"   
                    "for help use --help\n").lower().strip()

        if Action in QUITVALS:
            print("Good By")
            exit(1)
        elif Action in HELPVALS:
            ReadMe()
        #Runs saved machines as instances    
        elif Action == "-s" or Action == "--startmachines" or Action == "--start":
            StartMachine()
        elif Action == "-c" or Action == "--createmachine" or Action == "--create":
            CreateMachine()
        else: 
            print("Invalid action, please try again")
            continue
    
def Main():
    validate_jsons(CONFIG_PATH)
    validate_jsons(MACHINES_CONF)
    Welcome()

Main()

# def MachineUpdate(ids=None): #Depricated - Didn't have time to finish, isn't a project goal
#     Allmachines = JsonLoad(MACHINES_CONF)
#     if ids == None:
#         ids = input("What Machine id's do you want to update?").split()
#     Key = input("What Key would you like to update?")
#     Value = input("What is the new value? ")
#     for id in ids:
#         machine = Allmachines[id]
#         machine[Key] = Value
#         JsonWrite[machine, MACHINES_CONF]
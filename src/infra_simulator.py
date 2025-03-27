import json
import logging
from machine import Machine
import jsonschema

CONFIG_PATH = "../configs/config.json"
MACHINES_CONF = "../configs/instances.json"
README_PATH = "../README.MD"
QUITVALS = ["--quit, --Quit", "--QUIT", "-q", "-Q", "--q", "--Q"] #using one of those will quite the progrem
HELPVALS = ["--help", "--Help", "--HELP", "-h", "-H", "--h", "--H"] #using one of those will display the README.MD
# Open the read me file and print it
def ReadMe():
    with open(README_PATH, "r") as file:
        print(file.read())
    input("Press any key to continue...")
        
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
                "required": ["ID", "OS", "Disk", "Ram" "Cores"]
                    }
                },
            }

    Json = JsonLoad(path)
    try:
        jsonschema.validate(instance=Json, schema=schema)
        print("JSON is valid.")
    except jsonschema.exceptions.ValidationError as err:
        print("JSON is invalid:", err)



        
#Used for validating numaric machine params.
def validate_numeric_input(param, min_val, max_val, defaultVal):
    while True:
        value = input(f"please asign the desired {param} (default: {defaultVal})")
        
        #Checks if the value is a quit or help
        if value in QUITVALS:
            exit(1)
        elif value in HELPVALS:
            ReadMe()
            continue
        
        #Actual data validation
        #Checks if default
        if value == "":
            value = defaultVal
            break
        #Checks if number
        elif value.isdigit():
            value = int(value)
        else:
            print("Input must be a number")
            continue
        #Checks if the value is within the allowed range
        if value < min_val or value > max_val:
            print(f"Value must be between {min_val}-{max_val}/n")
            continue
        return value
    
def GetParams():
    machines = JsonLoad(MACHINES_CONF) #Get all machins for validating the ID
    config = JsonLoad(CONFIG_PATH) # Load configuration for valid params
    #Assign configured values to variables
    DefDisk, MinDisk, MaxDisk = config["DefDisk"], config["MinDisk"], config["MaxDisk"]
    DefRam, MinRam, MaxRam = config["DefRam"], config["MinRam"], config["MaxRam"]
    DefCores, MinCores, MaxCores = config["DefCores"], config["MinCores"], config["MaxCores"]
    OsList = config["OsList"]
 
    #This section validates all of the params

    #Get And Validate The IDs
    while True:
        ids = input("Please name all machines you want to create, NOTICE:\n1. Machine id's must be uniqe\n" 
                    "2. BulkBuilder create \"stacks\" of machines, specified resources will be assign for all given machines\n"
                    "3. For additional help read README.MD\n").split()
        if ids[0] in QUITVALS:
            exit(1)
        elif ids[0] in HELPVALS:
            ReadMe()
            continue
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
        if Os.lower in QUITVALS:
            exit(1)  
        elif Os.lower() not in OsList:
            print(f"Unsupported operating system: {Os}\n")
            continue
        else:
            break

    #Get And Validate The Disk
    Disk = validate_numeric_input("Disk", MinDisk, MaxDisk, DefDisk)
    #Get And Validate The Ram
    Ram = validate_numeric_input("Ram", MinRam, MaxRam, DefRam)
    #Get And Validate The Cores
    Cores = validate_numeric_input("Cores", MinCores, MaxCores, DefCores)
    return ids, Os, Disk, Ram, Cores

def CreateMachine(ids, Os, Disk, Cores):    
    NewMachines = {}  # Dictionary to store instances
    for id in ids: #Sets each id as an instance with the parsed params.
        NewMachines[id] = Machine(id, Os, Disk, Cores)
        instance = NewMachines[id]
        machine_conf = instance.InstanceToDict() #converts all self.param to a dict
        JsonWrite(machine_conf, MACHINES_CONF)
    print(f"Created the new machines: {list(NewMachines.keys())}")

def MachineUpdate(ids):
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
            except KeyError:
                print(f"The machine: {id} doesn't exist")
            
def Welcome():
    print("Hello!\nWelcome to BulkBuilder\n"
          "BultBuilder is a simple tool that lets you create and run multiple virtual machines at once..\n"
          "At any time for help use --help\n"
          )
    while True:
        Action = input("What action would you like to perform next?\nfor help use --help").lower()
        if Action == "--startmachines" or Action == "--start":
            StartMachine()
        elif Action == "--createmachine" or Action == "--create":
            CreateMachine()
        elif Action in QUITVALS:
            print("Good By")
            exit(0)
        else: 
            print("Invalid action, please try again")
            continue
    

def Main():
    Welcome()
    # Windows.ParsedStart(parser)
    # ArgsValidate(args, config)


    # print(args)
    # print(f"The OS is {args.operationalSystem}")
    # print(f"The Mode is {args.Mode}")
    # print(f"The Disk is {args.DiskSpace}")
    # print(f"The Ram is {args.Ram}")
    # print(f"The Cores is {args.Cores}")


Main()
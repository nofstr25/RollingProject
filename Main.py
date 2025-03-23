import argparse
import json
from sys import argv as argv
CONFIG_PATH = "config.json"
MACHINES_CONF = "Machines.json"
QUITVALS = ["q", "Q", "quit", "Quit", "QUIT", "--quit", "--Quit", "--QUIT"]



def JsonLoad(file_path):
    #Used for loading a Json (config.json or machines.json) as a dict (this is why it uses parsed arg)
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

def CreateMachine(IdList, Os, Disk, Cores):
    NewMachines = {}  # Dictionary to store instances
    for id in IdList: #Sets each id as an instance with the parsed params.
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
    machines = input("What machines would you like to start? (-a for all)")
    config  = JsonLoad(MACHINES_CONF)


    pass

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

def ParsedStart():

    parser = argparse.ArgumentParser(description="Qucikly create a VM")
    parser.add_argument("--Create", type=str, required=False)
    parser.add_argument("--Start", type=str, required=False)
    parser.add_argument("--ID", type=str, required=False)
    parser.add_argument("-os", "--oparetionalSystem", type=str, required=False)
    parser.add_argument("-d", "--DiskSpace", type=int, required=False, default=10000)
    parser.add_argument("--Cores", type=int, required=False, default=1)
    parser.add_argument("-m", "--Mode", type=str, required=False, default="CLI")
    parser.add_argument("--Ram", type=int, required=False, default=400)

    args = parser.parse_args()

    if args.oparetionalSystem not in VM_LIST: 
        raise(Exception("OS isn't valid"))

    
    return args



# def MachinesLoad(id=None):
#     Machines = JsonLoad(MACHINES_CONF)
#     if id == None:
#         for i in Machines:
#             with open("Machines.json", "r") as Machines:
#                 Machines = json.load(Machines)
#                 return Machines



class Machine:
    def __init__(self, ID, OS, Disk, Cores):
        self.ID = ID
        self.OS = OS
        self.Disk = Disk
        self.Cores = Cores

    def InstanceToDict(self):
        return {"ID" : self.ID, "OS": self.OS, "Disk": self.Disk, "Cores": self.Cores}

    def ArgsValidate(self, args, config):
    # Need to implemet switch case with win and linux diffrences
        Allowed_Values  = config[args.oparetionalSystem]

        MinRam = Allowed_Values ["MinRam"]
        MaxRam = Allowed_Values ["MaxRam"]
        MaxDisk = Allowed_Values ["MaxDisk"]
        MinDisk = Allowed_Values ["MinDisk"]

        if args.DiskSpace < MaxDisk and args.DiskSpace > MinDisk:
            self.Disk = args.DiskSpace
        else:
            print(f"disk space must be between {MinDisk} - {MaxDisk}")
            exit(1)
        if args.Ram < MaxRam and args.Ram > MinRam:
            self.Ram = args.Ram
        else:
            print(f"Ram must be between {MinRam} - {MaxRam}")
            exit(1)
        properties = {
            "Disk" : self.Disk,
            "Cores" : self.Ram
        }    
        return properties    


    
    # return NewMachines
    

def Main():
    # config = JsonLoad(CONFIG_PATH)
    if argv > 1: 
        args = ParsedStart()
        Machine.ArgsValidate(args)
    # id = args.ID
    # # m1 = Windows(id)
    # # m1.ArgsValidate(args, config)
    # # print(m1.ID)``
    # m2 = Linux(id)
    # m2.ArgsValidate(args, config)
    # print(m2.ID)
    IdList = input("ID?").split()
    Os = "windows"
    Disk = 900
    Cores = 3
    CreateMachine(IdList, Os, Disk, Cores)


    # Windows.ParsedStart(parser)
    # ArgsValidate(args, config)


    # print(args)
    # print(f"The OS is {args.operationalSystem}")
    # print(f"The Mode is {args.Mode}")
    # print(f"The Disk is {args.DiskSpace}")
    # print(f"The Ram is {args.Ram}")
    # print(f"The Cores is {args.Cores}")


Main()
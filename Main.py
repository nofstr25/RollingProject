import argparse
import json

VM_LIST = ["Windows", "Linux"] 
MACHINES = {}
# SERVER_MODES = ["CLI", "GUI", "GUI_light", "Headless",] #Alowed modes to be used
#Alowed Servers to be used


def ParsedStart():

    parser = argparse.ArgumentParser(description="Qucikly create a VM")

    parser.add_argument("--ID", type=str, required=True)
    parser.add_argument("-os", "--oparetionalSystem", type=str, required=True)
    parser.add_argument("-d", "--DiskSpace", type=int, required=False, default=10000)
    parser.add_argument("--Cores", type=int, required=False, default=1)

    args = parser.parse_args()

    if args.oparetionalSystem not in VM_LIST: 
        raise(Exception("OS isn't valid"))

    # parser.add_argument("-m", "--Mode", type=str, required=False, default="CLI")
    # parser.add_argument("--Ram", type=int, required=False, default=4)

    
    return args

def ConfigLoad():
    with open("config.json", "r") as config:
       config = json.load(config)

    # print(config["Windows"]["MaxRam"])
    return config

class machine:
    def __init__(self, ID, Disk, Cores):
        self.ID = ID
        self.Disk = Disk
        self.Cores = Cores

class Windows(machine):
    def __init__(self, ID):
        self.ID = ID

    def ArgsValidate(self, args, config):
    # Need to implemet switch case with win and linux diffrences
        server_config = config[args.oparetionalSystem]
        print(f"This Is the server conf: {server_config}\n END OF CONF")

        MaxDisk = server_config["MaxDisk"]
        MinDisk = server_config["MinDisk"]
        MaxCores = server_config["MaxCores"]
        MinCores = server_config["MinCores"]

        if args.DiskSpace < MaxDisk and args.DiskSpace > MinDisk:
            Disk = args.DiskSpace
        else:
            print(f"disk space must be between {MinDisk} - {MaxDisk}")
            exit(1)
        if args.Cores < MaxCores and args.Cores > MinCores:
            Cores = args.Cores
        else:
            print(f"Cores must be between {MinCores} - {MaxCores}")
            exit(1)
        properties = {
            "Disk" : Disk,
            "Cores" : Cores
        }    
        return properties            

class Linux:
    def __init__(self, config):
        self.name = "Linux"


def Main():
    config = ConfigLoad()
    print(f"\n\nconfig is:\n {config}\nSTOP\n")
    args = ParsedStart()
    print(f"\n\nArgs are:\n {args}\nSTOP\n")
    id = args.ID
    m1 = Windows(id)
    m1.ArgsValidate(args, config)
    print(m1.ID)
    # Windows.ParsedStart(parser)
    # ArgsValidate(args, config)


    # print(args)
    # print(f"The OS is {args.operationalSystem}")
    # print(f"The Mode is {args.Mode}")
    # print(f"The Disk is {args.DiskSpace}")
    # print(f"The Ram is {args.Ram}")
    # print(f"The Cores is {args.Cores}")


Main()
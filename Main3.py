import argparse
import json


VM_LIST = ["Windows", "Linux"] 
SERVER_MODES = ["CLI", "GUI", "GUI_light", "Headless",] #Alowed modes to be used
 #Alowed Servers to be used
# with open("config.json", "r") as config:


VM_LIST = ["Windows", "Linux"] 
SERVER_MODES = ["CLI", "GUI", "GUI_light", "Headless",] #Alowed modes to be used
 #Alowed Servers to be used
# with open("config.json", "r") as config:



def ConfigLoad():
    with open("config.json", "r") as config:
       config = json.load(config)
    # print(config)
    # print("-"*20)
    # print(config["Windows"]["MaxRam"])
    return config

def ConfigWrite():
    config = ConfigLoad()
    Key = input("What Key would you like to update?")
    Value = input("What is the new value?  ") 
    config["Windows"][Key] = Value
    with open("config.json", "w") as File:
        json.dump(config, File)
class Windows:
    def __init__(self, args):
        self.name = "Windows"
    def ArgsValidate(self, args, config):
        server = self.name
        server_config = config[server]
        print(server_config)

        if args.Mode not in SERVER_MODES: 
            print("StartUp mode isn't valid")
            raise(Exception("StartUp mode isn't valid"))
        if args.DiskSpace > MaxDisk or args.DiskSpace < MinDisk: 
            print(f"disk space must be between {MinDisk} - {MaxDisk}")
            exit(1)
        if args.Ram > MaxRam or args.Ram < MinRam: 
            print(f"Ram must be between {MinRam} - {MaxRam}")
            exit(1)
        if args.Cores > MaxCores or args.Cores < MinCores: 
            print(f"Cores must be between {MinCores} - {MaxCores}")
            exit(1)
        return args
        
    # args = parser.parse_args()
    # return args
    def ParsedStart(parser):

        parser.add_argument("-os", "--oparetionalSystem", type=str, required=True)
        parser.add_argument("-m", "--Mode", type=str, required=False, default="CLI")
        parser.add_argument("-d", "--DiskSpace", type=int, required=False, default=10000)
        parser.add_argument("--Ram", type=int, required=False, default=4)
        parser.add_argument("--Cores", type=int, required=False, default=1)

        args = parser.parse_args()
        return args





def ParsedStart():

    parser = argparse.ArgumentParser(description="Qucikly create a VM")

    parser.add_argument("-os", "--oparetionalSystem", type=str, required=True)
    parser.add_argument("-m", "--Mode", type=str, required=False, default="CLI")
    parser.add_argument("-d", "--DiskSpace", type=int, required=False, default=10000)
    parser.add_argument("--Ram", type=int, required=False, default=4)
    parser.add_argument("--Cores", type=int, required=False, default=1)

    args = parser.parse_args()
    return args

def ArgsValidate(args, config):
    # Need to implemet switch case with win and linux diffrences
    if args.oparetionalSystem not in VM_LIST: 
        print("OS isn't valid")
        exit(1)
    server = args.oparetionalSystem
    config = ConfigLoad()
    server_config = config[server]
    print(server_config)


    # if args.Mode not in SERVER_MODES: 
    #     print("StartUp mode isn't valid")
    #     exit(1)
    # if args.DiskSpace > MaxDisk or args.DiskSpace < MinDisk: 
    #     print(f"disk space must be between {MinDisk} - {MaxDisk}")
    #     exit(1)
    # if args.Ram > MaxRam or args.Ram < MinRam: 
    #     print(f"Ram must be between {MinRam} - {MaxRam}")
    #     exit(1)
    # if args.Cores > MaxCores or args.Cores < MinCores: 
    #     print(f"Cores must be between {MinCores} - {MaxCores}")
    #     exit(1)
    # return args

def Main():
    config = ConfigLoad()
    Windows.ArgsValidate(config)
    args = ParsedStart()

    ArgsValidate(args, config)


    # print(args)
    # print(f"The OS is {args.oparetionalSystem}")
    # print(f"The Mode is {args.Mode}")
    # print(f"The Disk is {args.DiskSpace}")
    # print(f"The Ram is {args.Ram}")
    # print(f"The Cores is {args.Cores}")


Main()

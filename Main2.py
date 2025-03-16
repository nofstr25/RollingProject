import argparse
import json

VM_LIST = ["Windows", "Linux"] 
SERVER_MODES = ["CLI", "GUI", "GUI_light"] #Alowed modes to be used
 #Alowed Servers to be used
# with open("config.json", "r") as config:

MinDisk = 1000
MaxDisk = 50000
MinRam = 200
MaxRam = 8000
MinCores = 1
MaxCores = 10

def ParseVal():
    MinDisk, MaxDisk = 1000, 50000
    MinRam, MaxRam = 200, 8000
    MinCores = 1
    MaxCores = 10

    parser = argparse.ArgumentParser(description="Qucikly create a VM")

    parser.add_argument("-os", "--oparetionalSystem", type=str, required=True)
    parser.add_argument("-m", "--Mode", type=str, required=True)
    parser.add_argument("-d", "--DiskSpace", type=int, required=True)
    parser.add_argument("--Ram", type=int, required=False, default=4)
    parser.add_argument("--Cores", type=int, required=False, default=1)

    args = parser.parse_args()
    # Need to implemet switch case with win and linux diffrences
    if args.oparetionalSystem not in VM_LIST: 
        print("OS isn't valid")
        exit(1)
    if args.Mode not in SERVER_MODES: 
        print("StartUp mode isn't valid")
        exit(1)
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

args = ParseVal()
print(args)
print(f"The OS is {args.oparetionalSystem}")
print(f"The Mode is {args.Mode}")
print(f"The Disk is {args.DiskSpace}")
print(f"The Ram is {args.Ram}")
print(f"The Cores is {args.Cores}")
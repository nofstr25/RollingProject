import json
from machine import Machine
import subprocess
import logging
import jsonschema # Full library is required for working with its exceptions 
CONFIG_PATH = "configs/config.json"
MACHINES_CONF = "configs/instances.json"
LOG_PATH = "Logs/provisioning.log"
README_PATH = "README.MD"
QUITVALS = ["--quit" "--Quit", "--QUIT", "-q", "-Q", "--q", "--Q"] #using one of those will quite the progrem
HELPVALS = ["--help", "--Help", "--HELP", "-h", "-H", "--h", "--H"] #using one of those will display the README.MD

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_PATH,
    filemode='a',
    format='%(levelname)s - %(asctime)s - %(message)s')

#Checks if a log file exists, if not it will create one
def CheckLog():
    try:
        with open(LOG_PATH, "r") as file:
            pass
    except FileNotFoundError:
        with open(LOG_PATH, "w") as file:
            pass

# Opens the read me file and print it,Notice it is in markdown format, but still readable in the console, i actually think it looks better this way
def ReadMe():
    try:
        with open(README_PATH, "r") as file:
            print("\n\n\n")
            print(file.read())
        logging.debug("The ReadMe file was reqested", exc_info=True)
        input("Press Enter to continue...")
    except(FileNotFoundError):
        logging.error(f"The file: {README_PATH} doesn't exist", exc_info=True)
        print(f"The file: {README_PATH} doesn't exist")
        exit(2)

#Used for loading a Json (config.json or machines.json) as a dict (this is why it use passed arg)
def JsonLoad(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except(FileNotFoundError):
        logging.critical(f"The file: {file_path} doesn't exist", exc_info=True)
        print(f"The file: {file_path} doesn't exist")
        exit(2)
    
#Pushes a machine dict into machines.json
def JsonWrite(machine, file_path):
    conf = JsonLoad(file_path) 
    conf[machine["ID"]] = machine     #Sets a key named by the given machine ID, with the machine dict itslef as its value
    with open(file_path, "w") as file:
        json.dump(conf, file)
    logging.debug(f"Config was updated, inserted machine: {machine['ID']}")

#Validates the jsons based on the schema
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
    #Loads the json and validates it based on the schema above    
    Json = JsonLoad(path)
    try:
        jsonschema.validate(instance=Json, schema=schema)
        logging.debug(f"Json Validator: {path} is valid.")
    except jsonschema.exceptions.ValidationError as err:
        logging.critical(f"The file {path} isn't in a valid json format:\n", exc_info=True)
        print(f"The file {path} isn't in a valid json format:\n", err)
        exit(3)

#Used for validating numaric machine params.
def validate_numeric_input(param, min_val, max_val, defaultVal):
    while True:
        value = input(f"please asign the desired {param} (default: {defaultVal})")
        
        #If the user didn't input anything, the default value will be used
        if not value: 
            value = int(defaultVal)
            print(f"Default value: {value} was chosen")
            break

        #Checks if the value is a quit or help
        if value in QUITVALS: 
            logging.info("User quit the program")
            exit(1)
        elif value in HELPVALS:
            logging.info("User requested help")
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
    print(f"Value: {value} was chosen")
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
    try:
        #Get And Validate The IDs
        while True:
            ids = input("Please name all machines you want to create\n").split()
            if not ids:
                continue
            if ids[0] in QUITVALS:
                logging.info("User quit the program")
                exit(1)
            elif ids[0] in HELPVALS:
                logging.info("User requested help")
                ReadMe()
                continue

            store_ids = ids #Stores the ids for safe iteration
            for id in store_ids: 
                if id in machines:
                    print(f"The given id \"{id}\" already exists and will be skipped")
                    ids.remove(id)
            if not ids: #If all ids are already in the machines.json Ask for 
                print("All given IDs are already in use, please try again")
                continue
            break

        #Setting params for the machines:
        print("\nNotice:\nThe BulkBuilder \"--createMachine\" command creates multiple machines with the same configuration.\n"
            "assigned parameters will be used for all mentioned machines:\n\n")
        #Get And Validate Vhe OS
        while True:
            Os = input("What operating system do you want to asign for the machines?\n")
            if Os.lower() in QUITVALS:
                logging.info("User quit the program")
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
        logging.info(f"Params were validated: {ids, Os, Disk, Ram, Cores}")
        return ids, Os, Disk, Ram, Cores
    except Exception as err:
        logging.error(f"Error Validating Params", exc_info=True)
        print("An error occured whilte trying to validate the params, please try again")

def CreateMachine():
    NewMachines = {}  # Dictionary to store instances
    FailedMachines = [] # List to store failed machines
    try: #Handle case where GetParams() fails to return the params
        ids, Os, Disk, Ram, Cores = GetParams()
    except TypeError:
        logging.error("CreateMachine Failed to get the machine parameters", exc_info=True)
        return
    
    for id in ids: #Sets each id as an instance with the parsed params.
        try:
            instance = Machine(id, Os, Disk, Ram, Cores)
            NewMachines[id] = instance
            machine_conf = instance.InstanceToDict() #converts all self.param to a dict
            JsonWrite(machine_conf, MACHINES_CONF)
        except Exception as err:
            logging.error(f"Failed to save machine configuration: {id} ", exc_info=True)
            print(f"Failed to write the machine: {id} to the configuration")
            FailedMachines.append(id)
        #Installs services on the new machines
        try:
            subprocess.run(["bash", "scripts/Install_machines.sh", id])
        except subprocess.CalledProcessError as err:
            logging.error(f"Failed to install services on the \"{id}\" machines due to a \"subprocess\" error:", exc_info=True)
            print(f"Failed to install services on the \"{id}\" due to a \"subprocess\" error: {id}\n {err}")
            
    if len(NewMachines) == len(ids):
        logging.info(f"Succesfully Created the new machines: {list(NewMachines.keys())}")
    else:
        logging.warning(f"The following machines were created successfully: {list(NewMachines.keys())}\n"
                        "Failed to create the following machines: {FailedMachines}")
    print(f"Created the new machines: {list(NewMachines.keys())}\n")


#Starts desired machines based on their configuration in instances.json
def StartMachine():
    ActiveMachines = {} #Dictionary to store the running machines
    machines  = JsonLoad(MACHINES_CONF)
    if not machines: #Checks if there are any machines to start
        logging.warning("Start Machine were called but there were no machines to start", exc_info=True)
        print("No machines to start:\n")
        return
    requests = input("What machines would you like to start? (-a for all)\n").split()
    if "-a" in requests or "--all" in requests or "-A" in requests or "--ALL" in requests:    #Was desided it's safer to check if -a is IN the answer and not THE answer to prevent machines named -a or --All.
        for machine in machines.values():
            try:
                ActiveMachines[machine["ID"]] = Machine(machine["ID"], machine["OS"], machine["Disk"], machine["Ram"], machine["Cores"])
                print(f"Started the machine: {machine['ID']}")
            except Exception:
                logging.error(f"Failed to start the machine: {machine['ID']}", exc_info=True)
                print(f"Failed to start the machine: {machine['ID']}")
    else:
        for id in requests: 
            try:
                machine = machines[id]
                ActiveMachines[machine["ID"]] = Machine(machine["ID"], machine["OS"], machine["Disk"], machine["Ram"], machine["Cores"])
                print(f"Started machine: {machine['ID']}")
            except KeyError:
                logging.warning(f"The machine: {id} doesn't exist", exc_info=True)
                print(f"The machine: {id} doesn't exist")
    if len(ActiveMachines) == len(requests):
        print(f"Successfully activated the requsted machines\n")
        logging.info(f"Activated requsted machines: {ActiveMachines.keys()}")
    else:
        print(f"The following machines were Successfully activated: {', '.join(ActiveMachines.keys())}\n")
def Welcome():
    print("\nHello!\nWelcome to BulkBuilder\n"
          "BultBuilder is a simple tool that lets you create and run multiple virtual machines at once..\n"
          "At any time for help use --help\n"
          )
    while True:
        logging.debug("Main loop was activated")
        Action = input("What action would you like to perform next?\n"
                    "--start or --startmachines for starting machines\n"
                    "--create or --createmachines for creating machines\n"   
                    "for help use --help\n").lower().strip()

        if Action in QUITVALS:
            print("Good By")
            logging.info("User quit the program")
            exit(1)
        elif Action in HELPVALS:
            ReadMe()
        elif Action == "-s" or Action == "--startmachines" or Action == "--start":
            logging.debug("Start machines was selected in main loop")
            StartMachine()   #Runs saved machines as based on their ID
        elif Action == "-c" or Action == "--createmachine" or Action == "--create":
            logging.debug("Create machines was selected in main loop")
            CreateMachine()  #Creates new machines 
        else: 
            print("Invalid action, please try again")
            continue
    
    
def Main():
    validate_jsons(CONFIG_PATH)
    logging.info("configuration was validated on Main run")
    print("Software configuration was validated")
    validate_jsons(MACHINES_CONF)
    logging.info("Machines file was validated on Main run")
    print("Machines configuration was validated")
    Welcome()

Main()

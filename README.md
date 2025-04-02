BulkBuilder
===========

BulkBuilder is a simple tool for creating and managing multiple virtual machines efficiently. It provides an interactive command-line interface to create and launch virtual machines based on predefined JSON configurations.


Features
--------

*   Create multiple virtual machines with a single command.
    
*   Assign machine resources based on configured parameters.
    
*   Automatically install necessary services on newly created machines.
    
*   Quickly start preconfigured machines based on machine IDs.
    

Installation
------------

Ensure the following dependencies are installed on your system:

*   Python 3.12 or later
    
*   Required Python module: jsonschema

*   For using with a virtual enviroment make sure to install requirments.txt
        

Configurations
-------------

Configuration files are stored inside configs/ directory

*   **config.json**: Defines default values and constraints for creating new machines.
    
*   **instances.json**: Stores information about created machines.

Notice: The configuration files DO NOT support comments.

Usage
-----

### Commands

Upon execution, BulkBuilder prompts the user to choose an action:
    
*   \--create or --createmachines: Create new virtual machines. (The actual required function for the project)

*   \--start or --startmachines: Start existing virtual machines. (Not required but its cool and will satisfy the Chokomoko gods)
    
*   \--help: Display the README file. (Recommended to open instead)
    
*   \--quit: Exit the program. (#SadFace)
    

### Creating Machines

First prompted to enter the desired machine IDs:

*   **Machine IDs** (Multiple IDs can be specified at once, separated by "Space")

Than prompted to enter the desired machines parameters: (parameters will affect all mentioned IDs)
    
*   **Operating System** (Supported oparetion systems are configured inside config.json)
    
*   **Disk size** (Values are in MB, limitations and default values are configured inside config.json)
    
*   **RAM size** (Values are in MB, limitations and default values are configured inside config.json)
    
*   **Number of CPU cores** (limitations and default values are configured inside config.json)
    

Once the parameters are validated:
*   Machines parameters are stored inside instances.json for later use.
*   Diffult Softwars are installed on the machine using a bash script.


### Starting Machines

Users can start machines stored inside instances.json by entering their IDs or use --all to start all available machines.
    

Future Enhancements
-------------------

*   Implement machine updates.
    
*   GUI-based configuration editor.

*   Actual Machines that work and stuff like that.

Loging
-------------------
Currently the log file is required for the software to run!
For convinience, the log file seperates the logs by their level and time of creation

License
-------

BulkBuilder is NOT open-sourced and the software rights are preserved for Chokomoko.ltd.

Developed with love by Nof Tsadok Strauss


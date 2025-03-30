BulkBuilder

BulkBuilder is a simple tool for creating and managing multiple virtual machines efficiently. It provides an interactive command-line interface to define machine parameters, validate configurations, and launch virtual machines based on predefined JSON configurations.


Features:
1. Create multiple virtual machines with a single command
2. Assign machines resources based on configured parameters
3. Automatically install necessary services on newly created machines
4. Quickly start preconfigured machines based on the machine IDs

Start machines based on saved configurations
Installation

Ensure that the following dependencies are installed on your system:
- Python 3.12 and above
- Required Python modules: jsonschema
- Configure new machine parameters inside "Configs/config.json"

CONFIGURATION:
The tool relies on two configuration files located in the configs/ directory:
config.json: Defines default values and constraints for machine the parameters.
instances.json: Stores information about created machines.

Both files must be correctly formatted for the tool to function properly. JSON schema validation ensures correctness.

Usage

Run the script using:

python main.py

Commands

Upon execution, BulkBuilder will prompt the user to choose an action:

--start or --startmachines: Start existing virtual machines.

--create or --createmachines: Create new virtual machines.

--help: Display the README file.

--quit: Exit the program.

Creating Machines

Users are prompted to enter:

Machine IDs (multiple IDs can be specified at once)

Operating System (must be one of the supported OS options in config.json)

Disk size (validated against configuration constraints)

RAM size (validated against configuration constraints)

Number of CPU cores (validated against configuration constraints)

Once the parameters are validated, machines are added to instances.json, and provisioning scripts (if available) are executed.

Starting Machines

Users can start specific machines by entering their IDs or use -a or --all to start all available machines.

Logging

BulkBuilder logs operations to Logs/provisioning.log, capturing:

Configuration validation

Machine creation success/failure

Machine startup attempts

Errors encountered

Error Handling

If any JSON file is missing or improperly formatted, the tool will:

Log the issue

Display an error message

Terminate execution with an appropriate exit code

Future Enhancements

Implement machine updates

Add support for additional machine configurations

Improve error handling and user feedback

License

This project is open-source and free to use under the MIT License.

Author

BulkBuilder was developed to simplify virtual machine provisioning and management. Contributions and improvements are welcome!


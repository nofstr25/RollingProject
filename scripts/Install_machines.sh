
if [ -z "$1" ]; then
  echo "Error: Machine id is missing"
  exit 1
fi

ID=$1

echo "Setting up services on the machine: $ID"
echo "Setting up Ngnix"
echo "1 2 3 Done"
sleep 1
echo "Setting up MongoDB"
echo "1 2 3 Done"
sleep 1
echo "Setting up Chokomoko v4.20"
echo "................... Done"
echo "All services are installed, Machine $ID is ready to use"
echo "CHO-KO-MO-KO!"
echo





# Depricated

# for arg in {1..5}; do
#   if [ -z "${!arg}" ]; then
#     echo "Error: Argument $i is missing"
#     exit 1
#   fi
# done

# ID=$1
# OS=$2
# Disk=$3
# Ram=$4
# Cores=$5

# # Print output
# echo "Setting up the Machine : $ID"
# echo "OS = $OS"
# echo "Disk = $Disk"
# echo "Ram = $Ram"
# echo "Cores = $Cores"

# echo "Machine $ID is ready to use"

#Depricated

#!/bin/bash
#Gets a dictonary like this: {"ID": "Machine1", "OS": "Windows", "Disk": 9000, "Ram": 2000, "Cores": 3}
#Print:  Setting up the Machine : {The value of ID}
#Print OS = {The value of OS}
#Print Disk = {The value of Disk}
#Print Ram = {The value of Ram}
#Print Cores = {The value of Cores}

# Check if jq is installed
# if ! [ -x "$(command -v jq)" ]; then
#   echo 'Error: jq is not installed.'
#   exit 1
# fi

# curl -L -o jq "https://github.com/stedolan/jq/releases/latest/download/jq-linux64"
# chmod a+x jq
# mv jq /usr/bin
# sleep 3
# echo "JQ installed"



# Use jq to parse JSON and extract values
# ID=$(echo "$json" | jq '.ID')
# OS=$(echo "$json" | jq '.OS')
# Disk=$(echo "$json" | jq '.Disk')
# Ram=$(echo "$json" | jq '.Ram')
# Cores=$(echo "$json" | jq '.Cores')
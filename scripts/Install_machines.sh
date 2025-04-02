
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
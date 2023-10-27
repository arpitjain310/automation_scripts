#!/bin/bash

# Check for required arguments
if [ $# -ne 4 ]; then
    echo "Usage: $0 <ResourceGroupName> <VMName> <VMNicName> <NewPublicIPName>"
    exit 1
fi

resourceGroupName="$1"
vmName="$2"
vmNicName="$3"
newPublicIPName="$4"

#Get the first IP configuration name for the NIC
ipConfigName=$(az network nic show --name $vmNicName --resource-group $resourceGroupName --query "ipConfigurations[0].name" --output tsv)

#Create a new public IP address
az network public-ip create --name $newPublicIPName --resource-group $resourceGroupName --allocation-method static

#Get the New Public IP address
newPublicIp=$(az network public-ip show --name $newPublicIPName --resource-group $resourceGroupName --query "ipAddress" --output tsv)

#Update the VMs NIC to use the new public IP address
az network nic ip-config update --name $ipConfigName --nic-name $vmNicName --resource-group $resourceGroupName --public-ip-address $newPublicIPName

echo "New Public IP address $newPublicIp assigned to VM $vmName's NIC $vmNicName ."
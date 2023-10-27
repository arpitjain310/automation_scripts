import csv
import subprocess
import argparse
import sys
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
log_file_name = f"cleanup_{timestamp}.log"
log_file = open(log_file_name, "w")
sys.stdout = log_file

def execute_az_command(command):
    try:
        subprocess.run(command, check=True,shell=True)
        print(command)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        pass

def main():
    parser = argparse.ArgumentParser(description="Delete Azure resources")
    parser.add_argument("csv_file_path", help="Path to the CSV file containing resource information")
    args = parser.parse_args()

    # Read the CSV file 
    try:
        with open(args.csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                resource_name = row['Resource Name']
                resource_type = row['Resource Type'].upper()

                if resource_type == "RESOURCE GROUP":
                    delete_rg_command = ['az', 'group', 'delete', '--name', resource_name, '--no-wait', '--yes']
                    execute_az_command(delete_rg_command)
                    print(f"Deletion initiated for Resource Group: {resource_name}. Check azure portal after few mins. to confirm deletion")
                else:
                    resource_group = row['Resource Group']
                    if resource_group:
                        if resource_type == "VIRTUAL MACHINE":
                            # Delete virtual machine
                            delete_vm_command = ['az', 'vm', 'delete', '--resource-group', resource_group, '--name', resource_name, '--yes']
                            execute_az_command(delete_vm_command)
                            print(f"Deleted Virtual Machine: {resource_name}")

                        elif resource_type == "KEY VAULT":
                            # Delete KeyVault
                            delete_kv_command = ['az', 'keyvault', 'delete', '--resource-group', resource_group, '--name', resource_name]
                            execute_az_command(delete_kv_command)
                            print(f"Deleted KeyVault: {resource_name}")

                        elif resource_type == "SEARCH SERVICE":
                            # Delete ACS Search Service
                            delete_acs_command = ['az', 'search', 'service', 'delete', '--resource-group', resource_group, '--name', resource_name, '--yes']
                            execute_az_command(delete_acs_command)
                            print(f"Deleted ACS Search Service: {resource_name}")

                    else:
                        print(f"Skipping resource {resource_name} of type {resource_type} as Resource Group is not specified.")
    except Exception as e:
        print(f"Error : {e}")
    finally:    
        log_file.close()

if __name__ == "__main__":
    main()

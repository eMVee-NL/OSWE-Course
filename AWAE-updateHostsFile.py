import os
import re
import sys

def banner():
    banner = """
                                 
         :                         
        *                 #        
       #:                  #       
      .#                   ##      
      ##           -       ##   :        _____ _ _ _ _____ _____    _____       _     _       _____         _       _____ _ _     
  #   +#     #####*###     #*   #       |  _  | | | |  _  |   __|  |  |  |___ _| |___| |_ ___|  |  |___ ___| |_ ___|   __|_| |___ 
  #    #-   ##########*    #    #       |     | | | |     |   __|  |  |  | . | . | .'|  _| -_|     | . |_ -|  _|_ -|   __| | | -_|
  *    ##*  # *###### #  ###    *       |__|__|_____|__|__|_____|  |_____|  _|___|__,|_| |___|__|__|___|___|_| |___|__|  |_|_|___|
  ##    #####   ##*   ##*##    ##                                        |_|                                                      
    ###   .:####.* #####.   +##    
      .#####- ####### :#####+      
            .##########                 Created by eMVee
           ##  *####  #*           
           #    * #    #           
           #    # #    #           
           *    # #    #           
            #     #   *            
             *       #             
              .                            
    """ 
    print(banner)
# Print banner
banner()

# Function to check if the script is run with sudo
def check_sudo():
    if os.geteuid() != 0:
        script_name = os.path.basename(__file__)  # Get the script's filename
        print(f"[!] This script must be run with sudo.")
        print(f"[-] Please run it as follows: sudo python3 {script_name}")
        sys.exit(1)

# Define the list of machines with the third octet replaced by 'xxx'
machines = {
    "atutor": "192.168.xxx.103",
    "bassmaster": "192.168.xxx.112",
    "manageengine": "192.168.xxx.113",
    "dnn": "192.168.xxx.120",
    "erpnext": "192.168.xxx.123",
    "opencrx": "192.168.xxx.126",
    "openitcockpit": "192.168.xxx.129",
    "concord": "192.168.xxx.132",
    "apigateway": "192.168.xxx.135",
    "chips": "192.168.xxx.138",
    "photog": "192.168.xxx.247",
    "sqeakr": "192.168.xxx.247",
    "docedit": "192.168.xxx.249",
    "answers": "192.168.xxx.251",
    "debugger": "192.168.xxx.253",
    "wiki": "192.168.xxx.100"
}

# Check if the script is run with sudo
check_sudo()

# Backup the current /etc/hosts file
hosts_file = '/etc/hosts'
backup_file = '/etc/hosts.bak'

# Create a backup of the hosts file
os.system(f'cp {hosts_file} {backup_file}')

# Read the current hosts file
with open(hosts_file, 'r') as file:
    current_hosts = file.readlines()

# Create a dictionary to hold current entries
current_entries = {}
for line in current_hosts:
    match = re.match(r'^\s*(\d+\.\d+\.\d+\.\d+)\s+(\S+)', line)
    if match:
        ip, name = match.groups()
        current_entries[name] = ip

# Ask for the new third octet once
new_third_octet = input("[+] Enter the new third octet for the machines: ")

# Prepare new entries
new_entries = {}
for name, default_ip in machines.items():
    new_ip = f"{default_ip.split('.')[0]}.{default_ip.split('.')[1]}.{new_third_octet}.{default_ip.split('.')[3]}"
    new_entries[name] = new_ip

# Write the updated entries back to the hosts file
try:
    with open(hosts_file, 'w') as file:
        # Write the original lines, replacing existing entries for the specified machines
        for line in current_hosts:
            match = re.match(r'^\s*(\d+\.\d+\.\d+\.\d+)\s+(\S+)', line)
            if match:
                _, name = match.groups()
                if name in new_entries:
                    # If the name is in new_entries, replace the line with the new IP
                    file.write(f"{new_entries[name]}\t{name}\n")
                else:
                    # Otherwise, keep the original line
                    file.write(line)
            else:
                # Write any non-matching lines (like comments) as is
                file.write(line)

        # Add a comment and the new entries for machines that were added
        file.write("\n# Added machines for AWAE (OSWE) course\n")
        for name, ip in new_entries.items():
            if name not in current_entries:  # Only add if it was not already present
                file.write(f"{ip}\t{name}\n")

    print("[!] Updated /etc/hosts file successfully.")

except KeyboardInterrupt:
    print("\n[I] Script interrupted by user. No changes were made.")
    sys.exit(0)

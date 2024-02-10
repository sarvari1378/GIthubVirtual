import os
import subprocess
import socket
import subprocess
import time

def create_user(username):
    # Check if the script is run as root
    if os.getuid() != 0:
        return "This script must be run as root"

    try:
        # Create a new user
        subprocess.run(["useradd", username], check=True)
        print(f"User '{username}' created successfully.")
        
        # Set password for the new user
        passwd = subprocess.run(["passwd", username], check=True)
        if passwd.returncode == 0:
            print(f"Password for '{username}' set successfully.")
        else:
            print(f"Failed to set password for '{username}'.")
    except subprocess.CalledProcessError:
        print(f"Failed to create user '{username}'.")


def save_config():
    # Get the IP address
    ip_address = socket.gethostbyname(socket.gethostname())

    # Get the available SSH ports
    ssh_ports = subprocess.check_output(["grep", "Port", "/etc/ssh/sshd_config"]).decode().split("\n")
    ssh_ports = [line.split()[1] for line in ssh_ports if line and not line.startswith("#")]

    # Write the IP address and SSH ports to the file
    with open("Config.txt", "w") as file:
        file.write(f"{ip_address}\n")
        file.write("\n".join(ssh_ports))


def wait_for_hours(hours):
    # Convert hours to seconds
    seconds = hours * 60 * 60
    time.sleep(seconds)

# Call the function with 6 hours
create_user("sajed")
save_config()

wait_for_hours(6)

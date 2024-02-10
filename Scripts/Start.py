import os
import subprocess
import socket
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
        # Note: You need to replace 'password' with the actual password
        subprocess.run(["echo", f"{username}:password", "|", "chpasswd"], check=True)
        print(f"Password for '{username}' set successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to create user '{username}'.")


def save_config():
    # Get the IP address
    ip_address = socket.gethostbyname(socket.gethostname())

    # Get the available SSH ports
    ssh_ports = subprocess.check_output(["grep", "Port", "/etc/ssh/sshd_config"]).decode().split("\n")
    ssh_ports = [line.split()[1] for line in ssh_ports if line and not line.startswith("#")]

    # Write the IP address and SSH ports to the file
    filename = "Config.txt"
    with open(filename, "w") as file:
        file.write(f"{ip_address}\n")
        file.write("\n".join(ssh_ports))
    
    return filename


def wait_for_hours(hours):
    # Convert hours to seconds
    seconds = hours * 60 * 60
    time.sleep(seconds)


def save_file_to_repo(filename):
    """
    Commit and push a file to the repository.
    """
    subprocess.run(["git", "config", "--local", "user.email", "action@github.com"], check=True)
    subprocess.run(["git", "config", "--local", "user.name", "GitHub Action"], check=True)
    subprocess.run(["git", "add", filename], check=True)
    subprocess.run(["git", "commit", "-m", f"Add {filename}"], check=True)
    subprocess.run(["git", "push"], check=True)


# Call the function with 6 hours
create_user("sajed")
config_filename = save_config()
save_file_to_repo(config_filename)

wait_for_hours(6)

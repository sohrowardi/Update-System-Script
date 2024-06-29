import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())

def main():
    # Update package lists
    print("Updating package lists...")
    run_command("sudo apt update")

    # Upgrade installed packages
    print("Upgrading installed packages...")
    run_command("sudo apt upgrade -y")

    # Install recommended drivers
    print("Installing recommended drivers...")
    run_command("sudo ubuntu-drivers autoinstall")

    # Clean up unnecessary packages and free up space
    print("Cleaning up unnecessary packages...")
    run_command("sudo apt autoremove -y")
    run_command("sudo apt autoclean")

    # Check and update Flatpak packages
    print("Checking and updating Flatpak packages...")
    result = subprocess.run("command -v flatpak", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        run_command("flatpak update -y")
    else:
        print("Flatpak not installed. Skipping Flatpak updates.")

    # Check and update Snap packages
    print("Checking and updating Snap packages...")
    result = subprocess.run("command -v snap", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        run_command("sudo snap refresh")
    else:
        print("Snap not installed. Skipping Snap updates.")

    # Check and update .deb packages
    print("Checking and updating .deb packages...")
    run_command("sudo apt-get dist-upgrade -y")

    print("System update and maintenance completed.")

if __name__ == "__main__":
    main()

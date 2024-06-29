import subprocess
import logging
import os

# Set up logging
LOGFILE = "/var/log/system_maintenance.log"
logging.basicConfig(filename=LOGFILE, level=logging.INFO, format='%(asctime)s %(message)s')

def log_error(message):
    logging.error(message)
    print(f"Error: {message}")

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        logging.info(output)
        print(output)
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode()
        log_error(error_message)
        print(error_message)

def main():
    # Update package lists
    logging.info("Updating package lists...")
    print("Updating package lists...")
    run_command("sudo apt update") or log_error("Failed to update package lists.")

    # Upgrade installed packages
    logging.info("Upgrading installed packages...")
    print("Upgrading installed packages...")
    run_command("sudo apt upgrade -y") or log_error("Failed to upgrade installed packages.")

    # Install recommended drivers
    logging.info("Installing recommended drivers...")
    print("Installing recommended drivers...")
    run_command("sudo ubuntu-drivers autoinstall") or log_error("Failed to install recommended drivers.")

    # Clean up unnecessary packages and free up space
    logging.info("Cleaning up unnecessary packages...")
    print("Cleaning up unnecessary packages...")
    run_command("sudo apt autoremove -y") or log_error("Failed to remove unnecessary packages.")
    run_command("sudo apt autoclean") or log_error("Failed to clean package cache.")

    # Check and update Flatpak packages
    if subprocess.run("command -v flatpak", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        logging.info("Updating Flatpak packages...")
        print("Updating Flatpak packages...")
        run_command("sudo flatpak update -y") or log_error("Failed to update Flatpak packages.")
        logging.info("Cleaning up Flatpak package cache...")
        print("Cleaning up Flatpak package cache...")
        run_command("sudo flatpak uninstall --unused -y") or log_error("Failed to clean Flatpak package cache.")
    else:
        logging.info("Flatpak not installed. Skipping Flatpak updates.")
        print("Flatpak not installed. Skipping Flatpak updates.")

    # Check and update Snap packages
    if subprocess.run("command -v snap", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        logging.info("Updating Snap packages...")
        print("Updating Snap packages...")
        run_command("sudo snap refresh") or log_error("Failed to update Snap packages.")
        logging.info("Cleaning up Snap package cache...")
        print("Cleaning up Snap package cache...")
        run_command("sudo snap remove --purge $(sudo snap list --all | awk '/disabled/{print $1, $3}')") or log_error("Failed to clean Snap package cache.")
    else:
        logging.info("Snap not installed. Skipping Snap updates.")
        print("Snap not installed. Skipping Snap updates.")

    # Check and update .deb packages
    logging.info("Checking and updating .deb packages...")
    print("Checking and updating .deb packages...")
    run_command("sudo apt-get dist-upgrade -y") or log_error("Failed to update .deb packages.")

    # Check for security updates
    logging.info("Checking for security updates...")
    print("Checking for security updates...")
    run_command("sudo unattended-upgrade --dry-run") or log_error("Failed to check for security updates.")

    # Check disk usage
    logging.info("Checking disk usage...")
    print("Checking disk usage...")
    run_command("df -h") or log_error("Failed to check disk usage.")

    # Check for filesystem errors
    logging.info("Checking for filesystem errors...")
    print("Checking for filesystem errors...")
    run_command("sudo fsck -A -R -N") or log_error("Failed to check filesystem errors.")

    # Check if a reboot is required
    if os.path.isfile("/var/run/reboot-required"):
        logging.info("A system reboot is required.")
        print("A system reboot is required.")

    logging.info("System update and maintenance completed.")
    print("System update and maintenance completed.")

if __name__ == "__main__":
    main()

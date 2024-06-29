import subprocess
import platform
import os
import logging
import distro  # Newer package for Linux distribution detection

# Set up logging
LOGFILE = "/var/log/system_maintenance.log"
logging.basicConfig(filename=LOGFILE, level=logging.INFO, format='%(asctime)s %(message)s')

def log_error(message):
    """Log an error message to the logfile and print it."""
    logging.error(message)
    print(f"Error: {message}")

def run_command(command):
    """Run a shell command and log its output or any errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(result.stdout.decode())
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        log_error(e.stderr.decode())

def detect_distro():
    """Detect the Linux distribution."""
    try:
        return distro.id().lower()
    except AttributeError:
        try:
            return subprocess.check_output(['lsb_release', '-is'], text=True).strip().lower()
        except subprocess.CalledProcessError as e:
            log_error("Failed to detect Linux distribution.")
            return "unknown"

def update_system(distro):
    """Update the system based on its distribution."""
    if distro in ["debian", "ubuntu", "mint"]:
        # Update for Debian-based systems
        run_command("sudo apt update")
        run_command("sudo apt upgrade -y")
        run_command("sudo apt autoremove -y")
        run_command("sudo apt autoclean")
    elif distro in ["fedora", "centos", "rhel"]:
        # Update for Red Hat-based systems
        run_command("sudo yum update -y")
        run_command("sudo yum autoremove -y")
        run_command("sudo yum clean all")
    elif distro in ["arch", "manjaro"]:
        # Update for Arch-based systems
        run_command("sudo pacman -Syu --noconfirm")
        run_command("sudo pacman -Rns $(pacman -Qtdq) --noconfirm")
    elif distro in ["opensuse", "suse"]:
        # Update for openSUSE-based systems
        run_command("sudo zypper refresh")
        run_command("sudo zypper update -y")
        run_command("sudo zypper clean -a")
    else:
        log_error("Unsupported Linux distribution")

def update_flatpak():
    """Update Flatpak packages if Flatpak is installed."""
    if subprocess.run("command -v flatpak", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        run_command("flatpak update -y")
        run_command("flatpak uninstall --unused -y")
    else:
        print("Flatpak not installed. Skipping Flatpak updates.")
        logging.info("Flatpak not installed. Skipping Flatpak updates.")

def update_snap():
    """Update Snap packages if Snap is installed."""
    if subprocess.run("command -v snap", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        run_command("sudo snap refresh")
        run_command("sudo snap remove --purge $(sudo snap list --all | awk '/disabled/{print $1, $3}')")
    else:
        print("Snap not installed. Skipping Snap updates.")
        logging.info("Snap not installed. Skipping Snap updates.")

def perform_additional_tasks(distro):
    """Perform additional maintenance tasks based on the distribution."""
    if distro in ["debian", "ubuntu", "mint"]:
        run_command("sudo apt-get dist-upgrade -y")  # For Debian-based systems

    # Check for security updates
    run_command("sudo unattended-upgrade --dry-run")

    # Check disk usage
    run_command("df -h")

    # Check for filesystem errors
    run_command("sudo fsck -A -R -N")

    # Check if a reboot is required
    if os.path.isfile("/var/run/reboot-required"):
        logging.info("A system reboot is required. Run 'sudo reboot' to restart.")
        print("A system reboot is required. Run 'sudo reboot' to restart.")

def main():
    """Main function to run system maintenance tasks."""
    if os.geteuid() != 0:
        print("This script must be run as root. Please use sudo.")
        return

    distro = detect_distro()
    logging.info(f"Detected distribution: {distro}")
    print(f"Detected distribution: {distro}")

    update_system(distro)
    update_flatpak()
    update_snap()
    perform_additional_tasks(distro)

    logging.info("System update and maintenance completed.")
    print("System update and maintenance completed.")

if __name__ == "__main__":
    main()

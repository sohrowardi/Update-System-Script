#!/bin/bash

# System Update and Maintenance Script for Kali Linux

# Log file
LOGFILE="/var/log/system_maintenance.log"
exec > >(tee -a "$LOGFILE") 2>&1

# Function to log errors
log_error() {
    echo "Error: $1" | tee -a "$LOGFILE" >&2
}

# Update package lists
echo "Updating package lists..."
sudo apt update || log_error "Failed to update package lists."

# Upgrade installed packages
echo "Upgrading installed packages..."
sudo apt upgrade -y || log_error "Failed to upgrade installed packages."

# Clean up unnecessary packages and free up space
echo "Cleaning up unnecessary packages..."
sudo apt autoremove -y || log_error "Failed to remove unnecessary packages."
sudo apt autoclean || log_error "Failed to clean package cache."

# Check and update Flatpak packages
if command -v flatpak &> /dev/null; then
    echo "Updating Flatpak packages..."
    sudo flatpak update -y || log_error "Failed to update Flatpak packages."
    echo "Cleaning up Flatpak package cache..."
    sudo flatpak uninstall --unused -y || log_error "Failed to clean Flatpak package cache."
else
    echo "Flatpak not installed. Skipping Flatpak updates."
fi

# Check and update Snap packages
if command -v snap &> /dev/null; then
    echo "Updating Snap packages..."
    sudo snap refresh || log_error "Failed to update Snap packages."
    echo "Cleaning up Snap package cache..."
    sudo snap remove --purge $(sudo snap list --all | awk '/disabled/{print $1, $3}') || log_error "Failed to clean Snap package cache."
else
    echo "Snap not installed. Skipping Snap updates."
fi

# Check and update .deb packages (assuming they are from official repositories)
echo "Checking and updating .deb packages..."
sudo apt-get dist-upgrade -y || log_error "Failed to update .deb packages."

echo "System update and maintenance completed."

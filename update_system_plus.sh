#!/bin/bash

# System Update and Maintenance Script

# Function to log errors
log_error() {
    echo "Error: $1" >&2
}

# Update package lists
echo "Updating package lists..."
sudo apt update || log_error "Failed to update package lists."

# Upgrade installed packages
echo "Upgrading installed packages..."
sudo apt upgrade -y || log_error "Failed to upgrade installed packages."

# Install recommended drivers
echo "Installing recommended drivers..."
sudo ubuntu-drivers autoinstall || log_error "Failed to install recommended drivers."

# Clean up unnecessary packages and free up space
echo "Cleaning up unnecessary packages..."
sudo apt autoremove -y || log_error "Failed to remove unnecessary packages."
sudo apt autoclean || log_error "Failed to clean package cache."

# Check and update Flatpak packages
if command -v flatpak &> /dev/null; then
    echo "Updating Flatpak packages..."
    flatpak update -y || log_error "Failed to update Flatpak packages."
    echo "Cleaning up Flatpak package cache..."
    flatpak uninstall --unused -y || log_error "Failed to clean Flatpak package cache."
else
    echo "Flatpak not installed. Skipping Flatpak updates."
fi

# Check and update Snap packages
if command -v snap &> /dev/null; then
    echo "Updating Snap packages..."
    sudo snap refresh || log_error "Failed to update Snap packages."
    echo "Cleaning up Snap package cache..."
    sudo apt autoremove --purge snapd -y || log_error "Failed to clean Snap package cache."
else
    echo "Snap not installed. Skipping Snap updates."
fi

# Check and update .deb packages (assuming they are from official repositories)
echo "Checking and updating .deb packages..."
sudo apt-get dist-upgrade -y || log_error "Failed to update .deb packages."

# Check for security updates
echo "Checking for security updates..."
sudo unattended-upgrade --dry-run || log_error "Failed to check for security updates."

echo "System update and maintenance completed."

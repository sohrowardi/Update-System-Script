#!/bin/bash

# System Update and Maintenance Script

# Update package lists
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Install recommended drivers
sudo ubuntu-drivers autoinstall

# Clean up unnecessary packages and free up space
sudo apt autoremove -y
sudo apt autoclean

# Check and update Flatpak packages
if command -v flatpak &> /dev/null; then
    flatpak update -y
else
    echo "Flatpak not installed. Skipping Flatpak updates."
fi

# Check and update Snap packages
if command -v snap &> /dev/null; then
    sudo snap refresh
else
    echo "Snap not installed. Skipping Snap updates."
fi

# Check and update .deb packages (assuming they are from official repositories)
sudo apt-get dist-upgrade -y

# Upgrade Pop!_OS system
if command -v pop-upgrade &> /dev/null; then
    sudo pop-upgrade release upgrade
else
    echo "pop-upgrade not installed. Skipping Pop!_OS release upgrade."
fi

echo "System update and maintenance completed."

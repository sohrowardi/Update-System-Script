#!/bin/bash

# System Update and Maintenance Script for Kali Linux

# Update package lists
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

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

echo "System update and maintenance completed."

#!/bin/bash

# System Update and Maintenance Script
set -e

# Log to file
exec > >(tee -i ~/update_log.txt)
exec 2>&1

echo "🔄 Starting system update and maintenance..."

# Update package lists
sudo apt update

# Full upgrade (includes dist-upgrade functionality)
sudo apt full-upgrade -y

# Install recommended drivers
sudo ubuntu-drivers autoinstall

# Clean up unnecessary packages
sudo apt autoremove -y
sudo apt autoclean

# Update Flatpak packages if installed
if command -v flatpak &> /dev/null; then
    flatpak update -y
else
    echo "⚠️  Flatpak not installed. Skipping Flatpak updates."
fi

# Update Snap packages if installed
if command -v snap &> /dev/null; then
    sudo snap refresh
else
    echo "⚠️  Snap not installed. Skipping Snap updates."
fi

echo "✅ System update and maintenance completed."

# Optional reboot prompt
read -p "Would you like to reboot now? (y/n): " answer
if [[ $answer =~ ^[Yy]$ ]]; then
    sudo reboot
fi

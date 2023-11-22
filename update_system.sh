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

echo "System update and maintenance completed."


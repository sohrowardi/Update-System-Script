# Update System Script

This script automates the process of updating and maintaining an Ubuntu-based system. It performs the following tasks:

1. Update package lists.
2. Upgrade installed packages.
3. Install recommended drivers.
4. Clean up unnecessary packages to free up space.

## Usage

1. Open a terminal on your Ubuntu system.
2. Clone this repository using the following command:

    ```bash
    git clone https://github.com/sohrowardi/Update-System-Script
    ```

3. Navigate into the cloned repository:

    ```bash
    cd update-system-script
    ```

4. Make the script executable:

    ```bash
    chmod +x update_system.sh
    ```

5. Run the script:

    ```bash
    ./update_system.sh
    ```

6. The script will prompt you for your password as it uses `sudo` to perform system-level tasks.
7. The script will run, updating your system and performing maintenance
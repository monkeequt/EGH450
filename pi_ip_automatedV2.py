#!/usr/bin/env python3

# This script retrieves the IP address of a specified network interface (e.g., wlan0 for Wi-Fi)
# and sends it to a Discord channel using a webhook. It is useful for monitoring the Raspberry Pi's
# network status or accessing its IP address remotely.


##########################################################################################
##### To run this script:
# 1. Save this script as pi_ip_automated.py on your Raspberry Pi.
# 2. Make sure you have Python 3 and the required libraries installed.
#    You can install the required libraries using pip as follows:
# pip3 install requests netifaces

# 3. Make the script executable  as follows:
# chmod +x pi_ip_automatedV2.py

# 4. Run the script using and see whether you receive the IP address in your Discord channel:
# python3 pi_ip_automated.py

# 5. Optionally, you can set up a cron job to run this script automatically on boot. The explanation can be found at the end of this script.
# 6. Make sure to replace the WEBHOOK_URL with your actual Discord webhook URL.
###########################################################################################

import requests
import netifaces

# Replace with your Discord webhook URL
# To set up a webhook:
# 1. Go to your Discord server settings.
# 2. Create a webhook in the desired channel and copy the webhook URL. then replace it here
## WEBHOOK_URL = ""

def get_ip_address(interface):
    """
    Fetch the IP address of a specified network interface.

    :param interface: Network interface name (e.g., wlan0 for Wi-Fi, eth0 for Ethernet)
    :return: IP address as a string or an error message
    """
    try:
        # Get a list of all available network interfaces
        interfaces = netifaces.interfaces()
        if interface in interfaces:
            # Get the addresses associated with the specified interface
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                # Return the IPv4 address of the interface
                return addrs[netifaces.AF_INET][0]['addr']
        return f"No valid IP address found for interface: {interface}"
    except Exception as e:
        return f"Error retrieving IP address for {interface}: {e}"

def send_to_discord(ip_address):
    """
    Send the IP address to Discord using a webhook.

    :param ip_address: IP address string
    """
    # Prepare the message to send to Discord
    data = {
        "content": f"📡 Raspberry Pi is online!\nIP Address: `{ip_address}`"
    }
    try:
        # Send the message to Discord using the webhook URL
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("IP address sent to Discord successfully.")
        else:
            print(f"Failed to send IP address: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending message to Discord: {e}")

if __name__ == "__main__":
    # Specify the network interface to monitor
    # Use "wlan0" for Wi-Fi or "eth0" for Ethernet
    network_interface = "wlan0"  # Change to "eth0" if using Ethernet

    # Get the IP address of the specified network interface
    ip_address = get_ip_address(network_interface)

    # Check if the IP address was retrieved successfully
    if ip_address.startswith("Error") or "No valid IP address" in ip_address:
        print(ip_address)  # Log the error
    else:
        # Send the IP address to Discord
        send_to_discord(ip_address)

# To run this script automatically on boot:
# 1. Open the crontab editor using the below command:
#    $ crontab -e
# 2. Add the following line to the crontab file. You can change the sleep time if needed:
#    @reboot sleep 60 &&  /usr/bin/python3 /home/<your RPi name>/<path to the script>/pi_ip_automated.py

#####Example:###### @reboot sleep 60 &&  /usr/bin/python3 /home/tronpi2/catkin_ws/src/tron_dynamixel/scripts/pi_ip_automatedV2.py


# 3. Save and exit the editor.
#    - If prompted to choose an editor, select one (e.g., nano).
# 4. Reboot the Raspberry Pi to test:
#    $ sudo reboot
# The script will run on boot and send the IP address to Discord.

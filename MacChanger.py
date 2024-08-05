#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="mac", help="New MAC address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("\033[91m[-] Please specify an interface, use --help for more info.")
    elif not options.mac:
        parser.error("\033[91m[-] Please specify a new mac, use --help for more info.")
    return options

def change_mac(interface, mac):
    print(f"\n\033[92m[+] Changing MAC address for {interface} to {mac}.", )
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    return re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

def is_mac_changed(current_mac, user_mac):
    if current_mac and current_mac.group(0) == user_mac:
        print(f"\033[92m[+] MAC address has been changed to {options.mac}.")
    else:
        print("\033[91m[-] Unfortunately MAC address has not been changed.")


# Getting options
options = get_arguments()

# Getting MAC address before change
current_mac = get_current_mac(options.interface)
print("\n\033[92mCurrent MAC =", current_mac.group(0))

# Changing MAC address
change_mac(options.interface, options.mac)

# Checking if MAC address has been changed
current_mac = get_current_mac(options.interface)
is_mac_changed(current_mac, options.mac)

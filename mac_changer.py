#!/usr/bin/python3.8

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    ops, arguments = parser.parse_args()

    if not ops.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not ops.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for more info")
    return ops


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
change_mac(options.interface, options.new_mac)
new_mac = get_current_mac(options.interface)

if new_mac == options.new_mac:
    print(f"[+] MAC address was successfully changed from {current_mac} to {new_mac}")
else:
    print(f"[-] MAC address did not changed")

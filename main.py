import subprocess
import random
import re
import json
import os
import argparse
import textwrap

def signature():
    sig = r"""
    ███╗   ███╗ █████╗  ██████╗     ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
    ████╗ ████║██╔══██╗██╔════╝    ██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
    ██╔████╔██║███████║██║         ██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
    ██║╚██╔╝██║██╔══██║██║         ██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║██║  ██║╚██████╗    ╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    print(sig)

def change_mac(interface, new_mac=None):
    try:
        subprocess.check_call(["sudo", "ifconfig", interface, "down"])
        if new_mac is None:
            new_mac = generate_mac_address()
        subprocess.check_call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        subprocess.check_call(["sudo", "ifconfig", interface, "up"])
    except subprocess.CalledProcessError as e:
        print(f"Error changing MAC address: {e}")
        exit(1)

def load_mac(interface):
    try:
        if os.path.exists("mac.json"):
            with open("mac.json", "r") as f:
                mac = json.load(f)
                subprocess.check_call(["sudo", "ifconfig", interface, "down"])
                subprocess.check_call(["sudo", "ifconfig", interface, "hw", "ether", mac["mac"]])
                subprocess.check_call(["sudo", "ifconfig", interface, "up"])
    except Exception as e:
        print(f"Error loading MAC address: {e}")
        exit(1)
    
def generate_mac_address():
    mac = [
        random.randint(0x00, 0xFF),
        random.randint(0x00, 0xFF),
        random.randint(0x00, 0xFF),
        random.randint(0x00, 0xFF),
        random.randint(0x00, 0xFF),
        random.randint(0x00, 0xFF),
    ]
    mac[0] &= 0xFC
    return ":".join(f"{byte:02x}" for byte in mac)

def preserve_mac(interface):
    try:
        result = subprocess.run(f"ip link show {interface} | awk '/ether/ {{print $2}}'", shell=True, capture_output=True, check=True)
        with open("mac.json", "w") as f:
            json.dump({"mac": result.stdout.decode().strip()}, f)
    except Exception as e:
        print(f"Error preserving MAC address: {e}")
        exit(1)

def get_current_mac(interface):
    try:
        result = subprocess.run(f"ip link show {interface} | awk '/ether/ {{print $2}}'", shell=True, stdout=subprocess.PIPE, check=True)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting current MAC address: {e}")
        exit(1)

def is_valid_mac(mac):
    if mac is None:
        return True
    pattern = r'^(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$' 
    return re.match(pattern, mac) is not None

def get_arguments():
    # to display help message in a more readable format help:(https://docs.python.org/3/library/argparse.html)
    parser = argparse.ArgumentParser(
        prog="PyMacChanger", 
        formatter_class= argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                    -----------------------------------------------------
        ----> PyMacChanger is a tool to change MAC address of a network interface.
        ----> It can also generate random MAC address or restore original MAC address.
                    ------------------------------------------------------
        '''),
        epilog="Developed by AGT Cyber")
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Interface to change its MAC address(mandatory)")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address(optional if -r is specified)")
    parser.add_argument("-o", "--original", dest="original_mac", action="store_true", help="Restore original MAC address")
    parser.add_argument("-r", "--random", dest="random", action="store_true", help="Generate random MAC address")
    parser.add_argument("-p", "--preserve", dest="preserve", action="store_true", help="Preserve current MAC address")
    parser.add_argument("-cli", "--cli", dest="cli", action="store_true", help="Command line GUI")
    args = parser.parse_args()
    
    if args.new_mac and not is_valid_mac(args.new_mac):
        parser.error("Invalid MAC address. Please use the following format: xx:xx:xx:xx:x:xx")
    
    return args

def main():
    signature()
    args = get_arguments()
    if args.preserve:
        preserve_mac(args.interface)
    
    if args.cli:
        while True:
            print("1. Change MAC Address")
            print("2. Generate Random MAC")
            print("3. Restore Original MAC")
            print("4. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                if not is_valid_mac(args.new_mac):
                    print("[-] Invalid MAC address, use --help for more info.")
                    return
                change_mac(args.interface, args.new_mac)
                print(f"Changed MAC: {args.new_mac}")
            elif choice == '2':
                args.new_mac = generate_mac_address()
                change_mac(args.interface, args.new_mac)
                print(f"Generated MAC: {args.new_mac}")
            elif choice == '3':
                load_mac(args.interface)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        if args.original_mac:
            print("[+] Restoring original MAC address...")
            load_mac(args.interface)
            exit(1)
        if args.random:
            print("[+] Generating random MAC address...")
            args.new_mac = generate_mac_address()
        if args.new_mac is None:
            print("[-] Please specify a new MAC address, use --help for more info.")
            exit(1)
        current_mac = get_current_mac(args.interface)
        print(f"Current MAC: {current_mac}")
        change_mac(args.interface, args.new_mac)
        new_mac = get_current_mac(args.interface)
        if new_mac == args.new_mac:
            print(f"[+] MAC address was successfully changed to {new_mac}")
        else:
            print("[-] MAC address did not get changed.")

if __name__ == "__main__":
    main()

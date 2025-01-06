# PyMacChanger

PyMacChanger is a tool to change the MAC address of a network interface. It can also generate a random MAC address or restore the original MAC address.

## Features

- Change the MAC address of a specified network interface.
- Generate a random MAC address.
- Restore the original MAC address.
- Preserve the current MAC address.
- Command line GUI for interactive usage.

## Installation

To use PyMacChanger, you need to have Python installed on your system. You can clone the repository and run the script directly.

```bash
git clone https://github.com/Sanjay-vcloud/PyMACChanger.git
cd PyMacChanger
```

## Usage

You can run the script with various command-line arguments to perform different actions.

### Command-Line Arguments

- `-i`, `--interface`: Interface to change its MAC address (mandatory).
- `-m`, `--mac`: New MAC address (optional if `-r` is specified).
- `-o`, `--original`: Restore the original MAC address.
- `-r`, `--random`: Generate a random MAC address.
- `-p`, `--preserve`: Preserve the current MAC address.
- `-cli`, `--cli`: Command line GUI.

### Examples

#### Change MAC Address

```bash
python3 main.py -i eth0 -m 00:11:22:33:44:55
```

#### Generate Random MAC Address

```bash
python3 main.py -i eth0 -r
```

#### Restore Original MAC Address

```bash
python3 main.py -i eth0 -o
```

#### Preserve Current MAC Address

```bash
python3 main.py -i eth0 -p
```

#### Command Line GUI

```bash
python3 main.py -cli
```

## Note
 You must run this script as root or use sudo to run this script for it to work properly. This is because changing a MAC address requires root privileges.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Developed by AGT Cyber.

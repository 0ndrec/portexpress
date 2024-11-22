# Port Scanner Tool
=====================

## Overview
------------
Single-file script without third-party dependencies for fast port scanning.
This is a Python-based port scanning tool that scans a target IP address for open ports. It uses the `socket` and `subprocess` modules to perform the scanning.

## Features
------------

* Scans a target IP address for open ports
* Uses parallel threads to speed up the scanning process
* Prints a progress bar to show the scanning progress
* Sends a curl request to the target IP address and port to retrieve the HTTP response code
* Prints the list of open ports and their corresponding HTTP response codes

### Running the Tool

1. Clone the repository: `git clone https://github.com/0ndrec/portexpress.git`
2. Run the tool: `python port_scanner.py <target_ip_address>`

### Example

`python scan.py 192.168.1.100`

## Options
------------

### Command Line Options [FUTURE]

* `-h` or `--help`: Show this help message and exit
* `-t` or `--target`: Specify the target IP address (required)
* `-s` or `--start-port`: Specify the starting port number (default: 1)
* `-e` or `--end-port`: Specify the ending port number (default: 65535)
* `-p` or `--ports`: Specify the number of parallel threads (default: 16)

## License
-------

This tool is released under the MIT License. See the LICENSE file for details.

## Author
--------

Your Name <your-email@example.com>

## Contributing
------------

Contributions are welcome! If you have any ideas or bug fixes, please submit a pull request.

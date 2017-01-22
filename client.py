#!/usr/bin/env python
import ConfigParser
import os
import socket
import ssl
import argparse

import norac.connection

DEFAULT_CONFIG_NAME="norac_default.cfg"
OVERRIDE_CONFIG_NAME="norac.cfg"

# Parse Configurations
config = ConfigParser.ConfigParser()
with open(DEFAULT_CONFIG_NAME, "r") as f:
    config.readfp(open(DEFAULT_CONFIG_NAME))
if os.path.exists(OVERRIDE_CONFIG_NAME):
    with open(OVERRIDE_CONFIG_NAME, "r") as f:
        config.readfp(open(OVERRIDE_CONFIG_NAME))

# Check for dangerous configuration
default = ConfigParser.ConfigParser()
with open(DEFAULT_CONFIG_NAME, "r") as f:
    default.readfp(open(DEFAULT_CONFIG_NAME))

if (config.get("security", "cafile") == default.get("security", "cafile")
    and config.get("security", "certificate") == default.get("security", "certificate")
    and config.get("security", "key") == default.get("security", "key")):
    # Default certificates are used in the application
    print("WARNING: EXAMPLE CERTIFICATES USED.")
    print("")
if not config.getboolean("security", "verify"):
    print("WARNING: NOT VERIFYING SERVER'S AUTHENTICITY")
    print("")

# Check for arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--command", type=str, help="Get information about all or a command on the server. (Too see available commands, use the 'all' command.)")
args = parser.parse_args()

connection = norac.connection.Connection()
connection.init(config)

if args.command:
    data = ""
    if args.command != "all":
        data = args.command
    response = connection.send_request({ "command" : "commands", "meta" : [], "data" : data })
    print(response["data"])

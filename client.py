#!/usr/bin/env python
import sys
import ConfigParser
import os
import socket
import ssl
import argparse

import norac.connection
import norac.modules.module as module

DEFAULT_CONFIG_NAME="norac_default.cfg"
OVERRIDE_CONFIG_NAME="norac.cfg"

def print_response(response):
    print("Code: %d" % response["result_code"])
    print("Msg : %s" % response["result_msg"])
    print("Data: %s" % response["data"])

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


# Registers all modules the client supports.
connection = norac.connection.Connection()
connection.init(config)
module_handler = module.Handler(config, connection)
module_handler.create_modules()

# Check for arguments
parser = argparse.ArgumentParser()
mutually_exclusive = parser.add_mutually_exclusive_group()

modules = module_handler.get_modules()
for m in modules.values():
    mutually_exclusive.add_argument(m.get_shorthand(), m.get_longhand(), help=m.get_description(), type=m.handle)

args = parser.parse_args()

# The default action
if not len(sys.argv) > 1:
    modules["add_note"].handle("") 

#if args.command:
    #data = ""
    #if args.command != "all":
        #data = args.command
    #response = connection.send_request({ "command" : "commands", "meta" : [], "data" : data })
    #print_response(response)

#!/usr/bin/env python
import ConfigParser
import os
import socket
import ssl
import argparse

import norac.connection

DEFAULT_CONFIG_NAME="norac_default.cfg"
OVERRIDE_CONFIG_NAME="norac.cfg"

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
if not config.getboolean("security", "verify"):
    print("WARNING: NOT VERIFYING SERVER'S AUTHENTICITY")


connection = norac.connection.Connection()
connection.init(config)

response = connection.send_request({ "command" : "help", "meta" : [], "data" : "add_note" })
print(response["data"])

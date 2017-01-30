#!/bin/bash
ramdevice="/dev/ram0"
maxsize="50M"
ramstorage="RAMSTORAGE"
owner="nora"

if [ "$EUID" -ne 0 ]; then
    echo "Run as root."
    exit
fi

if [ ! -b "$ramdevice" ]; then
    echo $ramdevice
    echo "No RAM device exists."
    exit
fi

if [ ! -d "$ramstorage" ]; then
    exit
fi

mounted=$(mount | grep $ramdevice)
if [[ ! -z "${mounted// }" ]]; then
    umount $ramstorage
    dd if=/dev/urandom of=$ramdevice bs=$maxsize count=1 > /dev/null 2>&1
    echo "Storage torn down."
else
    echo "Storage not mounted."
fi

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
    mkdir $ramstorage
    echo "Created storage at $ramstorage"
fi

mounted=$(mount | grep $ramdevice)
if [[ -z "${mounted// }" ]]; then
    mkfs $ramdevice $maxsize > /dev/null 2>&1
    mount $ramdevice $ramstorage
    chown -R $owner:$owner $ramstorage
    chmod -R 700 $ramstorage
    echo "Storage setup."
else
    echo "Storage already mounted."
fi

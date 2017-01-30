# Nora Client
A terminal client for the NORA daemon. The NORA daemon is a central server for storing encrypted notes. The client uses ramdisk storage to prevent unencrypted data from being written to disk, and uses your favorite editor to update the contents of the file.

If your editor is crazy and creates backups in unpredictable locations, it's not my fault.

## Dependencies
Some smaller list of weird stuff

## Setup
Review the contents of everything, obviously. The "prepare.sh" script needs to 
run as a privileged user, as this is responsible for allocating a RAM disk device, mounting it, and then to properly tear it down.

The following steps should be performed:

### 1 - Create user account
Create an account which runs this application. The below is just an example.
```
useradd nora
...
```

### 2 - Update prepare.sh & teardown.sh
The files are located under "utils/"

Set the properties of the mounted RAM disk in the prepare.sh script. 
**Remember to update the user account, and perform both changes in both files.**
The following is an example:
```
ramdevice="/dev/ram0"
maxsize="50M"
ramstorage="RAMSTORAGE"
owner="nora"
```

Description of the different configurations:
* ramdevice: the ramdisk device to use
* maxsize: the maximum amount of available memory for the files
* ramstorage: the path to the target directory
* owner: the account which runs the client

### 3 - Permissions prepare.sh teardown.sh
Restrict the permissions to this file as strict as possible

Set root ownership:
```
chown root:root prepare.sh teardown.sh
```

Set permissions
```
chmod 700 prepare.sh teardown.sh
```

### 4 - Update sudoers 
The application needs to run the prepare.sh script, but it doesn't want to much privileges. One way is to update the sudoers file to the following example:

```
nora    ALL=(root) NOPASSWD:/<path_to_script>/prepare.sh
nora    ALL=(root) NOPASSWD:/<path_to_script>/teardown.sh
```

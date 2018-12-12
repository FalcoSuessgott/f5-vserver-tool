# f5-vserver-tool

# Dependencies

# Installation

# Usage
Utitlity written in Python for displaying virtual server and their respective pools and nodes. Can be used for changing the default pool for a virtual server. Also it prints out the current sync status of a specified device group. 

# Getting Started

### Dependencies 

[Python F5 SDK](https://github.com/F5Networks/f5-common-python/releases)
(>= 3.0.20)

[Python F5 icontrol-rest](https://github.com/F5Networks/f5-icontrol-rest-python)
(>= 1.3.9)

### Installing
```
git clone https://github.com/FalcoSuessgott/f5-vserver-tool.git 
```

or get the rpm under releases
```
sudo yum localinstall f5-server-tool
```

### Prerequisites
In order to use this tool you will need to provide the config file some information

```
cat /etc/loadbalancer.conf
# [AUTH]
# User      = Name of the user that is used to connect to the loadbalancer
# Password	= Password of the loadbalancer that is used while authenticate to the loadbalancer

[AUTH]
User		  = ""
Password	= ""

# [BASIC]
# DeviceGroup	  = Name of the Device Group to which the loadbalancer are assigned to
# LoadbalancerX	= FQDN of respective the loadbalancer

[BASIC]
DeviceGroup	  = ""
Loadbalancer	= ""
```

### Usage
If filled in successful you can use it with

```
f5-server-tool  [--config / -c ] CONFIGFILE [--user/ -u ] USER [--password / -p] Password [--devicegroup / -dg] DEVICEGROUP [--loadbalancer / -lb ] LOADBALANCER [--list] [--list-vserver] [--list-pools] [--list-nodes] [
```
Note:
 - If no configfile [--config / -c] is specified when the tool is called. The default config under /etc/loadbalancer.conf is used.
 - Parameters that are passed as option ( [--user/ --password / --loadbalancer / --devicegroup ] overwrite the information in the default config or the config file specified with [--config / -c].
 - If no user is specified in the config file, the current user is used for authentication and may be prompted for the password.

### Example

List virtual server and their assigned pools and the nodes of the respective pool

```
[user@host ~]$ loadbalancer -l
Password:
Virtual Server               Pool               Pool member
xxx-8010                     xxxx               1.1.1.1:100, 1.1.1.1:200
xxx-8020                     xxxx               1.1.1.1:100, 1.1.1.1:200
....
```


List virtual server
```
[user@host ~]$ loadbalancer --list-vserver
Password:
vserver-1
vserver-2
vserver-3
....
```
>>>>>>> c2e3778e483dd36db9d6ad234cd136a7f1c1ef3e

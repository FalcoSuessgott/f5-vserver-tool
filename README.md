# f5-vserver-tool

Small python tool for displaying virtual server and their respective pools and nodes, changing the pool of virtual server. Also it can be used to print out the current sync status of a device group. Please see the Note under Usage to understand config file usage and commandline option passing
## Getting Started

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
 - Config parameters that are passed as options ( [--user/ --password / --loadbalancer / --devicegroup ] overwrite the information in the default config or the specified config file ([--config / -c]).
 - If no user is specified in the config file, the current user will be used and prompted for authentication

### Example

#### Print out information 
List virtual server and their assigned pools and their respective nodes

```
[user@host ~]$ loadbalancer -l
Password:
Virtual Server               Pool               Pool member
xxx-8010                     xxxx               1.1.1.1:100, 1.1.1.1:200
xxx-8020                     xxxx               1.1.1.1:100, 1.1.1.1:200
....
```


List all virtual server
```
[user@host ~]$ loadbalancer --list-vserver
Password:
vserver-1
vserver-2
vserver-3
....
```

List all pools
```
[user@host ~]$ loadbalancer --list-pools
Password:
pool-1
pool-2
pool-3
....
```

List all nodes
```
[user@host ~]$ loadbalancer --list-nodes
Password:
node1
node2
node3
....
```

List all virtual server
```
[user@host ~]$ loadbalancer --list-vserver
Password:
vserver-1
vserver-2
vserver-3
....
```

Print out sync-status 
```
[user@host ~]$ loadbalancer --show-sync-status
Password: 
deviceGroup is currently In Sync

```

#### Configure vserver and their assigend pool

Set assign pool1 to vserver1
```
[user@host ~]$ loadbalancer -s vserver1 pool1
Password: 
Changing pool for "vserver1" to "pool1"
Synchronizing new configuration to device group "devicegroup"
devicegroup is In Sync
```

#### Print out sample config file
```
[user@host ~]$ loadbalancer -m
[AUTH]
user		= "user"
password	= "password"

[BASIC]
devicegroup	= "devicegroup"
loadbalancer	= "fqdn"
```

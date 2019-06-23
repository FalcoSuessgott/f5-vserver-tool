# f5-vserver-tool
Functions:
* list all virtual server its pools and their members of a device group
* print out the sync status of a device group
* assign pools to specfied virtual server
## Getting Started

### Dependencies 

[Python F5 SDK](https://github.com/F5Networks/f5-common-python/releases)
(>= 3.0.20)

[Python F5 icontrol-rest](https://github.com/F5Networks/f5-icontrol-rest-python)
(>= 1.3.9)

### Installation
```
git clone https://github.com/FalcoSuessgott/f5-vserver-tool.git 
```

or download the rpm under [releases](https://github.com/FalcoSuessgott/f5-vserver-tool/releases) and then run:
```
sudo yum localinstall f5-server-tool
```

### Prerequisites
In order to use this tool you either need to set up `/etc/loadbalancer.conf`:

**/etc/loadbalancer.conf**
```
[AUTH]
user      = 
password	 = 

[BASIC]
devicegroup	 =
loadbalancer = 
```

Or you pass the parameter as commandline arguments.
You can override the configfile parameter with commandline arguments.

**Note:**
 * If no configfile parameter is specified, default location `/etc/loadbalancer.conf` is used.
 * If no `user` and `password` values are specified in the configfile or passes as commandline arguments, the current user will be used and prompted for authentication.

### Example

#### Print out information 
List virtual server and their assigned pools and their respective nodes

```
[user@host ~]$ f5-vserver-tool.py -l
Password:
Virtual Server               Pool               Pool member
xxx-8010                     xxxx               1.1.1.1:100, 1.1.1.1:200
xxx-8020                     xxxx               1.1.1.1:100, 1.1.1.1:200
....
```


List all virtual server
```
[user@host ~]$ f5-vserver-tool.py --list-vserver
Password:
vserver-1
vserver-2
vserver-3
....
```

List all pools
```
[user@host ~]$ f5-vserver-tool.py --list-pools
Password:
pool-1
pool-2
pool-3
....
```

List all nodes
```
[user@host ~]$ f5-vserver-tool.py --list-nodes
Password:
node1
node2
node3
....
```

List all virtual server
```
[user@host ~]$ f5-vserver-tool.py --list-vserver
Password:
vserver-1
vserver-2
vserver-3
....
```

Print out sync-status 
```
[user@host ~]$ f5-vserver-tool.py --show-sync-status
Password: 
deviceGroup is currently In Sync

```

#### Configure vserver and their assigend pool
```
[user@host ~]$ f5-vserver-tool.py --set vserver1 pool1
Password: 
Changing pool for "vserver1" to "pool1"
Synchronizing new configuration to device group "devicegroup"
devicegroup is In Sync
```

#### Print out sample config file
```
[user@host ~]$ f5-vserver-tool.py -m
[AUTH]
user		= "user"
password	= "password"

[BASIC]
devicegroup	= "devicegroup"
loadbalancer	= "fqdn"
```

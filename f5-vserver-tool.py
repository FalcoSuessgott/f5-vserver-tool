#!/usr/bin/python
#
# Commandline utility to execute specific operations on biotronik f5 loadbalancer
#
# Autor: Tom Morelly
# Date:  11.10.2018
#

import os
import sys
import ConfigParser
import argparse
import getpass
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from f5.bigip import ManagementRoot
from terminaltables import AsciiTable

SAMPLE_CONFIG = """
[AUTH]
user		= "user"
password	= "password"

[BASIC]
devicegroup	= "devicegroup"
loadbalancer	= "fqdn"
"""

def parseArgs():
	""" Argument parser """
        parser = argparse.ArgumentParser(description="Lists vserver, pool and nodes of from specified f5 big ip systems.\n"
					+ "Assigns a default pool to a specified vserver.\n"
					+ "Prints out the current sync-status of a device group.\n"
					+ "If no configfile is passed, /etc/loadbalancer.conf is used.\n"
					+ "Commandline options overwrite configfile options.\n"
					+ "If options are not present, either as configfile or as commandline option"
					+ " the programm will exit.",formatter_class=argparse.RawTextHelpFormatter)


	# C
        parser.add_argument("-c", "--config", dest="config",action="store",
			help="Path to configfile. Use -m to print sample config file."
			+ "\nDefault location is /etc/loadbalancer.conf.")

	# LIST ALL
	parser.add_argument("-l", "--list", dest="listAll", action="store_true",
			help="List all virtual server and their respective pools and nodes.")

	# LIST VS
        parser.add_argument("--list-vserver", dest="listVirtualServer", action="store_true",
                        help="List all virtual server.")

       # LIST POOLS
        parser.add_argument("--list-pools", dest="listPools", action="store_true",
                        help="List all pools.")

	# LIST NODES
        parser.add_argument("--list-nodes", dest="listNodes", action="store_true",
                        help="List all nodes.")

	# SET
        parser.add_argument("-s", "--set", dest="setPool", action="store",nargs=2,
                        help="Assigns a default pool to specified vserver"
			+ "\nUsage: --set VSERVER POOL")

	# SHOW SYNC STATUS
	parser.add_argument("--show-sync-status", dest="syncStatus", action="store_true",
			help="Prints the sync-status of the specified device group.")

	# USER
        parser.add_argument("-u", "--user", dest="user", action="store",
                        help="User used for authentication.\n"
			+ "This option overwrites config file options.\n"
			+ "If not specified the current logged on user will be prompted for password.")

	# Password
        parser.add_argument("-p", "--password", dest="password", action="store",
			help="Password used for authentication.\n"
			+ "This option overwrites config file options.\n"
			+ "If not specified, user will be prompted for password.")

	# loadbalancer
	parser.add_argument("-lb", "--loadbalancer", dest="loadbalancer", action="store",
                        help="Loadbalancer system.\n"
			+ "This option overwrites config file options.")

	# device group
	parser.add_argument("-dg", "--devicegroup", dest="devicegroup", action="store",
                        help="Device group of the specified loadbalancer.\n"
			+ "This option overwrites config file options.")

	# print config
        parser.add_argument("-m", "--print-config", dest="printconfig", action="store_true",
                        help="Print a sample full configuration file d exit.")

        parser = parser.parse_args()

	# No arguments
	if len(sys.argv) == 1:
        	print("No arguments were specified. Please use loadbalaner -h option for more information")
            	sys.exit(1)

	###############
	# USAGE OPTiONS
	###############

	global user
	global password
	global loadbalancer
	global devicegroup

	# sample config
	if parser.printconfig:
		print SAMPLE_CONFIG
		sys.exit(0)

	# configfile
	if parser.config:
		configfile = parser.config

		if not os.path.isfile(configfile):
                        print "File \"%s\" does not exist." %(configfile)
                        print "Exiting."
                        sys.exit(1)
                else:
			readConfig(configHandler(configfile))
	else:
		configfile = "/etc/loadbalancer.conf"

		if not os.path.isfile(configfile):
                        print "File \"%s\" does not exist." %(configfile)
                        print "Exiting."
                        sys.exit(1)
                else:
                	readConfig(configHandler(configfile))

	# user
	if not userValue:
		if parser.user is None:
			user = os.environ['USER']
		else:
			user = parser.user
	else:
		user = userValue

        # password
        if not passwordValue:
		password = getpass.getpass()
	else:
		password = passwordValue

	# loadbalancer
	if not loadbalancerValue:
		if parser.loadbalancer is None:
			print "Loadbalancer is not specified in configfile or has not been passed as option.\nExiting."
			sys.exit(1)
		else:
			loadbalancer = parser.loadbalancer
	else:
		loadbalancer = loadbalancerValue

	# devicegroup
        if not devicegroupValue:
		if parser.devicegroup is None:
                	print "Devicegroup is not specified in configfile or has not been passed as option.\nExiting."
                        sys.exit(1)
                else:
                        devicegroup = parser.devicegroup
	else:
		devicegroup = devicegroupValue

	# Auth
	auth(loadbalancer, user, password)

	################
	# ACTION OPTIONS
	################

	# list all
	if parser.listAll:
		listAll()

	# list pools
	if parser.listPools:
		listPools()

	# list nodes
	if parser.listNodes:
		listNodes()

	# list vs
	if parser.listVirtualServer:
		listVirtualServer()
	# set
	if parser.setPool:
		setPool(parser.setPool)

	# show sync
	if parser.syncStatus:
		showSyncStatus()

def readConfig(config):
	""" Reads configfile """
	try:
		global userValue
		userValue       = config.get('AUTH', 'user')
		userValue	= userValue.strip('"')

		global passwordValue
                passwordValue   = config.get('AUTH', 'password')
		passwordValue 	= passwordValue.strip('"')

		global loadbalancerValue
                loadbalancerValue = config.get('BASIC', 'loadbalancer')
		loadbalancerValue = loadbalancerValue.strip('"')

		global devicegroupValue
                devicegroupValue = config.get('BASIC', 'devicegroup')
		devicegroupValue = devicegroupValue.strip('"')

	except Exception as e:
		print "Error while reading configfile.\nExiting."
                sys.exit(1)

def auth(loadbalancer, user, password):
        """ Authenticates on the specified loadbalancer"""
	try:
		global mgmt
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		mgmt 		= ManagementRoot(loadbalancer, user, password)

        except Exception as e:
                print "Error while connecting. Please check permissions, configfile and network connectivity."
                print "Exiting"
                sys.exit(1)


def configHandler(configfile):
        """ Accesses and parsed the values in the specified configfile """
        config = ConfigParser.RawConfigParser()
        config.read(configfile)
        return config

def setPool(options):
	""" Sets a specific pool to a specified vserver"""
	try:
		poolExists       	= mgmt.tm.ltm.pools.pool.exists(name=options[1])
                virtualServerExists     = mgmt.tm.ltm.virtuals.virtual.exists(name=options[0])

		if not virtualServerExists:
			print "\"%s\" does not exist.\nExiting." %(options[0])
			sys.exit(1)
		if not poolExists:
                        print "\"%s\" does not exist.\nExiting." %(options[1])
                        sys.exit(1)

		print "Changing pool for \"%s\" to \"%s\"" %(options[0], options[1])
		virtualServer           = mgmt.tm.ltm.virtuals.virtual.load(name=options[0])
		params = {'pool': options[1]}
		virtualServer.update(**params)
		forceSync()
	        sys.exit(0)
        except Exception as e:
                print e
                sys.exit(1)


	print "\n[ "  + virtualServerName.upper() + " ]"
	print "Current pool: \"" + virtualServer.pool + "\""

	if virtualServer.pool == operationPoolName:
		print "Nothing to do. Exiting."
		sys.exit(1)
	else:
		print "Switching to: \"" + operationPoolName + "\""
		params = {'pool': operationPoolName}
		virtualServer.update(**params)
		tmpCurrentPool     = virtualServer.pool
		print "New Pool: \"" + virtualServer.pool + "\""
		forceSync(mgmt)
		sys.exit(0)

def listAll():
	try:
		pools = mgmt.tm.ltm.pools.get_collection()
		virtualServer = mgmt.tm.ltm.virtuals.get_collection()

		print "{:40}\t{:40}".format("Virtual Server","Pool"),"Pool member"

		for vs in virtualServer:
			try:
				vsName	= getVSName(vs)
				poolName= vs.raw['pool'].replace("/Common/","")
				for pool in pools:
					if pool.name == poolName:
						member = getMemberOfPool(pool)
						print "{:40}\t{:40}".format(getVSName(vs),poolName),", ".join([str(m) for m in member])
			except KeyError as e:
				pass

		sys.exit(0)
	except Exception as e:
		print e
		sys.exit(1)

def getMemberOfPool(pool):
	""" returns the member of a given pool """
	result = []
	for member in pool.members_s.get_collection():
		result.append(member.name)
	return result

def getPoolName(pool):
	""" returns the name of a given pool """
	return pool.name

def getVSName(vs):
	""" returns the name of a given virtual server """
	return vs.name

def listPools():
	""" Get a list of all pools and their members """
	try:
		pools = mgmt.tm.ltm.pools.get_collection()

		for pool in pools:
			 print pool.name
                sys.exit(0)
        except Exception as e:
                print e
                sys.exit(1)

def listVirtualServer():
	""" Get a list of all virtual servers and their details """
	try:
		virtualServer = mgmt.tm.ltm.virtuals.get_collection()

		for vs in virtualServer:
			print vs.name
                sys.exit(0)
        except Exception as e:
                print e
                sys.exit(1)

def listNodes():
        """ Get a list of all nodes and their ports """
        try:
                pools = mgmt.tm.ltm.pools.get_collection()

		for pool in pools:
                        for member in pool.members_s.get_collection():
                                print member.name
                sys.exit(0)
        except Exception as e:
                print e
                sys.exit(1)

def showSyncStatus():
	""" prints sync status of device group on terminal """

        mgmt.tm.cm.exec_cmd('run', utilCmdArgs='config-sync to-group ' + str(devicegroup))
        syncStatus = mgmt.tm.cm.sync_status.load(name=devicegroup)

	print devicegroup, "is currently", syncStatus.raw['entries']['https://localhost/mgmt/tm/cm/sync-status/0']['nestedStats']['entries']['status']['description']

def forceSync():
	""" Synchronizes both BigIP-systems """
	print "Synchronizing new configuration to device group \"%s\"" %(devicegroup)
	mgmt.tm.cm.exec_cmd('run', utilCmdArgs='config-sync to-group ' + str(devicegroup))
	syncStatus = mgmt.tm.cm.sync_status.load(name=devicegroup)
	print devicegroup, "is", syncStatus.raw['entries']['https://localhost/mgmt/tm/cm/sync-status/0']['nestedStats']['entries']['status']['description']

def systemExit(code, msgs=None):
    """ Exit with a code and optional message(s). Saved a few lines of code.  """
    if msgs:
        if type(msgs) not in [type([]), type(())]:
            msgs = (msgs, )
        for msg in msgs:
            sys.stderr.write(str(msg) + '\n')
	sys.exit(code)

def main():
	try:
	        args = parseArgs()
   	except KeyboardInterrupt:
        	systemExit(0, "\nUser interrupted process.")

if __name__ == '__main__':
    try:
        sys.exit(abs(main() or 0))
    except KeyboardInterrupt:
	systemExit(0, "\nUser interrupted process.")


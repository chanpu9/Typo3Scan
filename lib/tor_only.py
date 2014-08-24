import socket
import urllib2
import os, sys
import re
from colorama import Fore
try:
	import socks
except:
	print "The module 'SocksiPy' is not installed."
	if sys.platform.startswith('linux'):
		"Please install it with: sudo apt-get install python-socksipy"
	else:
		"You can download it from http://socksipy.sourceforge.net/"
	sys.exit(-2)

def start_daemon():
	if sys.platform.startswith('linux'):
		os.system('service tor start')
	elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
		print "Please make sure TOR is running..."
	else:
		print "You are using", sys.platform, ", which is not supported (yet)."
		sys.exit(-2)
	
# Using TOR for all connections
def connect(port):
	print "\nChecking connection..."
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", port, True)
	socket.socket = socks.socksocket
	try:
		url = urllib2.Request('https://check.torproject.org/')
		torcheck = urllib2.urlopen(url)
		response = torcheck.read()
		torcheck.close()
	except Exception, e:
		print e
		print Fore.RED + "Failed to connect through TOR!" + Fore.RESET
		print "Please make sure your configuration is right!\n"
		sys.exit(-2)
	try:
		regex = re.compile('Congratulations. This browser is configured to use Tor.')
		searchVersion = regex.search(response)
		version = searchVersion.groups()
		print Fore.GREEN + "Connection to TOR established" + Fore.RESET
		regex = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
		searchIP = regex.search(response)
		IP = searchIP.groups()[0]
		print "Your IP is: ", IP
	except:
		print "It seems like TOR is not used.\nAborting...\n"
		sys.exit(-2)

def stop():
	print "\n"
	if sys.platform.startswith('linux'):
		os.system('service tor stop')
	elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
		print "You can close TOR now..."

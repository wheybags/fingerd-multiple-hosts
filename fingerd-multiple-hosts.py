#!/usr/bin/env python

import sys
from socket import gethostname
import subprocess

# List of hosts to include apart from localhost
hosts = [
"spoon",
"prime",
"imhotep"
]


biggestusername = 5
biggestname = 4
biggestpts = 3

# Return input string, justified and padded within num chars
# Positive num for left, and negative for right justify
def justify(num, string):
	if num > 0:
		return string + " " * (num - len(string))
	else:
		return " " * (- num - len(string)) + string

# Takes a line from finger and inserts hostname, also checks avious sizes for justification
def fixline(line, hostname):
	userlist = line.split()
	
	# Make sure user has a real name
	if userlist[1][:3] != "pts" and userlist[1][0] != "*" and userlist[1][:3] != "tty":
		# Gather real name into userlist[1]
		while userlist[2][:3] != "pts" and userlist[2][0] != "*" and userlist[2][:3]!="tty":
			userlist[1] += " " + userlist.pop(2)
	

		
	# If user has no real name, fill it with a blank
	else:
		userlist.insert(1, " ")
	
	# Make sure there is an idle time, if not, fill with blank 
	try:
		float(userlist[3][0])	
	except:
		userlist.insert(3, " ")
	
	# Insert hostname
	userlist.insert(2, hostname)

	# Indent if no *
	if userlist[3][0] != "*":
		userlist[3] = " " + userlist[3]
		#print "asdasdas"
	
	# Rest is checking sizes for justification
	global biggestusername
	if len(userlist[0]) > biggestusername:
		biggestusername = len(userlist[0])
	global biggestname
	if len(userlist[1]) > biggestname:
		biggestname = len(userlist[1])
	global biggestpts
	if len(userlist[3]) > biggestpts:
		biggestpts = len(userlist[3])

	return userlist



if __name__ == "__main__":
	user = sys.stdin.readline()[:-2]

	# Build command to run
	cmd = ["/usr/bin/finger"]
	if user != "":
		cmd.append(user)

	p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	# If fingering a specific user, do that and quit
	if user != "":
		for line in p.stdout.readlines():
			print line,


	else:
		p.stdout.readline() # Advance by one line - to avoid the status line
		
		users = []

		hostname = gethostname().split(".")[0]
		
		# For padding
		biggesthostname = len(hostname)
		if biggesthostname < 4:
			biggesthostname = 4 # 4 because the "Host" heading is 4 chars long
		
		# Loop through all lines from localhost
		for line in p.stdout.readlines():
			users.append(fixline(line, hostname))
		
		# Finger all extra hosts, and loop through them
		for host in hosts:
			if len(host) > biggesthostname:
				biggesthostname = len(host)

			p = subprocess.Popen(["/usr/bin/finger", "@"+host], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			p.stdout.readline()
			for line in p.stdout.readlines():
				users.append(fixline(line, host))

			
		users.sort()
		

		# Print Headings
		print justify(biggestusername, "Login"),
		print justify(biggestname,     "Name"),
		print justify(biggesthostname, "Host"),
		print justify(biggestpts + 1,  "Tty"),
		print justify(5,               "Idle"),
		print justify(12,              "Login Time"),
		print                          "Location"
		
		# And finally, print all users
		for x in users:
			print justify(biggestusername, x[0]),
			print justify(biggestname,     x[1]),
			print justify(biggesthostname, x[2]),
			print justify(biggestpts,      x[3]),
			print justify(-5,              x[4]),
			print                          x[5] ,
			print justify(-2,              x[6]),
			print                          x[7],
			try:
				print                  x[8]
			except:
				print

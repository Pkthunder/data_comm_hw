import socket # module for all socket calls
import sys # module used for "argv" functionality
import re # regex module for input validation
from os import path # helper module for modifying path and file names

	
def fromTerminal():
	""" 
	helper function responsible for passing command
	line arguments to the client function
	"""

	# default values (for testing)
	if len(sys.argv) == 2 and sys.argv[1] == "default":
		runClient("127.0.1.1", "8888", "GET", "/")
		return

	# list of regex to validate input
	valid_regex = [
		re.compile(r'^[a-zA-Z0-9.//_-]{4,}$'),	# host
		re.compile(r'^[0-9]{2,5}$'),			# port_number
		re.compile(r'^(GET|PUT)$'),				# GET|PUT
		re.compile(r'^[a-zA-Z0-9.//_-]+$')		# file_name
	]

	# example of how to call this script
	example_call = "Example:\tpython myclient.py www.google.com 80 GET /"

	try:
		# Checks all inputs are entered (4 args and myclient.py itself)
		if len(sys.argv) != 5:
			raise RuntimeError("too few args\n%s" % example_call)

		# Check all argv inputs (1 to 5 exclusive)
		for i in range(1,5):
			if not valid_regex[i-1].match(sys.argv[i]):
				raise RuntimeError("'%s': invalid format" % sys.argv[i])
	
	except RuntimeError as e:
		print e.message
		return

	# on valid input
	runClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

def runClient(dest, port, gp, file):
	""" 
	A simple HTTP 1.0 client 
	"""

	CRLF = "\r\n\r\n"
	# tuple containing GET|PUT and file_name
	# path.basename returns the file name of a path
	params = (gp, file) # default value
	if gp == "PUT" and file != "/":
		# PUT requests only need the file name
		params = (gp, path.basename(file))

	# Real HTTP-1.0 ASCII-based request string
	# example: GET /path/to/file/index.html HTTP/1.0
	request = "%s %s HTTP/1.0" % params
	request += CRLF

	# create an INET, STREAMing socket
	s = socket.socket(
		socket.AF_INET, socket.SOCK_STREAM)

	# set a timeout for the requests
	# the connection() method is subject to the timeout settings
	s.settimeout(0.80)

	# a flag to instruct the kernel to reuse the local socket
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# establish TCP connection with dest at port 80 (HTTP default)
	print "\nEstablishing connection..."
	s.connect((dest, int(port)))

	# send request message in HTTP format
	print "Sending request %s" % request
	s.sendall(request)

	# response from the server
	response = ""

	# run GET or PUT specific code
	if gp == "GET":

		# place all segments into a string buffer
		# then save the segments into memory
		# until EOF is reached
		temp = s.recv(1024)
		while temp:
			response += temp
			temp = s.recv(1024)
		print "Response received"

	elif gp == "PUT":
		# receive "ACK" from server before sending file
		put_response = s.recv(1024)

		# on Successful "ACK" message
		if put_response == "Connection established. Send file":

			# open the file to send to server via file stream
			with open(file, "r") as f:
				# read in the file until EOF
				# load initial segment of file
				# then loop until EOF is reached
				raw_data = f.read(1024)
				while raw_data:
					# send the file data to the server
					# as the client reads in the file
					print "Sending data..."
					s.send(raw_data)
					raw_data = f.read(1024)

			# sends EOF to the server
			s.shutdown(socket.SHUT_WR)
			print "File was sent"

			# store the HTTP response from the server
			response = s.recv(1024)
			print "Response received"

		else:
			print "Connection was broken"
			s.shutdown(1)
			s.close()
			return

	else:
		print "Error - Bad HTTP Verb"
		s.shutdown(1)
		s.close()
		return


	# shutdown TCP 
	print "Closing the connection...\n"
	#s.shutdown(1)
	s.close()

	print "\t**Reponse**\n"
	print response.strip()
	#print 'Raw Data Received', repr(response)
	print "\n*************************************\n"


# defaults to terminal args, for calls
# outside terminal, import runClient directly
fromTerminal()

"""
More info can be found at
https://docs.python.org/2/library/socket.html
"""
import socket # module for all socket calls
import sys # module used for "argv" functionality
import re # regex module for input validation

	
def fromTerminal():
	""" 
	helper function responsible for passing command
	line arguments to the client function
	"""

	# list of regex to validate input
	valid_regex = [
		re.compile(r'^[a-zA-Z0-9.//_-]{4,}$'),	# host
		re.compile(r'^[0-9]{2,5}$'),			# port_number
		re.compile(r'^(GET|PUT)$'),				# GET|PUT
		re.compile(r'^[a-zA-Z0-9.//_-]+$')		# file_name
	]

	# example of how to call this script
	example_call = "python myclient.py www.google.com 80 GET /"

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
	How to call from command line:
	python myclient.py host|url port_number GET|PUT file_name
	"""

	CRLF = "\r\n\r\n"
	#dest, port_num = sys.argv[1], sys.argv[2]
	# tuple containing GET|PUT and file_name
	params = (gp, file)

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

	# a flag to instruct the kernel to reuse a local socket
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# establish TCP connection with dest at port 80 (HTTP default)
	print "\nEstablishing connection..."
	s.connect((dest, int(port)))

	# send request message in HTTP format
	print "Sending request %s" % request
	s.sendall(request)

	# receives response, string buffer size should be a low
	# power of 2 for best results
	response = s.recv(8192)
	print "Response received"

	# shutdown TCP 
	print "Closing the connection...\n"
	s.shutdown(1)
	s.close()

	print "\t**Reponse**\n"
	print response
	print 'Receive', repr(response)


# defaults to terminal args, for calls
# outside terminal, import runClient directly
fromTerminal()

"""
More info can be found at
https://docs.python.org/2/library/socket.html
"""
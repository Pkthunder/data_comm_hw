"""
based off the following examples
https://docs.python.org/2/howto/sockets.html
"""

import socket # module for all socket calls
import sys # module used for "argv" functionality
import re # regex module for input validation
from os import path # helper module for modifying path and file names

def fromTerminal():
	""" 
	helper function responsible for passing command
	line arguments to the server function
	"""	

	example_call = "python myserver.py 8888"

	try:
		# checks input
		if len(sys.argv) != 2 or (not re.compile(r'^[0-9]{2,5}$').match(sys.argv[1])):

			raise RuntimeError("bad port number\ntry %s" % example_call)

	except RuntimeError as e:
		print e.message
		return

	# on valid input
	runServer(int(sys.argv[1]))


def runServer(port):

	# returns the IP address of the machine
	HOST = socket.gethostbyname(socket.gethostname())

	# Port number to listen on
	PORT = port

	# create an INET, STREAMing socket
	server_socket = socket.socket(
		socket.AF_INET, socket.SOCK_STREAM)

	# a flag to instruct the kernel to reuse a local socket
	server_socket.setsockopt(
		socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# creates a server socket to listen on port <PORT arg>
	# first arg: could also be 'localhost' or '127.0.0.1'
	# socket.gethostname() returns visible outside address
	# passing '' has the socket reachable by any address the machine has
	server_socket.bind((HOST, PORT))

	# listens to the binded IP and port
	# will queue 5 requests before refusing connections
	server_socket.listen(5)
	print "\nSimple HTTP server now running at %s on port %s...\n" % (HOST, PORT)

	listening = True

	while listening:
		# accept connection, creates new TCP on a new port and thread
		(client_connection, client_address) = server_socket.accept()
		
		# received request from client
		# buffer size is small because simple requests are also small
		request = client_connection.recv(1024)
		print request.rstrip()

		# parse out the file name from the request
		# removes a leading "/" if it exists
		start = 4
		end = request.find("HTTP")-1
		# only removes "/" if a word exists after
		# "/" results in "/" and "/abc" results in "abc"
		if request[4] == "/" and request[5] != " ":
			start = 5
		# a slice of the request equal to the file's name
		file_name = request[start:end]
		print "requested file name: %s" % file_name

		# process statement
		if request[:3] == "GET":
			http_response = ""
			
			# get the file to serve to the client
			if file_name == "/": # for testing purposes
				http_response = """\
HTTP/1.0 200 OK

Hello World!
"""
				# send the response to the client
				client_connection.send(http_response)

			# if the file exists, serve it to client
			elif path.exists(file_name) and path.isfile(file_name):
				try:
					# read in the requested file to send back to client
					with open(file_name, "r") as f:
						# first send the http response
						http_response = "HTTP/1.0 200 OK\n\n"
						# send the response to the client
						client_connection.send(http_response)

						# read and send file data to client
						file_data = f.read(1024)
						while file_data:
							print "Sending data..."
							client_connection.send(file_data)
							file_data = f.read(1024)

				# if an error occurs while reading in the file, return 500
				except:
					http_response = "HTTP/1.0 500 INTERNAL SERVER ERROR"
					# send the response to the client
					client_connection.sendall(http_response)

			else:
				http_response = "HTTP/1.0 404 NOT FOUND"
				# send the response to the client
				client_connection.sendall(http_response)

		elif request[:3] == "PUT":
			
			# send "ACK" to the client, signaling the
			# client to send the file to the server
			http_response = "Connection established. Send file"
			client_connection.sendall(http_response)

			# open a file stream with the corresponding file name
			try:
				with open("putdata/" + file_name, "w+") as f:
					# writes data to the file as it is received
					raw_data = client_connection.recv(1024)
					while raw_data:
						print "Receiving data..."
						f.write(raw_data)
						raw_data = client_connection.recv(1024)

			# if an error occurs while save the file to the server, return 500
			except:
				http_response = "HTTP/1.0 500 INTERNAL SERVER ERROR"
				# send the response to the client
				client_connection.sendall(http_response)

			# if no error occurs, return 200 OK
			else:
				# Once file is transferred completely
				http_response = "HTTP/1.0 200 OK FILE CREATED"
				client_connection.sendall(http_response)

		else:
			print "Error - Bad HTTP Verb"
			return

		# shutdown and close the connection
		print "Closing connection..."
		client_connection.shutdown(1)
		client_connection.close()
		print "\n*************************************\n"

		# prevents continuous loop
		# breaks loop after first request
		#listening = False

fromTerminal()
import subprocess
import socket
from time import sleep
from multiprocessing import Process
import os
import signal


def runTest(test_cmd, test_index):

	test_complete = False
	retry_count = 3
	test = None

	def sigint_handler(*args):
		print "SIGINT received!"
		test_complete = True
		print "exiting test..."

	signal.signal(signal.SIGINT,
		sigint_handler)

	print "\nRunning Test %s...\n" % str(test_index)

	while not test_complete:
		try:
			print "Executing test..."
			# test = subprocess.check_output(test_cmd, shell=True)
			cmd_list = test_cmd.split(" ")
			fileno = len(cmd_list)-1
			# print cmd_list
			with open(cmd_list[fileno], "wb") as f:
				test = subprocess.Popen(cmd_list, stdout=f,
					stderr=subprocess.STDOUT, shell=True)
				print test
			break

		except socket.timeout as e:
			# catch socket timeout and try again
			retry_count = retry_count - 1

			if retry_count == 0:
				print "Test %s failed...\n" % test_index
				return

		else:
			# wait for a few seconds before continuing
			sleep(3.0)
			return

	# A successful test only means the test ran without errors
	# it does NOT mean the request itself was successful
	print "Test %s was successful!\n" % str(test_index)


# Runs tests asynchronously, so the server script doesn't block
# Creates a new Process per test. 
server_port = 8888

p1 = Process(target=runTest, 
	args=("python myclient.py www.google.com 80 GET / > log/client_test.log", 1))

p2 = Process(target=runTest,
	args=("python myserver.py %s > log/server_test.log" % server_port, 2))

p3 = Process(target=runTest,
	args=("python myclient.py 127.0.1.1 %s GET / >> log/client_test.log" % server_port, 3))

p4 = Process(target=runTest,
	args=("python myclient.py 127.0.1.1 %s PUT temp.txt >> log/client_test.log" % server_port, 4))

p5 = Process(target=runTest,
	args=("python myclient.py 127.0.1.1 %s GET temp.txt >> log/client_test.log" % server_port, 5))

p1.start() # www.google 80 GET /
sleep(1.5)
p2.start() # run server on port 8888
sleep(1.5)
p3.start() # 127.0.1.1 8888 GET /
sleep(1.5)
p4.start() # 127.0.1.1 8888 PUT temp.txt
sleep(1.5)
p5.start() # 127.0.1.1 8888 GET putdata/temp.txt

# join all processes to main thread
p1.join()
p2.join()
p3.join()
p4.join()
p5.join()

sleep(2.0)
subprocess.call("reset", shell=True)
sleep(1.0)
print "test.py has completed running!"

# sleep(1.5)
# print "Killing server..."
# print p2.pid, p2.is_alive()
# os.kill(p2.pid, signal.SIGINT)
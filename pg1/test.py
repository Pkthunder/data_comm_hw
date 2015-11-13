import subprocess
import socket
from time import sleep
from multiprocessing import Process


def runTest(test_cmd, test_index):

	test_complete = False
	retry_count = 3
	test = None

	print "\nRunning Test %s...\n" % str(test_index)

	while not test_complete:
		try:
			print "Executing test..."
			test = subprocess.check_output(test_cmd, shell=True)
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
	args=("python myclient.py 127.0.1.1 8888 GET / >> log/client_test.log", 3))

p1.start()
sleep(1.5)
p2.start()
sleep(1.5)
p3.start()
p1.join()
p2.join(5.0)
p3.join()
# Data Communications
#### Programming Assignments | UMass Lowell | Professor Guanling Chen

Programming Assignment 1 is contained within the pg1 directory

Code was developed and tested on a Ubuntu system running Python version 2.7.6

No additional modules are needed

## How To Install
```bash
# clone this github repo
git clone https://github.com/Pkthunder/data_comm_hw.git
# enter the cloned project directory
cd data_comm_hw
# enter the pg1 directory
cd pg1
# now you can execute the scripts (as explained below)
# ensure your system is running Python 2.7.6
which python
python --version # tested on version 2.7.6
```

## How To Run

To run the client and server, open 2 terminal windows

##### In window 1:
```bash
# python myclient.py <url> <port> <(GET|PUT)> <file_name>
# For example:
# retreives the Google homepage
python myclient.py www.google.com 80 GET /
# Or:
# sends text file to local server (myserver.py)
python 127.0.1.1 8888 PUT temp.txt
```
  
##### In window 2:
```bash
# python myserver.py <port>
# For example:
python myserver.py 8888
```

Obviously requests targetted at the local server (`myserver.py`) must match the port number that `myserver.py` was ran on. I had a few problems with the client when sending requests to the Internet with a bad connection. If any errors persist simply run `killall python` then try re-running the python command(s).

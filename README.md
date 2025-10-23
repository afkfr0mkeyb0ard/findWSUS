# Description
Python scripts to find WSUS servers on a network without any credentials.

Clone and install the requirements:
```
$ git clone https://github.com/afkfr0mkeyb0ard/findWSUS.git
$ cd findWSUS
$ python3 -m pip install -r requirements.txt

# Scan the web services to find WSUS
$ python3 scanWSUS.py TARGET
```

## 1. Using web exposure
WSUS may expose Web page to deploy updates. By scanning the Web ports we can find out the WSUS IP (port 8530/8531 by default):

    $ python3 scanWSUS.py TARGET

**TARGET** *can be a single IP, a file containing IP or a network*

#### Scanning a single IP:
    $ python3 scanWSUS.py 10.10.10.1

#### Scanning a list of IP (one per line):
    $ python3 scanWSUS.py FILE

#### Scanning a network:
    $ python3 scanWSUS.py 10.10.10.0/24

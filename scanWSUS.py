import socket
import sys
import requests
from ipaddress import IPv4Network, ip_address
from concurrent.futures import ThreadPoolExecutor, as_completed

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if len(sys.argv) <= 1 :
    print("[!] No parameter found. Aborting.")
    print("[!] Please provide an IP range or file.")
    print("[EXAMPLE] > python3 scanWSUS.py 192.168.0.0/24")
    print("[EXAMPLE] > python3 scanWSUS.py 192.168.0.123")
    print("[EXAMPLE] > python3 scanWSUS.py IPS.txt")
    sys.exit()
arg = sys.argv[1]
print("*** Scanning range " + arg + " ***")
ports = [8530,8531]

########################################################################
MAX_WORKERS = 20    # MAX CONCURRENT REQUESTS
HTTP_TIMEOUT = 2    # SECONDS BEFORE TIMEOUT FOR HTTP REQUESTS
VERBOSE = False     # False : TO DISPLAY ONLY OPEN PORTS
########################################################################

WSUS_IP = []

def scan_ip(ip_address):
    if VERBOSE :
        print(f"-> Scanning {ip_address}")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            if port == 8530:
                url = f"http://{ip_address}:{port}/ClientWebService/client.asmx"
            else:
                url = f"https://{ip_address}:{port}/ClientWebService/client.asmx"
            try:
                response = requests.get(url,verify=False,timeout=HTTP_TIMEOUT)
                if response.status_code == 200 :
                    url_proof = url.replace("/ClientWebService/client.asmx","/ClientWebService/client222.asmx")
                    response_proof = requests.get(url_proof,verify=False,timeout=HTTP_TIMEOUT)
                    if response_proof.status_code == 404:
                        print(f"-----> WSUS FOUND on http://{ip_address}:{port}/ClientWebService/client.asmx !!")
                        WSUS_IP.append(url)
                    else:
                    	print(f"-> {ip_address} --> Port {port} open but no WSUS found")
                else :
                    print(f"-> {ip_address} --> Port {port} open but no WSUS found")
            except requests.exceptions.RequestException as e:
                #print(e) TO DISPLAY THE ERROR
                pass
        else:
            pass
        sock.close()

try:
    ip_address = ip_address(arg)
    scan_ip(str(ip_address))
except ValueError:
    try:
        network = IPv4Network(arg)
        ip_addresses = [str(ip) for ip in network]
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = executor.map(scan_ip, ip_addresses)
            for result in results:
                pass
    except ValueError:
        try:
            with open(arg) as f:
                ip_addresses = [line.strip() for line in f]
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    results = executor.map(scan_ip, ip_addresses)
        except FileNotFoundError:
            print(f"{arg} is not a valid IP address, network in CIDR notation, or file")
            print("Aborting...")
            sys.exit()

print("\n")
print("--------------------------------")
print("----------- RESULT -------------")
print("--------------------------------")


if len(WSUS_IP) == 0 :
    print("No WSUS found")
else :
    for url in WSUS_IP :
        print(url)

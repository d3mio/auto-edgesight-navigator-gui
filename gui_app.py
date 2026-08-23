import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from threading import Thread
import json

class EdgeDeviceTelemetry:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.cpu = random.randint(1, 100)
        self.memory = random.randint(1, 100)
        self.network = random.randint(1, 100)
        self.temp = random.randint(20, 80)
        self.status = 'OK'
        self.last_update = time.strftime('%H:%M:%S')

    def update(self):
        self.cpu = random.randint(1, 100)
        self.memory = random.randint(1, 100)
        self.network = random.randint(1, 100)
        self.temp = random.randint(20, 80)
        if self.cpu > 90 or self.memory > 90 or self.network < 10:
            self.status = 'CRITICAL'
        elif self.cpu > 70 or self.memory > 70:
            self.status = 'WARNING'
        else:
            self.status = 'OK'
        self.last_update = time.strftime('%H:%M:%S')

class EdgeSightNavigator:
    def __init__(self, root):
        self.root = root
        self.root.title('EdgeSight Navigator')
        self.root.geometry('1200x800')
        self.root.configure(bg='#1e1e1e')
        
        # Create sample devices
        self.devices = [
            EdgeDeviceTelemetry('Edge-Device-001', 'New York'),
            EdgeDeviceTelemetry('Edge-Device-002', 'London'),
            EdgeDeviceTelemetry('Edge-Device-003', 'Tokyo'),
            EdgeDeviceTelemetry('Edge-Device-004', 'Sydney'),
            EdgeDeviceTelemetry('Edge-Device-005', 'Berlin')
        ]
        
        # Configure dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='#1e1e1e', foreground='white', fieldbackground='#2d2d2d')
        style.map('TCombobox', fieldbackground=[('readonly', '#2d2d2d')])
        
        # Main container
        self.main_frame = ttk.Frame(root, padding='10')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.title_label = ttk.Label(self.header_frame, text='EdgeSight Navigator', font=('Helvetica', 16, 'bold'))
        self.title_label.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(self.header_frame, text='Status: Active', foreground='green')
        self.status_label.pack(side=tk.RIGHT)
        
        # Dashboard
        self.dashboard_frame = ttk.Frame(self.main_frame)
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Device list
        self.device_list_frame = ttk.LabelFrame(self.dashboard_frame, text='Edge Devices', padding='10')
        self.device_list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.device_tree = ttk.Treeview(self.device_list_frame, columns=('name', 'location', 'status'), show='headings')
        self.device_tree.heading('name', text='Device Name')
        self.device_tree.heading('location', text='Location')
        self.device_tree.heading('status', text='Status')
        self.device_tree.column('name', width=150)
        self.device_tree.column('location', width=100)
        self.device_tree.column('status', width=80)
        self.device_tree.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Metrics
        self.metrics_frame = ttk.Frame(self.dashboard_frame)
        self.metrics_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Metrics tabs
        self.metrics_notebook = ttk.Notebook(self.metrics_frame)
        self.metrics_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Telemetry tab
        self.telemetry_frame = ttk.Frame(self.metrics_notebook)
        self.metrics_notebook.add(self.telemetry_frame, text='Telemetry')
        
        # CPU
        self.cpu_frame = ttk.LabelFrame(self.telemetry_frame, text='CPU Usage (%)')
        self.cpu_frame.pack(fill=tk.X, padx=5, pady=5)
        self.cpu_var = tk.IntVar()
        self.cpu_bar = ttk.Progressbar(self.cpu_frame, orient=tk.HORIZONTAL, length=200, variable=self.cpu_var)
        self.cpu_bar.pack(fill=tk.X, padx=5, pady=5)
        self.cpu_label = ttk.Label(self.cpu_frame, text='0%')
        self.cpu_label.pack()
        
        # Memory
        self.memory_frame = ttk.LabelFrame(self.telemetry_frame, text='Memory Usage (%)')
        self.memory_frame.pack(fill=tk.X, padx=5, pady=5)
        self.memory_var = tk.IntVar()
        self.memory_bar = ttk.Progressbar(self.memory_frame, orient=tk.HORIZONTAL, length=200, variable=self.memory_var)
        self.memory_bar.pack(fill=tk.X, padx=5, pady=5)
        self.memory_label = ttk.Label(self.memory_frame, text='0%')
        self.memory_label.pack()
        
        # Network
        self.network_frame = ttk.LabelFrame(self.telemetry_frame, text='Network Bandwidth (%)')
        self.network_frame.pack(fill=tk.X, padx=5, pady=5)
        self.network_var = tk.IntVar()
        self.network_bar = ttk.Progressbar(self.network_frame, orient=tk.HORIZONTAL, length=200, variable=self.network_var)
        self.network_bar.pack(fill=tk.X, padx=5, pady=5)
        self.network_label = ttk.Label(self.network_frame, text='0%')
        self.network_label.pack()
        
        # Temperature
        self.temp_frame = ttk.LabelFrame(self.telemetry_frame, text='Temperature (°C)')
        self.temp_frame.pack(fill=tk.X, padx=5, pady=5)
        self.temp_var = tk.IntVar()
        self.temp_bar = ttk.Progressbar(self.temp_frame, orient=tk.HORIZONTAL, length=200, variable=self.temp_var)
        self.temp_bar.pack(fill=tk.X, padx=5, pady=5)
        self.temp_label = ttk.Label(self.temp_frame, text='0°C')
        self.temp_label.pack()
        
        # Alerts tab
        self.alerts_frame = ttk.Frame(self.metrics_notebook)
        self.metrics_notebook.add(self.alerts_frame, text='Alerts')
        
        self.alerts_tree = ttk.Treeview(self.alerts_frame, columns=('time', 'device', 'message', 'severity'), show='headings')
        self.alerts_tree.heading('time', text='Time')
        self.alerts_tree.heading('device', text='Device')
        self.alerts_tree.heading('message', text='Message')
        self.alerts_tree.heading('severity', text='Severity')
        self.alerts_tree.column('time', width=100)
        self.alerts_tree.column('device', width=120)
        self.alerts_tree.column('message', width=250)
        self.alerts_tree.column('severity', width=80)
        self.alerts_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Footer
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.last_update_label = ttk.Label(self.footer_frame, text='Last update: Never')
        self.last_update_label.pack(side=tk.LEFT)
        
        self.refresh_btn = ttk.Button(self.footer_frame, text='Refresh', command=self.refresh_data)
        self.refresh_btn.pack(side=tk.RIGHT)
        
        # Initialize UI
        self.populate_device_list()
        self.refresh_data()
        
        # Start background updates
        self.running = True
        self.update_thread = Thread(target=self.background_updates, daemon=True)
        self.update_thread.start()
        
        # Bind device selection
        self.device_tree.bind('<<TreeviewSelect>>', self.on_device_select)
        
        # Handle window close
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
    
    def populate_device_list(self):
        for device in self.devices:
            status_color = 'green' if device.status == 'OK' else 'orange' if device.status == 'WARNING' else 'red'
            self.device_tree.insert('', tk.END, values=(device.name, device.location, device.status), tags=(status_color,))
        
        self.device_tree.tag_configure('green', foreground='green')
        self.device_tree.tag_configure('orange', foreground='orange')
        self.device_tree.tag_configure('red', foreground='red')
    
    def refresh_data(self):
        for device in self.devices:
            device.update()
        
        self.update_device_list()
        self.last_update_label.config(text=f'Last update: {time.strftime("%H:%M:%S")}')
        
        # Select first device if none selected
        if not self.device_tree.selection():
            self.device_tree.selection_set(self.device_tree.get_children()[0])
            self.on_device_select(None)
    
    def update_device_list(self):
        for i, device in enumerate(self.devices):
            item = self.device_tree.get_children()[i]
            status_color = 'green' if device.status == 'OK' else 'orange' if device.status == 'WARNING' else 'red'
            self.device_tree.item(item, values=(device.name, device.location, device.status), tags=(status_color,))
    
    def on_device_select(self, event):
        selected = self.device_tree.selection()
        if not selected:
            return
        
        item = selected[0]
        idx = self.device_tree.index(item)
        device = self.devices[idx]
        
        # Update telemetry displays
        self.cpu_var.set(device.cpu)
        self.cpu_label.config(text=f'{device.cpu}%')
        self.cpu_bar.configure(style='green.Horizontal.TProgressbar' if device.cpu < 70 else 
                              'orange.Horizontal.TProgressbar' if device.cpu < 90 else 
                              'red.Horizontal.TProgressbar')
        
        self.memory_var.set(device.memory)
        self.memory_label.config(text=f'{device.memory}%')
        self.memory_bar.configure(style='green.Horizontal.TProgressbar' if device.memory < 70 else 
                                 'orange.Horizontal.TProgressbar' if device.memory < 90 else 
                                 'red.Horizontal.TProgressbar')
        
        self.network_var.set(device.network)
        self.network_label.config(text=f'{device.network}%')
        self.network_bar.configure(style='green.Horizontal.TProgressbar' if device.network > 30 else 
                                  'orange.Horizontal.TProgressbar' if device.network > 10 else 
                                  'red.Horizontal.TProgressbar')
        
        self.temp_var.set(device.temp)
        self.temp_label.config(text=f'{device.temp}°C')
        self.temp_bar.configure(style='green.Horizontal.TProgressbar' if device.temp < 60 else 
                               'orange.Horizontal.TProgressbar' if device.temp < 75 else 
                               'red.Horizontal.TProgressbar')
        
        # Check for alerts
        if device.status != 'OK':
            self.add_alert(device)
    
    def add_alert(self, device):
        # Check if alert already exists
        for item in self.alerts_tree.get_children():
            if self.alerts_tree.item(item, 'values')[1] == device.name and \
               self.alerts_tree.item(item, 'values')[3] == device.status:
                return
        
        # Add new alert
        message = f"High {'CPU' if device.cpu > 90 else 'Memory' if device.memory > 90 else 'Network' if device.network < 10 else 'Temperature'} usage"
        self.alerts_tree.insert('', 0, values=(device.last_update, device.name, message, device.status))
        
        if device.status == 'CRITICAL':
            self.root.bell()  # System alert sound
            messagebox.showwarning('Critical Alert', f'{device.name} is in critical state!')
    
    def background_updates(self):
        while self.running:
            time.sleep(5)
            self.root.after(0, self.refresh_data)
    
    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = EdgeSightNavigator(root)
    
    # Configure progress bar styles
    style = ttk.Style()
    style.configure('green.Horizontal.TProgressbar', background='green')
    style.configure('orange.Horizontal.TProgressbar', background='orange')
    style.configure('red.Horizontal.TProgressbar', background='red')
    
    root.mainloop()
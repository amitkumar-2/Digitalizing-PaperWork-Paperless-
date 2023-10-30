import tkinter as tk
import subprocess
import time
import psutil

# URL to be opened automatically
url = "https://example.com"

# Function to open the URL in the default web browser
def open_url():
    subprocess.Popen(["python", "-m", "webbrowser", "-t", url])

# Function to check if the web browser is running
def is_browser_running():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "chrome" in process.info['name'].lower():  # Change "chrome" to the browser you are using
            return True
    return False

# Create a Tkinter window
root = tk.Tk()
root.title("URL Opener")

# Start the web browser
open_url()

# Check if the browser is running and close the app if it's not
def check_browser_status():
    if not is_browser_running():
        root.destroy()
    else:
        root.after(1000, check_browser_status)  # Check every second

# Start checking the browser status
check_browser_status()

# Run the Tkinter main loop
root.mainloop()

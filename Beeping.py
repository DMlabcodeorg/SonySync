import csv
import os
import time
from datetime import datetime
import winsound
import argparse
import tkinter as tk
from tkinter import filedialog

def beep_and_log(frequency, duration, directory_path):
    # Generate beep
    winsound.Beep(frequency, int(duration * 1000))  # duration is in sec, so multiply by 100 to convert to ms

    # Get current timestamp
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Slicing to get milliseconds

    # Check if directory exists, if not create it
    os.makedirs(directory_path, exist_ok=True)

    # Define the path of the log file
    log_path = os.path.join(directory_path, 'tone_log.csv')

    # Check if 'tone_log.csv' exists in the specified directory, if not create it and write headers
    if not os.path.exists(log_path):
        with open(log_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Frequency (Hz)', 'Duration (sec)'])  # Column headers

    # Append to 'tone_log.csv'
    with open(log_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, frequency, duration])

    print(f"Beeped at frequency {frequency} and duration {duration} seconds. Logged at {current_time}")

def main():
    root = tk.Tk()
    root.title("Beep and Log")

    tk.Label(root, text="Frequency (Hz):").pack(pady=5)
    frequency_entry = tk.Entry(root)
    frequency_entry.insert(0, "11000")  # Default value is 11000 Hz
    frequency_entry.pack(pady=5)

    tk.Label(root, text="Duration (sec):").pack(pady=5)
    duration_entry = tk.Entry(root)
    duration_entry.insert(0, "2")  # Default value is 2 sec
    duration_entry.pack(pady=5)

    tk.Label(root, text="Log Directory:").pack(pady=5)
    log_dir_entry = tk.Entry(root)
    log_dir_entry.insert(0, ".")  # Default value is the same path
    log_dir_entry.pack(pady=5)

    def browse_directory():
        directory = filedialog.askdirectory()
        log_dir_entry.delete(0, tk.END)
        log_dir_entry.insert(0, directory)

    browse_button = tk.Button(root, text="Browse", command=browse_directory)
    browse_button.pack(pady=5)

    def start_beeping():
        frequency = int(frequency_entry.get())
        duration = float(duration_entry.get())
        log_dir = log_dir_entry.get()
        beep_and_log(frequency, duration, log_dir)

    start_button = tk.Button(root, text="Start Beeping", command=start_beeping)
    start_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()

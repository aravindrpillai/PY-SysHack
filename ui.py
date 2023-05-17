import tkinter as tk

def create_window():
    window = tk.Tk()

    window.title("Aravind R Pillai")
    window.geometry("300x200")

    label = tk.Label(window, text="Hello Kannappi.. With love Aravind")
    label.pack()

    button = tk.Button(window, text="Click Me")
    button.pack()

    window.mainloop()

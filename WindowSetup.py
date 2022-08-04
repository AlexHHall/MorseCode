import tkinter as tk
from tkinter import ttk
from settings import *
import time


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(window_title)
        self.geometry(window_size)


class KeyerPage(ttk.Frame):
    def __init__(self, options):
        super().__init__(options)
        master = self.master
        self.pressed = False
        self.time_of_press = 0
        self.time_of_release = 0
        self.dit_time = (60/wpm*50) / 1000
        print(self.dit_time)
        self.currently_typing_str = ""
        self.typed_str = ""

        master.bind("<KeyPress>", self.key_down)
        master.bind("<KeyRelease>", self.key_up)

        self.label = tk.Label(master, text=self.currently_typing_str)
        self.label.pack()

    def key_down(self, e):
        if e.keysym == "space":
            if not self.pressed:
                self.time_of_press = time.time()
                total_released_time = self.time_of_press - self.time_of_release
                if total_released_time < self.dit_time * 3:
                    self.currently_typing_str = self.currently_typing_str + " "
                else:
                    print(" / ")
            self.pressed = True
            print(self.currently_typing_str)
            self.label.config(text=self.currently_typing_str)

    def key_up(self, e):
        if e.keysym == "space":
            if self.pressed:
                self.time_of_release = time.time()
                total_pressed_time = self.time_of_release - self.time_of_press
                if total_pressed_time < self.dit_time:
                    self.currently_typing_str = self.currently_typing_str + "."
                else:
                    self.currently_typing_str = self.currently_typing_str + "-"
            print(self.currently_typing_str)
            self.label.config(text=self.currently_typing_str)

            self.pressed = False


import tkinter as tk
from tkinter import ttk
import random
from settings import *
import time

english_to_morse_list = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
                         'H': '....',
                         'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                         'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--',
                         'X': '-..-',
                         'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
                         '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '/', '!': '-.-.--'}


english = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
symbols = "!"


def english_to_morse(english):
    english_list = [i for i in english]
    for k, v in english_to_morse_list.items():
        for i in range(len(english_list)):
            if english_list[i] == k:
                english_list[i] = v
    return "".join(i + " " for i in english_list)


def morse_to_english(morse):
    morse_chars = morse.split(" ")
    for k, v in english_to_morse_list.items():
        for i in range(len(morse_chars)):
            if morse_chars[i] == v:
                morse_chars[i] = k
    return "".join(i for i in morse_chars)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(window_title)  # Using the Window Title from settings.py, set the title of the window
        self.geometry(window_size)  # Using the Window Size from settings.py, set the size of the window
        self.current_win = None

    def open_window(self, window, app):
        if window == "translator":
            self.clear_win()
            MenuBar(self, selected=window, main_app=app)
            self.current_win = TranslatorPage(self)
        elif window == "keyer":
            self.clear_win()
            MenuBar(self, selected=window, main_app=app)
            self.current_win = KeyerPage(self)
        elif window == "legend":
            self.clear_win()
            MenuBar(self, selected=window, main_app=app)
            self.current_win = LegendPage(self)
        elif window == "learn":
            self.clear_win()
            MenuBar(self, selected=window, main_app=app)
            self.current_win = LearnPage(self)

    def clear_win(self):
        for i in self.winfo_children():
            i.destroy()


class KeyerPage(ttk.Frame):
    def __init__(self, options):
        super().__init__(options)
        master = self.master
        self.pressed = False
        self.time_of_press = 0
        self.time_of_release = 0
        self.dit_time = (
                                60 / wpm * 50) / 1000  # Using the WPM from settings.py file, Work out the required time for one "dit"
        self.currently_typing_str = ""
        self.typed_str = ""

        master.bind("<KeyPress>", self.key_down)  # Bind the KeyPress event to the key_down function
        master.bind("<KeyRelease>", self.key_up)  # Bind the KeyRelease event to the key_up function

        self.morse_display_label = tk.Text(master, font=("Ariel", 25), state="disabled",
                                           height=5)  # Create a label that will display the text that is currently being typed
        self.morse_display_label.pack()

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_box)
        self.clear_button.pack()

        self.english_display_label = tk.Text(master, font=("Ariel", 25), state="disabled",
                                             height=5)  # Create a label that will display the text that is currently being typed
        self.english_display_label.pack()

    def key_down(self, e):
        if e.keysym == "space":
            if not self.pressed:
                self.time_of_press = time.time()
                total_released_time = self.time_of_press - self.time_of_release  # Get Total Time that the Space Bar was released for
                if self.dit_time * 3 < total_released_time < self.dit_time * 7:
                    self.currently_typing_str = self.currently_typing_str + " "  # If the Total Time was longer than the required amount for a space but less than for a "/" then add a space to the text
                elif total_released_time > self.dit_time * 3:
                    if not self.currently_typing_str == "":
                        self.currently_typing_str = self.currently_typing_str + " / "  # If the Total Time was long enough to add a "/" then add a "/" to the text
            self.pressed = True

            self.update_text_box()  # Update Label to Display Text

    def key_up(self, e):
        if e.keysym == "space":
            if self.pressed:
                self.time_of_release = time.time()
                total_pressed_time = self.time_of_release - self.time_of_press  # Get Total Time that the Space Bar was pressed for
                if total_pressed_time < self.dit_time:
                    self.currently_typing_str = self.currently_typing_str + "."  # If the Total Time was longer than the required amount for a "." but less than for a "-" then add a "." to the text
                elif total_pressed_time > self.dit_time:
                    self.currently_typing_str = self.currently_typing_str + "-"  # If the Total Time was long enough to add a "-" then add a "-" to the text
            self.pressed = False
            self.update_text_box()  # Update label to Display Text

    def clear_box(self):
        self.currently_typing_str = ""
        self.update_text_box()

    def update_text_box(self):
        self.morse_display_label.config(state="normal")
        self.morse_display_label.delete(1.0, tk.END)
        self.morse_display_label.insert(1.0, self.currently_typing_str)
        self.morse_display_label.config(state="disabled")
        self.english_display_label.config(state="normal")
        self.english_display_label.delete(1.0, tk.END)
        self.english_display_label.insert(1.0, morse_to_english(self.currently_typing_str))
        self.english_display_label.config(state="disabled")


class TranslatorPage(ttk.Frame):
    def __init__(self, options):
        super().__init__(options)
        master = self.master

        self.input_box = tk.Text(master)
        self.input_box.pack()

        self.translate_button = tk.Button(master, command=self.begin_translate)
        self.translate_button.pack()

        self.output_box = tk.Text(master, state="disabled")
        self.output_box.pack()

    def begin_translate(self):
        translate_type = None
        for i in english_to_morse_list.keys():
            if i in self.input_box.get(1.0, tk.END).upper():
                translate_type = "eng_to_morse"
        if not translate_type:
            if "-" in self.input_box.get(1.0, tk.END).upper() or "." in self.input_box.get(1.0, tk.END).upper():
                translate_type = "morse_to_eng"
            else:
                return "Invalid"
        if translate_type == 'eng_to_morse':
            translation = english_to_morse(self.input_box.get(1.0, tk.END).upper())
            self.output_box.config(state="normal")
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(1.0, translation)
            self.output_box.config(state="disabled")
        elif translate_type == 'morse_to_eng':
            translation = morse_to_english(self.input_box.get(1.0, tk.END).upper().strip())
            self.output_box.config(state="normal")
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(1.0, translation)
            self.output_box.config(state="disabled")


class LegendPage(ttk.Frame):
    def __init__(self, options):
        super().__init__(options)
        master = self.master
        i = 0
        for k, v in english_to_morse_list.items():
            if not k == " ":
                i += 25
                if i % 2 == 1:
                    tk.Label(master, text=f"{k}   :   {v}").place(x=300, y=i/2 + 15)
                else:
                    tk.Label(master, text=f"{k}   :   {v}").place(x=720, y=i/2)


class LearnPage(ttk.Frame):
    def __init__(self, options):
        super().__init__(options)
        master = self.master
        self.game_type = tk.StringVar(value='english-morse')
        self.english_to_morse = ttk.Radiobutton(master, variable=self.game_type, text="English To Morse Code", value="morse-english")
        self.morse_to_english = ttk.Radiobutton(master, variable=self.game_type, text="Morse Code to English", value="english-morse")
        self.morse_to_english.pack()
        self.english_to_morse.pack()
        self.letters_var, self.numbers_var, self.symbols_var = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()
        self.letters, self.numbers, self.symbols = ttk.Checkbutton(master, text="Letters", variable=self.letters_var), ttk.Checkbutton(master, text="Numbers", variable=self.numbers_var), ttk.Checkbutton(master, text="Symbols", variable=self.symbols_var)
        self.letters_var.set(True)
        self.numbers_var.set(True)
        self.letters.pack()
        self.numbers.pack()
        self.symbols.pack()
        self.start_button = ttk.Button(master, command=self.start_game, text="Start")
        self.start_button.pack()



    def start_game(self):
        print("Starting ")
        all_items_list = {}

        if self.letters_var.get():
            for k, v in english_to_morse_list.items():
                if k in english:
                    all_items_list[k] = v
        if self.numbers_var.get():
            for k, v in english_to_morse_list.items():
                if k in numbers:
                    all_items_list[k] = v
        if self.symbols_var.get():
            for k, v in english_to_morse_list.items():
                if k in symbols:
                    all_items_list[k] = v

        if all_items_list == {}:
            return

        if self.game_type.get() == "english-morse":
            question = random.choice([k for k, v in all_items_list.items()])
            print(question)
            answer = english_to_morse(question)
            print(answer)
        elif self.game_type.get() == "morse-english":
            print("M-E")

        self.letters.destroy()
        self.numbers.destroy()
        self.symbols.destroy()
        self.start_button.destroy()

        game_playing = False




class MenuBar(ttk.Frame):
    def __init__(self, options, selected, main_app):
        super().__init__(options)
        master = self.master
        self.master_app = main_app

        translator_page_button = tk.Button(self, text="Translator", command=self.open_translate)
        translator_page_button.pack(side="left")

        keyer_page_button = tk.Button(self, text="Keyer", command=self.open_keyer)
        keyer_page_button.pack(side="left")

        legend_page_button = tk.Button(self, text="Legend", command=self.open_legend)
        legend_page_button.pack(side="left")

        learn_page_button = tk.Button(self, text="Learn", command=self.open_learn)
        learn_page_button.pack(side="left")

        self.pack(side="top")

    def open_translate(self):
        self.master_app.open_window("translator", self.master_app)

    def open_keyer(self):
        self.master_app.open_window("keyer", self.master_app)

    def open_legend(self):
        self.master_app.open_window("legend", self.master_app)

    def open_learn(self):
        self.master_app.open_window("learn", self.master_app)

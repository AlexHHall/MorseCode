import tkinter as tk
from tkinter import ttk
import random
from settings import *
import time
import json

current_window = "Translator"


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(window_title)  # Using the Window Title from settings.py, set the title of the window
        self.geometry(window_size)  # Using the Window Size from settings.py, set the size of the window
        self.current_win = None
        self.config(bg=bg_color)  # Using the Window Size from settings.py, set the color of the background

    def open_window(self, window, app):
        global current_window
        if window == "translator":
            self.clear_win()
            MenuBar(self, selected=window, main_app=app)
            self.current_win = TranslatorPage(self)
            current_window = "Translator"
        elif window == "keyer":
            self.clear_win()
            MenuBar(self, selected=window, main_app=app)
            self.current_win = KeyerPage(self)
            current_window = "Keyer"
        elif window == "legend":
            self.clear_win()
            MenuBar(self, selected=window, main_app=app)
            self.current_win = LegendPage(self)
            current_window = "Legend"
        elif window == "learn":
            self.clear_win()
            MenuBar(self, selected=window, main_app=app)
            self.current_win = LearnPage(self)
            current_window = "Learn"

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
                60 / (wpm * 50))  # Using the WPM from settings.py file, Work out the required time for one "dit"
        self.currently_typing_str = ""
        self.typed_str = ""

        master.bind("<KeyPress>", self.key_down)  # Bind the KeyPress event to the key_down function
        master.bind("<KeyRelease>", self.key_up)  # Bind the KeyRelease event to the key_up function

        self.morse_display_label = tk.Text(master, font=full_font, state="disabled",
                                           height=input_height, width=input_width,
                                           bg=text_box_bg)  # Create a label that will display the text that is currently being typed
        self.morse_display_label.pack()

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_box, font=full_font, bg=text_box_bg)
        self.clear_button.pack()

        self.english_display_label = tk.Text(master, font=full_font, state="disabled",
                                             height=input_height, width=input_width,
                                             bg=text_box_bg)  # Create a label that will display the text that is currently being typed
        self.english_display_label.pack()

    def key_down(self, e):
        global current_window
        if current_window == "Keyer":
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
        if current_window == "Keyer":
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

        self.input_box = tk.Text(master, bg=text_box_bg, font=full_font, width=input_width, height=input_height)
        self.input_box.pack()

        self.translate_button = tk.Button(master, command=self.begin_translate, bg=text_box_bg, font=full_font,
                                          text="Translate")
        self.translate_button.pack()

        self.output_box = tk.Text(master, state="disabled", bg=text_box_bg, font=full_font, width=input_width,
                                  height=input_height)
        self.output_box.pack()

    def begin_translate(self):
        translate_type = None
        for i in english_to_morse_list.keys():
            if i == "." or i == "-" or i == " ":
                continue
            if i in self.input_box.get(1.0, tk.END).upper().strip():
                translate_type = "eng_to_morse"
        if not translate_type:
            if "-" in self.input_box.get(1.0, tk.END).upper().strip() or "." in self.input_box.get(1.0,
                                                                                                   tk.END).upper().strip():
                translate_type = "morse_to_eng"
            else:
                return "Invalid"
        if translate_type == 'eng_to_morse':
            translation = english_to_morse(self.input_box.get(1.0, tk.END).upper().strip())
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
        row_size = 11
        for k, v in english_to_morse_list.items():
            if i < row_size * 1:
                _ = tk.LabelFrame(master, height=1, width=1, bg=button_color, borderwidth=2)
                _.place(x=(i * row_size * 10) + 15, y=50)
                tk.Label(_, text=f"{k}", bg="#B0BFBE", borderwidth=2, width=1).grid(row=0, column=0)
                tk.Label(_, text=f"{v}", bg=button_color, width=5).grid(row=0, column=1)
            elif i < row_size * 2:
                _ = tk.LabelFrame(master, height=1, width=1, bg=button_color, borderwidth=2)
                _.place(x=((i - row_size * 1) * row_size * 10) + 15, y=100)
                tk.Label(_, text=f"{k}", bg="#B0BFBE", borderwidth=2, width=1).grid(row=0, column=0)
                tk.Label(_, text=f"{v}", bg=button_color, width=5).grid(row=0, column=1)
            elif i < row_size * 3:
                _ = tk.LabelFrame(master, height=1, width=1, bg=button_color, borderwidth=2)
                _.place(x=((i - row_size * 2) * row_size * 10) + 15, y=150)
                tk.Label(_, text=f"{k}", bg="#B0BFBE", borderwidth=2, width=1).grid(row=0, column=0)
                tk.Label(_, text=f"{v}", bg=button_color, width=5).grid(row=0, column=1)
            elif i < row_size * 4:
                _ = tk.LabelFrame(master, height=1, width=1, bg=button_color, borderwidth=2)
                _.place(x=((i - row_size * 3) * row_size * 10) + 15, y=200)
                tk.Label(_, text=f"{k}", bg="#B0BFBE", borderwidth=2, width=1).grid(row=0, column=0)
                tk.Label(_, text=f"{v}", bg=button_color, width=5).grid(row=0, column=1)
            i += 1


class LearnPage(ttk.Frame):
    def __init__(self, options):
        super().__init__(options)
        self.correct_label = None
        self.game_playing = False
        self.question = None
        self.start_new = False
        self.answer = None
        self.answer_box = None
        self.question_label = None
        master = self.master
        self.game_type = tk.StringVar(value='english-morse')
        self.english_to_morse = tk.Radiobutton(master, variable=self.game_type, text="English To Morse Code",
                                               value="morse-english", bg=bg_color, font=full_font, fg=button_color,
                                               highlightbackground=bg_color, selectcolor=bg_color,
                                               activebackground=button_color)
        self.morse_to_english = tk.Radiobutton(master, variable=self.game_type, text="Morse Code to English",
                                               value="english-morse", bg=bg_color, font=full_font, fg=button_color,
                                               highlightbackground=bg_color, selectcolor=bg_color,
                                               activebackground=button_color)
        self.morse_to_english.pack()
        self.english_to_morse.pack()
        self.letters_var, self.numbers_var, self.symbols_var = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()
        self.letters, self.numbers, self.symbols = tk.Checkbutton(master, text="Letters",
                                                                  variable=self.letters_var, bg=bg_color,
                                                                  font=full_font, activebackground=button_color,
                                                                  selectcolor=bg_color, highlightbackground=bg_color,
                                                                  fg=button_color), tk.Checkbutton(master,
                                                                                                   text="Numbers",
                                                                                                   variable=self.numbers_var,
                                                                                                   bg=bg_color,
                                                                                                   font=full_font,
                                                                                                   activebackground=button_color,
                                                                                                   selectcolor=bg_color,
                                                                                                   highlightbackground=bg_color,
                                                                                                   fg=button_color), tk.Checkbutton(
            master, text="Symbols", variable=self.symbols_var, bg=bg_color, font=full_font,
            activebackground=button_color, selectcolor=bg_color, highlightbackground=bg_color, fg=button_color)
        self.letters_var.set(True)
        self.numbers_var.set(True)
        self.letters.pack()
        self.numbers.pack()
        self.symbols.pack()
        self.start_button = tk.Button(master, command=self.start_game, text="Start", bg=button_color, font=full_font)
        self.start_button.pack()

    def start_game(self):
        print("Starting ")
        self.all_items_list = {}

        if self.letters_var.get():
            for k, v in english_to_morse_list.items():
                if k in english:
                    self.all_items_list[k] = v
        if self.numbers_var.get():
            for k, v in english_to_morse_list.items():
                if k in numbers:
                    self.all_items_list[k] = v
        if self.symbols_var.get():
            for k, v in english_to_morse_list.items():
                if k in symbols:
                    self.all_items_list[k] = v

        if self.all_items_list == {}:
            return

        self.letters.destroy()
        self.numbers.destroy()
        self.symbols.destroy()
        self.start_button.destroy()
        self.english_to_morse.destroy()
        self.morse_to_english.destroy()

        self.game_playing = True

        self.correct_label = tk.Label(self.master, text="", bg=bg_color, font=(font, 25, "bold"), fg=button_color)
        self.correct_label.pack()

        if self.game_type.get() == "english-morse":
            self.question = random.choice([k for k, v in self.all_items_list.items()])
            print(self.question)
            self.answer = english_to_morse(self.question)
            print(self.answer)
            self.question_label = tk.Label(self.master, text=self.question, font=(font, 25, "bold"), bg=bg_color,
                                           fg=button_color)
            self.question_label.pack()
            self.answer_box = tk.Entry(self.master, font=(font, 25), justify="center", bg=button_color)
            self.answer_box.bind("<KeyPress>", self.submit_answer)
            self.answer_box.pack()
            self.help_button = tk.Button(self.master, text="?", font=(font, 25, "bold"), bg=button_color, command=self.help)
            self.help_button.pack()
        elif self.game_type.get() == "morse-english":
            self.question = random.choice([v for k, v in self.all_items_list.items()])
            print(self.question)
            self.answer = morse_to_english(self.question)
            print(self.answer)
            self.question_label = tk.Label(self.master, text=self.question, font=(font, 25, "bold"), bg=bg_color,
                                           fg=button_color)
            self.question_label.pack()
            self.answer_box = tk.Entry(self.master, font=(font, 25), justify="center", bg=button_color)
            self.answer_box.bind("<KeyPress>", self.submit_answer)
            self.answer_box.pack()

    def submit_answer(self, e):
        if e.keysym == "Return":
            if not self.answer_box.get() == "".rstrip(" ") and not " " in self.answer_box.get():
                if self.game_type.get() == "morse-english":
                    if self.answer_box.get().strip().upper() == self.answer.strip().upper():
                        self.correct_label.config(text="Correct!")
                        self.new_letter()
                    else:
                        self.correct_label.config(text="Incorrect!")
                        self.new_letter()
                else:
                    if self.answer_box.get().strip().upper() == self.answer.strip().upper():
                        self.correct_label.config(text="Correct!")
                    else:
                        self.correct_label.config(text="Incorrect!")
                self.new_letter()
        # if not e.keysym == "." or not e.keysym == "-":
        # self.answer_box.delete(1.0, "end-1")

    def new_letter(self):
        if self.game_type.get() == "english-morse":
            self.question = random.choice([k for k, v in self.all_items_list.items()])
            self.answer = english_to_morse(self.question)
            self.answer_box.delete(0, tk.END)
            self.question_label.config(text=self.question)
        else:
            self.question = random.choice([v for k, v in self.all_items_list.items()])
            self.answer = morse_to_english(self.question)
            self.answer_box.delete(0, tk.END)
            self.question_label.config(text=self.question)

    def help(self):
        self.correct_label.config(text=f"{morse_to_english(self.answer.strip().upper())} is {self.answer.strip().upper()}")


class MenuBar(ttk.Frame):
    def __init__(self, options, selected, main_app):
        super().__init__(options)
        master = self.master
        self.master_app = main_app

        translator_page_button = tk.Button(self, text="Translator", command=self.open_translate, font=full_font,
                                           bg=button_color, fg=button_text_color)
        translator_page_button.pack(side="left")

        keyer_page_button = tk.Button(self, text="Keyer", command=self.open_keyer, font=full_font, bg=button_color,
                                      fg=button_text_color)
        keyer_page_button.pack(side="left")

        legend_page_button = tk.Button(self, text="Legend", command=self.open_legend, font=full_font, bg=button_color,
                                       fg=button_text_color)
        legend_page_button.pack(side="left")

        learn_page_button = tk.Button(self, text="Learn", command=self.open_learn, font=full_font, bg=button_color,
                                      fg=button_text_color)
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

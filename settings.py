# Window Settings
window_title = "Morse Code"
window_size = "1080x720"
bg_color = "#36454f"
button_color = "#CDD7D6"
font_size = 14
text_color = "#000000"
font = "Helvetica"
full_font = (font, font_size, "bold")
button_text_color = "#000000"
text_box_bg = "#CDD7D6"
input_height = 10
input_width = 60

# Morse Code Settings
wpm = 10
english_to_morse_list = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
                         'H': '....',
                         'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                         'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--',
                         'X': '-..-',
                         'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
                         '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '/', '!': '-.-.--'}


def english_to_morse(english_text):
    english_list = [i for i in english_text]
    for k, v in english_to_morse_list.items():
        for i in range(len(english_list)):
            if english_list[i] == k:
                english_list[i] = v
    return "".join(i + " " for i in english_list)


def morse_to_english(morse_code):
    morse_chars = morse_code.split(" ")
    for k, v in english_to_morse_list.items():
        for i in range(len(morse_chars)):
            if morse_chars[i] == v:
                morse_chars[i] = k
    return "".join(i for i in morse_chars)


english = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
symbols = "!"

import tkinter as tk
from tkinter import ttk, messagebox,PhotoImage
from googletrans import Translator, LANGUAGES
import os
import shutil
import string
import random
    

def encryption(text, shift):
    encrypted_text = ''
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                new_char = chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
            else:
                new_char = chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A'))
            encrypted_text += new_char
        else:
            encrypted_text += char
    return encrypted_text


def decryption(text, shift):
    decrypted_text = ''
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                new_char = chr((ord(char) - ord('a') - shift_amount) % 26 + ord('a'))
            else:
                new_char = chr((ord(char) - ord('A') - shift_amount) % 26 + ord('A'))
            decrypted_text += new_char
        else:
            decrypted_text += char
    return decrypted_text


def convert_length(value, from_unit, to_unit):
    length_units = {
        'meter': 1.0,
        'kilometer': 1000.0,
        'centimeter': 0.01,
        'millimeter': 0.001,
        'mile': 1609.34,
        'yard': 0.9144,
        'foot': 0.3048,
        'inch': 0.0254
    }
    if from_unit in length_units and to_unit in length_units:
        return value * length_units[from_unit] / length_units[to_unit]
    else:
        return None


def convert_weight(value, from_unit, to_unit):
    weight_units = {
        'gram': 1.0,
        'kilogram': 1000.0,
        'milligram': 0.001,
        'pound': 453.592,
        'ounce': 28.3495
    }
    if from_unit in weight_units and to_unit in weight_units:
        return value * weight_units[from_unit] / weight_units[to_unit]
    else:
        return None


def convert_temp(value, from_unit, to_unit):
    if from_unit == 'celsius':
        if to_unit == 'fahrenheit':
            return (value * 9/5) + 32
        elif to_unit == 'kelvin':
            return value + 273.15
    elif from_unit == 'fahrenheit':
        if to_unit == 'celsius':
            return (value - 32) * 5/9
        elif to_unit == 'kelvin':
            return (value - 32) * 5/9 + 273.15
    elif from_unit == 'kelvin':
        if to_unit == 'celsius':
            return value - 273.15
        elif to_unit == 'fahrenheit':
            return (value - 273.15) * 9/5 + 32
    return None


def file_organization(path):
    file_types = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx'],
        'videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
        'music': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
        'archives': ['.zip', '.rar', '.tar', '.gz', '.bz2', '.7z'],
        'scripts': ['.py', '.js', '.sh', '.bat', '.php', '.html', '.css'],
        'Minecraft': ['.mcpack','.mcworld'],
        'EXE':['.exe'],
        'Analyze':['.json']
        
    }
    files = os.listdir(path)
    for file in files:
        file_path=os.path.join(path,file)
        if os.path.isdir(file_path):
            continue
        filename, root = os.path.splitext(file)
        
        for category,extension in file_types.items():
            if root.lower() in extension:
                category_folder=os.path.join(path,category)
                if not os.path.exists(category_folder):
                    os.makedirs(category_folder)
                shutil.move(file_path,os.path.join(category_folder,file))
                break    

        
def pw_generator(length):
    all_characters = string.ascii_letters + string.punctuation + string.digits
    return ''.join(random.choice(all_characters) for _ in range(length))

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Multifunctional App")
        self.notebook = ttk.Notebook(root)
        self.create_encrypt_decrypt_tab()
        self.create_calculator_tab()
        self.create_converter_tab()
        self.create_translator_tab()
        self.create_file_org_tab()
        self.create_sudoku_solver_tab()
        self.create_dice_roll_tab()
        self.create_password_generator_tab()
        self.notebook.pack(expand=1, fill="both")
    
    def create_dice_roll_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Dice Roll')

        tk.Label(tab, text="Enter number of dice: ").pack(pady=5)
        self.num_of_roll = tk.IntVar()
        tk.Entry(tab, textvariable=self.num_of_roll).pack(pady=5)
        tk.Button(tab, text="Let's roll", command=self.roll_dice).pack(pady=5)
        self.dice_result_label = tk.Label(tab, text="", font=("Helvetica", 80))
        self.dice_result_label.pack(pady=5)

    def roll_dice(self):
        num_of_roll = self.num_of_roll.get()
        dice = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
        if num_of_roll > 0:
            result = [random.choice(dice) for _ in range(num_of_roll)]
            self.dice_result_label.config(text=' '.join(result))
        else:
            self.dice_result_label.config(text="Please enter a valid number of dice")

    def create_password_generator_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Password Generator')

        tk.Label(tab, text="Enter password length: ").pack(pady=5)
        self.pw_length = tk.IntVar()
        tk.Entry(tab, textvariable=self.pw_length).pack(pady=5)
        tk.Button(tab, text="Generate Password", command=self.password_generator).pack(pady=5)
        self.result_label = tk.Label(tab, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=5)

        tk.Button(tab, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=5)

    def password_generator(self):
        length = self.pw_length.get()
        password = pw_generator(length)
        self.result_label.config(text=password)
    def copy_to_clipboard(self):
        password = self.result_label.cget("text")
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()  # Keeps the clipboard content even after the app is closed




    def create_encrypt_decrypt_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Encrypt/Decrypt')

        self.enc_dec_text = tk.StringVar()
        self.enc_dec_result = tk.StringVar()

        tk.Label(tab, text="Enter Text:").pack(pady=5)
        tk.Entry(tab, textvariable=self.enc_dec_text).pack(pady=5)

        tk.Label(tab, text="Shift Value:").pack(pady=5)
        self.shift_value = tk.IntVar()
        tk.Entry(tab, textvariable=self.shift_value).pack(pady=5)

        tk.Button(tab, text="Encrypt", command=self.encrypt_text).pack(pady=5)
        tk.Button(tab, text="Decrypt", command=self.decrypt_text).pack(pady=5)

        tk.Label(tab, text="Result:").pack(pady=5)
        tk.Entry(tab, textvariable=self.enc_dec_result, state='readonly').pack(pady=5)

    def encrypt_text(self):
        text = self.enc_dec_text.get()
        shift = self.shift_value.get()
        self.enc_dec_result.set(encryption(text, shift))

    def decrypt_text(self):
        text = self.enc_dec_text.get()
        shift = self.shift_value.get()
        self.enc_dec_result.set(decryption(text, shift))

    def create_calculator_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Calculator')

        self.calc_entry = tk.StringVar()
        tk.Entry(tab, textvariable=self.calc_entry,width=25).pack(pady=20)

        buttons_frame = tk.Frame(tab)
        buttons_frame.pack()

        buttons = [
            ('7', 1, 1), ('8', 1, 2), ('9', 1, 3),
            ('4', 2, 1), ('5', 2, 2), ('6', 2, 3),
            ('1', 3, 1), ('2', 3, 2), ('3', 3, 3),
            ('0', 4, 2), ('.', 4, 1), ('+', 1, 4),
            ('-', 2, 4), ('*', 3, 4), ('/', 4, 4),
            ('=', 4, 3), ('C', 5, 4)
        ]

        for (text, row, col) in buttons:
            tk.Button(buttons_frame, text=text, command=lambda t=text: self.on_calc_button_click(t)).grid(row=row, column=col, ipadx=10, ipady=10)

        self.calc_result = tk.StringVar()
        tk.Entry(tab, textvariable=self.calc_result, state='readonly').pack(pady=5)

    def on_calc_button_click(self, char):
        if char == 'C':
            self.calc_entry.set('')
        elif char == '=':
            self.evaluate_calc()
        else:
            current_text = self.calc_entry.get()
            new_text = current_text + char
            self.calc_entry.set(new_text)

    def evaluate_calc(self):
        try:
            result = eval(self.calc_entry.get())
            self.calc_result.set(result)
        except Exception as e:
            self.calc_result.set(f"Error: {e}")

    def create_converter_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Converter')

        self.conv_value = tk.DoubleVar()
        self.conv_result = tk.StringVar()

        length_units = ['meter', 'kilometer', 'centimeter', 'millimeter', 'mile', 'yard', 'foot', 'inch']
        weight_units = ['gram', 'kilogram', 'milligram', 'pound', 'ounce']
        temp_units = ['celsius', 'fahrenheit', 'kelvin']

        self.unit_options = length_units + weight_units + temp_units

        tk.Label(tab, text="Value:").pack(pady=5)
        tk.Entry(tab, textvariable=self.conv_value).pack(pady=5)

        tk.Label(tab, text="From Unit:").pack(pady=5)
        self.conv_from = ttk.Combobox(tab, values=self.unit_options)
        self.conv_from.pack(pady=5)

        tk.Label(tab, text="To Unit:").pack(pady=5)
        self.conv_to = ttk.Combobox(tab, values=self.unit_options)
        self.conv_to.pack(pady=5)

        tk.Button(tab, text="Convert", command=self.convert_units).pack(pady=5)

        tk.Label(tab, text="Result:").pack(pady=5)
        tk.Entry(tab, textvariable=self.conv_result, state='readonly').pack(pady=5)

    def convert_units(self):
        value = self.conv_value.get()
        from_unit = self.conv_from.get().lower()
        to_unit = self.conv_to.get().lower()

        if from_unit in ['meter', 'kilometer', 'centimeter', 'millimeter', 'mile', 'yard', 'foot', 'inch']:
            result = convert_length(value, from_unit, to_unit)
        elif from_unit in ['gram', 'kilogram', 'milligram', 'pound', 'ounce']:
            result = convert_weight(value, from_unit, to_unit)
        elif from_unit in ['celsius', 'fahrenheit', 'kelvin']:
            result = convert_temp(value, from_unit, to_unit)
        else:
            result = None

        if result is not None:
            self.conv_result.set(f"{result} {to_unit}")
        else:
            self.conv_result.set("Invalid conversion units")

    def create_translator_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Translator')

        self.trans_text = tk.StringVar()
        self.trans_result = tk.StringVar()
        self.selected_lang = tk.StringVar()

        tk.Label(tab, text="Text to Translate:").pack(pady=5)
        tk.Entry(tab, textvariable=self.trans_text).pack(pady=5)

        tk.Label(tab, text="Destination Language:").pack(pady=5)

        languages = {
            'en': 'English',
            'es': 'Spanish',
            'zh-cn': 'Chinese (Simplified)',
            'zh-tw': 'Chinese (Traditional)',
            'hi': 'Hindi',
            'ar': 'Arabic',
            'bn': 'Bengali',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'de': 'German',
            'ko': 'Korean',
            'fr': 'French',
            'vi': 'Vietnamese',
            'it': 'Italian',
        }

        language_options = [f"{code} - {name}" for code, name in languages.items()]
        self.selected_lang.set(language_options[0])

        lang_menu = tk.OptionMenu(tab, self.selected_lang, *language_options)
        lang_menu.pack(pady=5)

        tk.Button(tab, text="Translate", command=self.translate_text).pack(pady=5)

        tk.Label(tab, text="Translated Text:").pack(pady=5)
        tk.Entry(tab, textvariable=self.trans_result, state='readonly').pack(pady=5)

    def translate_text(self):
        translator = Translator()
        text = self.trans_text.get()
        selected_lang = self.selected_lang.get()

        try:
            if not selected_lang:
                raise ValueError("Please select a language from the list")
            dest_lang = selected_lang.split(' - ')[0]
            translation = translator.translate(text, dest=dest_lang)
            self.trans_result.set(translation.text)
        except Exception as e:
            self.trans_result.set(f"Error: {e}")

    def create_file_org_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='File Organizer')

        self.file_org_path = tk.StringVar()

        tk.Label(tab, text="Directory Path:").pack(pady=5)
        tk.Entry(tab, textvariable=self.file_org_path).pack(pady=5)

        tk.Button(tab, text="Organize Files", command=self.organize_files).pack(pady=5)

    def organize_files(self):
        path = self.file_org_path.get()
        try:
            file_organization(path)
            messagebox.showinfo("Success", "Files organized successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error organizing files: {e}")

    def create_sudoku_solver_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Sudoku Solver')

        self.sudoku_board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.sudoku_entries = [[tk.Entry(tab, width=2) for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                entry = self.sudoku_entries[i][j]
                entry.grid(row=i, column=j, ipadx=5, ipady=5)
                if self.sudoku_board[i][j] != 0:
                    entry.insert(0, str(self.sudoku_board[i][j]))

        self.sudoku_button = tk.Button(tab, text="Solve", command=self.solve_sudoku)
        self.sudoku_button.grid(row=9, columnspan=9)

    def solve_sudoku(self):
        board = [[int(self.sudoku_entries[i][j].get() or 0) for j in range(9)] for i in range(9)]
        if self.solve(board):
            for i in range(9):
                for j in range(9):
                    self.sudoku_entries[i][j].delete(0, tk.END)
                    if board[i][j] != 0:
                        self.sudoku_entries[i][j].insert(0, str(board[i][j]))
        else:
            messagebox.showerror("Error", "Sudoku puzzle is unsolvable.")

    def solve(self, board):
        empty_pos = self.find_empty(board)
        if not empty_pos:
            return True
        else:
            row, col = empty_pos

        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0

        return False

    def is_valid(self, board, num, pos):
        # Check row
        for i in range(len(board[0])):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(board)):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

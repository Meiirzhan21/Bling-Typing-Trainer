import pygame
import tkinter as tk
import random
import time

# Слова с уровнями
words = {
    'easy': ["asdf", "ahha", "eee", "qwerty", "hjkl", "zxc", "uuu", "www", "aaa", "abcd", "hi", "bye", "tea", "ball", "key"],
    'medium': ["big", "mom", "dad", "tree", "boy", "girl", "joy", "ball", "hello", "print", "world", "shirt", "laptop", "farmer"],
    'hard': ["grandfather", "precision", "accuracy", "rural", "literally", "pharmacy", "tourist", "responsibility", "keyboard"]
}
used_words = {'easy': [], 'medium': [], 'hard': []} #для использованных слов

# Миксер для музыки
pygame.mixer.init()

def play_music(file_path): #функ. для музыки
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def generate_exercise(difficulty): #Выдать новое слово
    global words, used_words
    if not words[difficulty]:
        words[difficulty], used_words[difficulty] = used_words[difficulty], []
    word = random.choice(words[difficulty])
    used_words[difficulty].append(word)
    words[difficulty].remove(word)
    return word

root = tk.Tk()
root.geometry("600x300")  # Масштаб интерфейса
root.title("BlindTyping Trainer")

start_time = 0
record = float('inf')
is_active = False
correct_count = 0

# Текст для отображения счетчика
correct_counter_text = tk.StringVar(value="Correct in a row: 0")

current_word = tk.StringVar()
result_text = tk.StringVar(value="Start typing the word and press Enter. Select a level to begin.")
difficulty = tk.StringVar(value="easy")

# Настройки графического интерфейса
word_display = tk.Text(root, height=2, width=30, font=('Arial', 30), bd=0, bg=root.cget('bg'), relief='flat')
word_display.tag_configure('center', justify='center')  # Center text
word_display.tag_configure('correct', foreground='green', justify='center')
word_display.tag_configure('incorrect', foreground='red', justify='center')
word_display.pack(expand=True)
word_display.configure(state='disabled')

entry = tk.Entry(root, font=('Arial', 24), bd=3, width=30)
entry.pack(pady=(10, 20))

result_label = tk.Label(root, textvariable=result_text, font=('Arial', 14))
result_label.pack(pady=(10, 20))

# Метка для счетчика
correct_counter_label = tk.Label(root, textvariable=correct_counter_text, font=('Arial', 14))
correct_counter_label.pack()

def update_word_display(): #Для покраски в цвета букв слов
    user_input = entry.get()
    correct_word = current_word.get()
    word_display.configure(state='normal')
    word_display.delete('1.0', tk.END)
    for i, char in enumerate(correct_word):
        if i < len(user_input):
            if user_input[i] == char:
                word_display.insert(tk.END, char, 'correct')  # Правильные в зеленый
            else:
                word_display.insert(tk.END, char, 'incorrect')  # Неправильные в красный
        else:
            word_display.insert(tk.END, char, 'center')  # Остальный символы
    word_display.configure(state='disabled')

# читает отпускани клавиш
entry.bind('<KeyRelease>', lambda event: update_word_display())

def check_input(event=None):
    global record, is_active, correct_count
    if not is_active:
        return
    user_input = entry.get()
    if user_input == current_word.get():
        play_music('correct.mp3')
        end_time = time.time()
        elapsed_time = end_time - start_time
        record = min(record, elapsed_time)
        result_text.set(f"Correct! Time: {elapsed_time:.2f} sec. Best Time: {record:.2f} sec.")
        correct_count += 1
        correct_counter_text.set(f"Correct in a row: {correct_count}")  # Счетчик обновляется
        if correct_count >= 3:
            next_level_button.config(state=tk.NORMAL)  # Доступные баттон
            prev_level_button.config(state=tk.NORMAL)
        new_word()
    else:
        play_music('incorrect.mp3')
        result_text.set("Incorrect. Try again.")
        correct_count = 0
        correct_counter_text.set("Correct in a row: 0")
        next_level_button.config(state=tk.DISABLED)  # Недоступная кнопка
        prev_level_button.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

entry.bind('<Return>', check_input)

def start_timer(): #для таймера
    global start_time
    start_time = time.time()

def new_word(): #рандомное новое слово
    global is_active
    if not is_active:
        return
    word = generate_exercise(difficulty.get())
    current_word.set(word)
    entry.delete(0, tk.END)
    start_timer()
    update_word_display()

def next_level(): #для кнопки след.уровня
    global correct_count
    levels = ["easy", "medium", "hard"]
    current_index = levels.index(difficulty.get())
    if current_index < len(levels) - 1:
        select_level(levels[current_index + 1])
    else:
        result_text.set("Congratulations! You have completed all levels.")
    correct_count = 0
    correct_counter_text.set("Correct in a row: 0")
    next_level_button.config(state=tk.DISABLED)  # Выключение кнопки перехода на след.уровень
    prev_level_button.config(state=tk.NORMAL)  # А пред. уровень доступен

def prev_level():
    global correct_count
    levels = ["easy", "medium", "hard"]
    current_index = levels.index(difficulty.get())
    if current_index > 0:
        select_level(levels[current_index - 1])
    else:
        result_text.set("This is the easiest level.")
    correct_count = 0
    correct_counter_text.set("Correct in a row: 0")
    prev_level_button.config(state=tk.DISABLED)  # Пред.уровень недотсупен
    next_level_button.config(state=tk.NORMAL)  # След.уровень доступен

def select_level(level): #Уровень сложностей
    global is_active, correct_count
    difficulty.set(level)
    is_active = True
    correct_count = 0
    correct_counter_text.set("Correct in a row: 0")
    new_word()
    result_text.set("Type the word above and press Enter to continue.")
    # Кнопки выключены до 3 успешных
    next_level_button.config(state=tk.DISABLED)
    prev_level_button.config(state=tk.DISABLED)

# Кнопки управления
control_frame = tk.Frame(root)
control_frame.pack(pady=(5, 20))

prev_level_button = tk.Button(control_frame, text="Previous Level", command=prev_level, font=('Arial', 12), state=tk.DISABLED)
prev_level_button.grid(row=0, column=0, padx=5)

next_level_button = tk.Button(control_frame, text="Next Level", command=next_level, font=('Arial', 12), state=tk.DISABLED)
next_level_button.grid(row=0, column=1, padx=5)

def stop_game():
    global is_active
    is_active = False
    entry.delete(0, tk.END)
    entry.config(state='disabled')
    result_text.set("Game stopped. Press 'Restart' to start again.")
    correct_counter_text.set("Correct in a row: 0")
    next_level_button.config(state='disabled')
    prev_level_button.config(state='disabled')

def restart_game():
    global is_active, correct_count
    is_active = True
    correct_count = 0
    entry.config(state='normal')
    select_level("easy")

# Обновить команду для кнопок Остановки и перезапуска
tk.Button(control_frame, text="Stop", command=stop_game, font=('Arial', 12)).grid(row=0, column=2, padx=5)
tk.Button(control_frame, text="Restart", command=restart_game, font=('Arial', 12)).grid(row=0, column=3, padx=5)

select_level("easy")  # Задан легкий уровень

root.mainloop()

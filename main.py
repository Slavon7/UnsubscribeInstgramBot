import pyautogui
import time
import random
import customtkinter as ctk
from threading import Thread
import json
import keyboard
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

settings_file = 'settings.json'

default_settings = {
    'min_interval': 0.5,
    'max_interval': 1.5,
    'toggle_key': 'h',
    'language': 'en'
}

def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            return settings.get('min_interval', default_settings['min_interval']), \
                   settings.get('max_interval', default_settings['max_interval']), \
                   settings.get('toggle_key', default_settings['toggle_key']), \
                   settings.get('language', default_settings['language'])
    return default_settings['min_interval'], default_settings['max_interval'], default_settings['toggle_key'], default_settings['language']

def save_settings():
    settings = {
        'min_interval': min_interval,
        'max_interval': max_interval,
        'toggle_key': toggle_key,
        'language': language
    }
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

first_button_image = 'button.png'
second_button_image = 'second_button.png'
running = False

min_interval, max_interval, toggle_key, language = load_settings()

texts = {
    'uk': {
        'title': "Unfollow Bot",
        'functionality': "Функціонал",
        'start_bot': "Запустити бота",
        'stop_bot': "Зупинити бота",
        'status_running': "Статус: Бот запущено",
        'status_stopped': "Статус: Бот зупинено",
        'stop_instructions': "Зупинити бота можна за допомогою гарячої клавіші",
        'settings': "Налаштування",
        'min_interval': "Мін. інтервал (сек):",
        'max_interval': "Макс. інтервал (сек):",
        'toggle_key': f"Гаряча клавіша: {toggle_key}",
        'select_language': "Оберіть мову:"
    },
    'en': {
        'title': "Unfollow Bot",
        'functionality': "Functionality",
        'start_bot': "Start Bot",
        'stop_bot': "Stop Bot",
        'status_running': "Status: Bot is running",
        'status_stopped': "Status: Bot is stopped",
        'stop_instructions': "You can stop the bot using the hotkey",
        'settings': "Settings",
        'min_interval': "Min Interval (sec):",
        'max_interval': "Max Interval (sec):",
        'toggle_key': f"Hotkey: {toggle_key}",
        'select_language': "Select Language:"
    }
}

def click_button(image_path):
    try:
        button_location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if button_location is not None:
            button_center = pyautogui.center(button_location)
            pyautogui.click(button_center)
            print(f"Клик по кнопке {image_path} выполнен.")
            return True
        else:
            print(f"Кнопка {image_path} не найдена.")
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def bot_loop():
    global running, min_interval, max_interval
    while running:
        if click_button(first_button_image):
            time.sleep(random.uniform(min_interval, max_interval))
            click_button(second_button_image)
        else:
            pyautogui.scroll(-300)
            print("Первая кнопка не найдена, выполняю прокрутку вниз.")
        time.sleep(random.uniform(min_interval, max_interval))
        
        # Проверяем нажатие горячей клавиши
        if keyboard.is_pressed(toggle_key):  # Проверяем, нажата ли горячая клавиша
            stop_bot()  # Останавливаем бота

def start_bot():
    global running
    if not running:
        running = True
        bot_thread = Thread(target=bot_loop)
        bot_thread.start()
        start_status_label.configure(text=texts[language]['status_running'])
        print("Бот запущен.")

def stop_bot():
    global running
    running = False
    start_status_label.configure(text=texts[language]['status_stopped'])
    print("Бот остановлен.")

def update_min_interval(value):
    global min_interval
    min_interval = float(value)
    print(f"Минимальный интервал установлен на: {min_interval} секунд")
    save_settings()  # Сохранение настроек при обновлении

def update_max_interval(value):
    global max_interval
    max_interval = float(value)
    print(f"Максимальный интервал установлен на: {max_interval} секунд")
    save_settings()  # Сохранение настроек при обновлении

def set_toggle_key():
    global toggle_key
    def on_key_press(event):
        global toggle_key
        toggle_key = event.keysym
        toggle_key_button.configure(text=f"Горячая клавиша: {toggle_key}")
        print(f"Горячая клавиша установлена на: {toggle_key}")
        save_settings()  # Сохранение настроек при изменении горячей клавиши
        root.unbind_all('<Key>')
    
    root.bind_all('<Key>', on_key_press)
    toggle_key_button.configure(text="Нажмите любую клавишу...")

def change_language(selected_language):
    global language
    language = selected_language
    title_label.configure(text=texts[language]['title'])
    functionality_label.configure(text=texts[language]['functionality'])
    start_button.configure(text=texts[language]['start_bot'])
    stop_button.configure(text=texts[language]['stop_bot'])
    stop_status_label.configure(text=texts[language]['stop_instructions'])
    settings_label.configure(text=texts[language]['settings'])
    min_interval_label.configure(text=texts[language]['min_interval'])
    max_interval_label.configure(text=texts[language]['max_interval'])
    toggle_key_button.configure(text=texts[language]['toggle_key'])
    language_label.configure(text=texts[language]['select_language'])
    save_settings()  # Сохранение языка в настройках

# Настройка интерфейса CustomTkinter
root = ctk.CTk()
root.title(texts[language]['title'])
root.geometry("400x500")

# Заголовок
title_label = ctk.CTkLabel(root, text=texts[language]['title'], font=("Arial", 20))
title_label.pack(pady=10)

# Фрейм для функционала
functionality_frame = ctk.CTkFrame(root)
functionality_frame.pack(pady=5, fill="x", padx=10)

functionality_label = ctk.CTkLabel(functionality_frame, text=texts[language]['functionality'], font=("Arial", 16))
functionality_label.pack(anchor="w", padx=10, pady=5)

# Кнопка запуска бота
start_button = ctk.CTkButton(functionality_frame, text=texts[language]['start_bot'], command=start_bot)
start_button.pack(fill="x", padx=5, pady=5)

start_status_label = ctk.CTkLabel(functionality_frame, text="")
start_status_label.pack(pady=5)

# Кнопка остановки бота
stop_button = ctk.CTkButton(functionality_frame, text=texts[language]['stop_bot'], command=stop_bot)
stop_button.pack(fill="x", padx=5, pady=5)

stop_status_label = ctk.CTkLabel(functionality_frame, text=texts[language]['stop_instructions'])
stop_status_label.pack(pady=5)

# Меню настроек
settings_frame = ctk.CTkFrame(root)
settings_frame.pack(pady=20, fill="x", padx=10)

settings_label = ctk.CTkLabel(settings_frame, text=texts[language]['settings'], font=("Arial", 16))
settings_label.pack(anchor="w", padx=10, pady=5)

# Поля ввода для интервалов
min_interval_frame = ctk.CTkFrame(settings_frame)
min_interval_frame.pack(fill="x", padx=10, pady=5)

min_interval_label = ctk.CTkLabel(min_interval_frame, text=texts[language]['min_interval'])
min_interval_label.pack(side="left", padx=5)
min_interval_entry = ctk.CTkEntry(min_interval_frame, width=50)
min_interval_entry.insert(0, str(min_interval))
min_interval_entry.pack(side="left", padx=5)
min_interval_entry.bind("<Return>", lambda event: update_min_interval(min_interval_entry.get()))

max_interval_frame = ctk.CTkFrame(settings_frame)
max_interval_frame.pack(fill="x", padx=10, pady=5)

max_interval_label = ctk.CTkLabel(max_interval_frame, text=texts[language]['max_interval'])
max_interval_label.pack(side="left", padx=5)
max_interval_entry = ctk.CTkEntry(max_interval_frame, width=50)
max_interval_entry.insert(0, str(max_interval))
max_interval_entry.pack(side="left", padx=5)
max_interval_entry.bind("<Return>", lambda event: update_max_interval(max_interval_entry.get()))

# Кнопка для установки горячей клавиши
toggle_key_button = ctk.CTkButton(settings_frame, text=texts[language]['toggle_key'], command=set_toggle_key)
toggle_key_button.pack(anchor="w", padx=10, pady=5)

# Язык
language_frame = ctk.CTkFrame(settings_frame)
language_frame.pack(fill="x", padx=10, pady=5)

language_label = ctk.CTkLabel(language_frame, text=texts[language]['select_language'])
language_label.pack(side="left", padx=5)

language_option = ctk.CTkOptionMenu(language_frame, values=["uk", "en"], command=change_language)
language_option.set(language)
language_option.pack(side="left", padx=5)

root.mainloop()
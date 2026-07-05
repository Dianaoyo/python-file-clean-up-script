import os
import time
from datetime import datetime, timedelta

TARGET_DIRECTORY = r"C:\Users\ditap\OneDrive\Desktop\Новая папка (2)"  # Для теста создайте рядом папку Temp_Folder и положите туда файлы

DAYS_THRESHOLD = 20

LOG_FILE_NAME = "cleanup_log.txt"

def setup_logging():
    """
    Создает или очищает файл лога перед началом работы.
    """
    with open(LOG_FILE_NAME, "w", encoding="utf-8") as log_file:
        log_file.write(f"--- Лог очистки папки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        log_file.write(f"Целевая папка: {os.path.abspath(TARGET_DIRECTORY)}\n")
        log_file.write("-" * 40 + "\n\n")

def log_action(message):
    """
    Добавляет сообщение в консоль и в файл лога.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE_NAME, "a", encoding="utf-8") as log_file:
        log_file.write(full_message + "\n")

def clean_directory():
    """
    Основная логика очистки папки.
    """
    setup_logging()

    if not os.path.exists(TARGET_DIRECTORY):
        log_action(f"ОШИБКА: Указанная папка '{TARGET_DIRECTORY}' не существует.")
        return

    log_action("Начинаем сканирование папки...")

    files_deleted = 0
    now = time.time()
    threshold_seconds = DAYS_THRESHOLD * 24 * 60 * 60

    for filename in os.listdir(TARGET_DIRECTORY):
        file_path = os.path.join(TARGET_DIRECTORY, filename)

        if os.path.isfile(file_path):
            try:
                file_modified_time = os.path.getmtime(file_path)

                file_age_seconds = now - file_modified_time

                if file_age_seconds > threshold_seconds:
                    mod_date_str = datetime.fromtimestamp(file_modified_time).strftime('%Y-%m-%d %H:%M')

                    log_action(f"УДАЛЯЮ: '{filename}' (Дата изменения: {mod_date_str})")
                    os.remove(file_path)
                    files_deleted += 1

            except Exception as e:
                log_action(f"ОШИБКА при удалении '{filename}': {e}")

    log_action("-" * 40)
    if files_deleted > 0:
        log_action(f"Готово. Удалено файлов: {files_deleted}.")
        log_action(f"Отчет сохранен в файл: {os.path.abspath(LOG_FILE_NAME)}")
    else:
        log_action("Готово. Старых файлов не найдено, ничего не удалено.")
        log_action(f"Отчет сохранен в файл: {os.path.abspath(LOG_FILE_NAME)}")

if __name__ == "__main__":
    clean_directory()
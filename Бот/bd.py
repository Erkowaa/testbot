import sqlite3

# Устанавливаем соединение с базой данных
conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

# Создаем таблицу пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    chat_id INTEGER PRIMARY KEY,
                    name TEXT,
                    department TEXT,
                    is_registered INTEGER
                )''')

# Создаем таблицу заявок
cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
                    request_id INTEGER PRIMARY KEY,
                    chat_id INTEGER,
                    problem TEXT,
                    description TEXT,
                    FOREIGN KEY (chat_id) REFERENCES users(chat_id)
                )''')

# Сохраняем изменения и закрываем соединение с базой данных
conn.commit()
conn.close()

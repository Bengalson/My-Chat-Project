import sqlite3

conn = sqlite3.connect('chat_history.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS messages (message_text text)''')
conn.commit()
conn.close()
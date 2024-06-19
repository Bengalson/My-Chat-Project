import sqlite3

conn = sqlite3.connect('library.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS books (title text, author text)''')

c.execute("INSERT INTO books VALUES ('The Carcher in the rye', 'J.D , Salinger'")
c.execute("INSERT INTO books VALUES ('To Kill a Mockingbird' , 'Harper Lee')")
c.execute("INSERT INTO books VALUES ('1984' , 'Georgr Orwell')")

conn.commit()

c.execute('SELECT * FROM books')
print("Books in the database:")
for row in c.fetchall():
    print(row)

conn.close
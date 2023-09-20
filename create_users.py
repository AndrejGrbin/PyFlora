import sqlite3

# Stvaranje baze podataka i tablice
conn = sqlite3.connect("pyflora.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE users
                  (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_name TEXT NOT NULL UNIQUE,
                   ime TEXT NOT NULL,
                   prezime TEXT NOT NULL,
                   password TEXT NOT NULL)''')

# Unos primjernih korisničkih podataka
user_data = [
    ("admin", "John", "Doe", "password")
]

cursor.executemany("INSERT INTO users (user_name, ime, prezime, password) VALUES (?, ?, ?, ?)", user_data)

# Potvrda promjena i zatvaranje veze s bazom podataka
conn.commit()
conn.close()
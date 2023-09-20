import sqlite3

# Stvaranje baze podataka i tablice
conn = sqlite3.connect("pyflora.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE plants
                (id_biljke INTEGER PRIMARY KEY AUTOINCREMENT,
                naziv TEXT NOT NULL UNIQUE,
                slika TEXT NOT NULL,
                vlaznost_tla REAL NOT NULL,
                osvjetljenje INTEGER NOT NULL,
                temperatura_celzijusi REAL NOT NULL,
                dohrana BOOLEAN NOT NULL)''')

# Unos primjernih korisničkih podataka
user_data = [
    ("Božur", "images/bozur.png", 0.2, 1750, 25, True),
    ("Dalija", "images/dalija.png", 0.2, 5000, 30, True),
    ("Lotos", "images/lotos.png", 0.5, 500, 30, False),
    ("Ljiljan", "images/ljiljan.png", 0.1, 7500, 30, True),
    ("Neven", "images/neven.png", 0.1, 2500, 25, True),
    ("Ruža", "images/ruza.png", 0.25, 1750, 25, True),
    ("Suncokret", "images/suncokret.png", 0.15, 3250, 27, False),
    ("Tratinčica", "images/tratincica.png", 0.3, 4750, 28, False),
    ("Tulipan", "images/tulipan.png", 0.35, 1000, 25, True),
    ("Zimzelen", "images/zimzelen.png", 0.05, 3250, 25, False)
]

cursor.executemany("INSERT INTO plants (naziv, slika, vlaznost_tla, osvjetljenje, temperatura_celzijusi, dohrana) VALUES (?, ?, ?, ?, ?, ?)", user_data)
# Potvrda promjena i zatvaranje veze s bazom podataka
conn.commit()
conn.close()
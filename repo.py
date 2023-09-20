import sqlite3

def connect_to_database():
    conn = sqlite3.connect("pyflora.db")
    return conn

def close_database_connection(conn):
    conn.close()

def check_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_name=? AND password=?", (username, password))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_user_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    user_data = cursor.fetchone()
    cursor.close()
    return user_data

def update_user_data(conn, new_name, new_surname, new_username, new_password):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET ime=?, prezime=?, user_name=?, password=?", (new_name, new_surname, new_username, new_password))
    conn.commit()
    cursor.close()

def update_plant_data(conn, id_biljke, new_naziv, new_putanja, new_vlaznost_tla, new_osvjetljenje, new_temperatura, new_dohrana):
    cursor = conn.cursor()
    cursor.execute("UPDATE plants SET naziv=?, slika=?, vlaznost_tla=?, osvjetljenje=?, temperatura_celzijusi=?, dohrana=? WHERE id_biljke=?", (new_naziv, new_putanja, new_vlaznost_tla, new_osvjetljenje, new_temperatura, new_dohrana, id_biljke))
    conn.commit()
    cursor.close()

def check_plant_exists(conn, new_naziv):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plants WHERE naziv=?", (new_naziv))
    naziv = cursor.fetchone()
    cursor.close()
    return naziv

def insert_plant(conn, naziv, putanja, vlaznost_tla, osvjetljenje, temperatura, dohrana):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO plants (naziv, slika, vlaznost_tla, osvjetljenje, temperatura_celzijusi, dohrana) VALUES (?, ?, ?, ?, ?, ?)",
                   (naziv, putanja, vlaznost_tla, osvjetljenje, temperatura, dohrana))
    conn.commit()
    cursor.close()
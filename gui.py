import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import repo

class MainWindow(tk.Tk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.title("PyPosude - Popis posuda")
        self.geometry("800x600")

        # Gornja traka (navbar)
        navbar_frame = tk.Frame(self)
        navbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Naziv aplikacije
        app_name_label = tk.Label(navbar_frame, text="PyFlora Posude", font=("Arial", 14, "bold"))
        app_name_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Gumbi Biljke i Moj Profil
        plants_button = tk.Button(navbar_frame, text="Biljke", command=self.open_plants_window)
        plants_button.pack(side=tk.LEFT, padx=10, pady=5)

        profile_button = tk.Button(navbar_frame, text="Moj Profil", command=self.open_update_window)
        profile_button.pack(side=tk.LEFT, padx=10, pady=5)

        # User_name prijavljenog korisnika
        user_data = repo.get_user_data(self.conn)
        user_name_label = tk.Label(navbar_frame, text="Korisnik: {}".format(user_data[1]))
        user_name_label.pack(side=tk.RIGHT, padx=10, pady=5)

        # Gumb "Dodaj novu vazu" u glavnom frame-u
        add_vase_button = tk.Button(self, text="Dodaj novu vazu", command=self.add_new_vase)
        add_vase_button.pack(side=tk.TOP, padx=10, pady=5)

    def open_plants_window(self):
        plants_window = PlantsWindow(self.conn)
        plants_window.mainloop()

    def open_update_window(self):
        update_window = UpdateUserWindow(self.conn)
        update_window.mainloop()

    def add_new_vase(self):
    # otvaranje prozora za dodavanje nove vaze
        pass

    def __del__(self):
        repo.close_database_connection(self.conn)

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.conn = repo.connect_to_database()
        self.title("Prijava")
        self.geometry("800x600")

        # Labela i unos za korisničko ime
        username_label = tk.Label(self, text="Korisničko ime:")
        username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # Labela i unos za lozinku
        password_label = tk.Label(self, text="Lozinka:")
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*")  # Skrivanje prikaza unosa lozinke
        self.password_entry.pack()

        # Gumb za prijavu
        login_button = tk.Button(self, text="Prijavi se", command=self.login)
        login_button.pack()

    def login(self):
        # Uneseni korisnički podaci
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Provjera korisničkih podataka u bazi

        if repo.check_user(self.conn, username, password):
            # Prijava uspješna, prikaži poruku i otvori glavni prozor
            messagebox.showinfo("Prijavljeno", "Uspješna prijava!")
            main_window = MainWindow(self.conn)
            self.destroy()
            main_window.mainloop()
        else:
            # Prijava nije uspjela, prikaži poruku o pogrešnim podacima
            messagebox.showerror("Pogrešna prijava", "Uneseni korisnički podaci nisu ispravni.")

    def __del__(self):
        repo.close_database_connection(self.conn)

class UpdateUserWindow(tk.Tk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.title("Ažuriranje korisnika")
        self.geometry("800x600")

        # Dohvatite korisničke podatke iz baze
        user_data = repo.get_user_data(self.conn)
        ime = user_data[2]  # Index 2 odgovara "ime" u tablici "users"
        prezime = user_data[3]  # Index 3 odgovara "prezime" u tablici "users"
        korisnicko_ime = user_data[1]  # Index 4 odgovara "user_name" u tablici "users"
        lozinka = user_data[4]  # Index 5 odgovara "password" u tablici "users"

        # Labela i unos za ime
        ime_label = tk.Label(self, text="Ime:")
        ime_label.pack()
        self.ime_entry = tk.Entry(self)
        self.ime_entry.insert(0, ime)  # Postavite početnu vrijednost na ime iz baze
        self.ime_entry.pack()

        # Labela i unos za prezime
        prezime_label = tk.Label(self, text="Prezime:")
        prezime_label.pack()
        self.prezime_entry = tk.Entry(self)
        self.prezime_entry.insert(0, prezime)  # Postavite početnu vrijednost na prezime iz baze
        self.prezime_entry.pack()

        # Labela i unos za korisničko ime
        korisnicko_ime_label = tk.Label(self, text="Korisničko Ime:")
        korisnicko_ime_label.pack()
        self.korisnicko_ime_entry = tk.Entry(self)
        self.korisnicko_ime_entry.insert(0, korisnicko_ime)  # Postavite početnu vrijednost na korisničko ime iz baze
        self.korisnicko_ime_entry.pack()

        # Labela i unos za lozinku
        lozinka_label = tk.Label(self, text="Lozinka:")
        lozinka_label.pack()
        self.lozinka_entry = tk.Entry(self, show="*")
        self.lozinka_entry.insert(0, lozinka)  # Postavite početnu vrijednost na lozinku iz baze
        self.lozinka_entry.pack()

        # Gumb za prikazivanje/skrivanje lozinke
        self.show_password_var = tk.BooleanVar()
        show_password_button = tk.Checkbutton(self, text="Prikaži/sakrij lozinku", variable=self.show_password_var, command=self.toggle_password_visibility)
        show_password_button.pack()

        # Gumb za ažuriranje korisničkih podataka
        update_button = tk.Button(self, text="Ažuriraj", command=self.update_user_data)
        update_button.pack()

    def toggle_password_visibility(self):
        # Prikazivanje/skrivanje lozinke ovisno o stanju show_password_var
        show_password = self.show_password_var.get()
        if show_password:
            self.lozinka_entry.config(show="")
        else:
            self.lozinka_entry.config(show="*")

    def update_user_data(self):
        # Dohvatite nove vrijednosti unosa
        novo_ime = self.ime_entry.get()
        novo_prezime = self.prezime_entry.get()
        novo_korisnicko_ime = self.korisnicko_ime_entry.get()
        nova_lozinka = self.lozinka_entry.get()

        # Prikaži messagebox s izborom
        result = messagebox.askquestion("Potvrda", "Jeste li sigurni da želite ažurirati korisničke podatke?")

        if result == "yes":
        # Ažurirajte korisničke podatke u bazi
            repo.update_user_data(self.conn, novo_ime, novo_prezime, novo_korisnicko_ime, nova_lozinka)

            # Zatvorite prozor za ažuriranje korisnika
            self.destroy()

    def __del__(self):
        repo.close_database_connection(self.conn)

class PlantsWindow(tk.Tk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.title("PyPosude - Popis biljaka")
        self.geometry("800x600")

        # Gornji traka (navbar)
        navbar_frame = tk.Frame(self)
        navbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Naziv aplikacije
        app_name_label = tk.Label(navbar_frame, text="PyFlora Biljke", font=("Arial", 14, "bold"))
        app_name_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Gumbi Posude i Moj Profil
        vases_button = tk.Button(navbar_frame, text="Posude", command=self.open_vases_window)
        vases_button.pack(side=tk.LEFT, padx=10, pady=5)

        profile_button = tk.Button(navbar_frame, text="Moj Profil", command=self.open_update_window)
        profile_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Gumb za dodavanje nove biljke
        self.dodaj_biljku_button = tk.Button(self, text="Dodaj biljku", command=self.add_new_plant)
        self.dodaj_biljku_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Popis biljaka (lijevo)
        self.plant_listbox = tk.Listbox(self, width=30)
        self.plant_listbox.pack(side=tk.LEFT, padx=10, pady=10)
        self.plant_listbox.bind("<<ListboxSelect>>", self.display_selected_plant)  # Dodajte event handler za odabir

        # Desni frame za prikaz pojedinačnih biljaka
        self.plant_details_frame = tk.Frame(self)
        self.plant_details_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Elementi za prikaz pojedinačnih biljaka
        self.id_biljke_label = tk.Label(self.plant_details_frame, text="ID:")
        self.id_biljke_label.grid(row=0, column=0, sticky="w")

        self.id_biljke_entry = tk.Entry(self.plant_details_frame)
        self.id_biljke_entry.grid(row=0, column=1, padx=5, pady=5)

        self.naziv_label = tk.Label(self.plant_details_frame, text="Naziv biljke:")
        self.naziv_label.grid(row=1, column=0, sticky="w")

        self.naziv_entry = tk.Entry(self.plant_details_frame)
        self.naziv_entry.grid(row=1, column=1, padx=5, pady=5)

        self.putanja_label = tk.Label(self.plant_details_frame, text="Putanja slike (Path):")
        self.putanja_label.grid(row=2, column=0, sticky="w")

        self.putanja_entry = tk.Entry(self.plant_details_frame)
        self.putanja_entry.grid(row=2, column=1, padx=5, pady=5)

        self.vlaznost_label = tk.Label(self.plant_details_frame, text="Potrebna vlažnost tla (0-1):")
        self.vlaznost_label.grid(row=3, column=0, sticky="w")

        self.vlaznost_entry = tk.Entry(self.plant_details_frame)
        self.vlaznost_entry.grid(row=3, column=1, padx=5, pady=5)

        self.osvjetljenje_label = tk.Label(self.plant_details_frame, text="Potrebno osvjetljenje (lumen):")
        self.osvjetljenje_label.grid(row=4, column=0, sticky="w")

        self.osvjetljenje_entry = tk.Entry(self.plant_details_frame)
        self.osvjetljenje_entry.grid(row=4, column=1, padx=5, pady=5)

        self.temperatura_label = tk.Label(self.plant_details_frame, text="Potrebna temperatura (stupnjevi celzijusi):")
        self.temperatura_label.grid(row=5, column=0, sticky="w")

        self.temperatura_entry = tk.Entry(self.plant_details_frame)
        self.temperatura_entry.grid(row=5, column=1, padx=5, pady=5)

        self.dohrana_label = tk.Label(self.plant_details_frame, text="Dohrana:")
        self.dohrana_label.grid(row=6, column=0, sticky="w")

        self.dohrana_var = tk.StringVar()  # Uklonili smo inicijalnu vrijednost

        self.dohrana_da_radio = tk.Radiobutton(self.plant_details_frame, text="Da", variable=self.dohrana_var, value="Da")
        self.dohrana_da_radio.grid(row=6, column=1, padx=5, pady=5)

        self.dohrana_ne_radio = tk.Radiobutton(self.plant_details_frame, text="Ne", variable=self.dohrana_var, value="Ne")
        self.dohrana_ne_radio.grid(row=6, column=2, padx=5, pady=5)

        # Prikaz slike
        self.slika_label = tk.Label(self.plant_details_frame)
        self.slika_label.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

        # Dodajte event handler za klik na sliku
        self.slika_label.bind("<Button-1>", self.choose_image)

        # Dodajte gumb za ažuriranje
        self.update_button = tk.Button(self.plant_details_frame, text="Ažuriraj", command=self.update_plant)
        self.update_button.grid(row=7, column=0, columnspan=3, pady=10)

        # Prikaz svih biljaka u Listbox
        self.display_all_plants()

    def choose_image(self, event):
        # Otvaranje dijaloga za odabir slike
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])

        # Ažuriranje putanje slike u Entry-ju
        if file_path:
            self.putanja_entry.delete(0, tk.END)
            self.putanja_entry.insert(0, file_path)


    def display_all_plants(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT naziv FROM plants")
        plants = cursor.fetchall()
        for plant in plants:
            self.plant_listbox.insert(tk.END, plant[0])
        cursor.close()

    def display_selected_plant(self, event):
        selected_index = self.plant_listbox.curselection()
        if selected_index:
            selected_plant = self.plant_listbox.get(selected_index[0])
            self.display_plant_details(selected_plant)

    def display_plant_details(self, plant_name):
        # Dohvatite podatke o biljci iz baze prema nazivu
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM plants WHERE naziv=?", (plant_name,))
        plant_data = cursor.fetchone()
        cursor.close()

        # Ispis podataka o biljci u desnom frame-u
        if plant_data:
            self.id_biljke_entry.configure(state='normal')
            self.id_biljke_entry.delete(0, tk.END)
            self.id_biljke_entry.insert(0, plant_data[0])
            self.id_biljke_entry.configure(state='readonly')

            self.naziv_entry.delete(0, tk.END)
            self.naziv_entry.insert(0, plant_data[1])

            self.putanja_entry.delete(0, tk.END)
            self.putanja_entry.insert(0, plant_data[2])

            self.vlaznost_entry.delete(0, tk.END)
            self.vlaznost_entry.insert(0, str(plant_data[3]))

            self.osvjetljenje_entry.delete(0, tk.END)
            self.osvjetljenje_entry.insert(0, str(plant_data[4]))

            self.temperatura_entry.delete(0, tk.END)
            self.temperatura_entry.insert(0, str(plant_data[5]))

            # Postavljanje vrijednosti Radio gumba
            self.dohrana_var.set("Da" if plant_data[6] else "Ne")

            # Prikaz slike
            slika_path = plant_data[2]
            slika = tk.PhotoImage(file=slika_path)
            self.slika_label.config(image=slika)
            self.slika_label.image = slika  # Očuvanje reference na sliku
            # Ostali podaci o biljci (vlažnost, osvjetljenje, temperatura, dohrana_tjedno)
            # Dodajte ovdje Label-ove i prikažite podatke

    def update_plant(self):
        # Dohvati unesene podatke iz Entry-eva
        id_biljke = self.id_biljke_entry.get()  # Pretpostavimo da imate atribut "id_biljke" u vašoj klasi koji sadrži ID biljke koju želite ažurirati
        new_naziv = self.naziv_entry.get()
        new_putanja = self.putanja_entry.get()
        new_vlaznost_tla = float(self.vlaznost_entry.get())
        new_osvjetljenje = int(self.osvjetljenje_entry.get())
        new_temperatura = float(self.temperatura_entry.get())
        new_dohrana = True if self.dohrana_var.get() == "Da" else False

        # Prikaži messagebox s izborom
        result = messagebox.askquestion("Ažuriranje biljke", "Jeste li sigurni da želite ažurirati podatke biljke?")

        if result == "yes":
            # Ažurirajte biljku u bazi podataka
            repo.update_plant_data(self.conn, id_biljke, new_naziv, new_putanja, new_vlaznost_tla, new_osvjetljenje, new_temperatura, new_dohrana)

            # Nakon ažuriranja prikažite messagebox s potvrdom
            messagebox.showinfo("Ažurirano", "Podaci biljke su uspješno ažurirani.")
            # Zatvorite prozor za ažuriranje biljke
            self.destroy()

    def add_new_plant(self):
        self.destroy()
        new_plant_window = AddPlantWindow(self.conn)
        new_plant_window.mainloop()

    def open_vases_window(self):
        vases_window = MainWindow(self.conn)
        vases_window.mainloop()

    def open_update_window(self):
        update_window = UpdateUserWindow(self.conn)
        update_window.mainloop()

    def __del__(self):
        repo.close_database_connection(self.conn)

class AddPlantWindow(tk.Tk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.title("PyPosude - Dodaj biljku")
        self.geometry("800x600")

        # Gornji traka (navbar)
        navbar_frame = tk.Frame(self)
        navbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Naziv aplikacije
        app_name_label = tk.Label(navbar_frame, text="PyFlora Biljke", font=("Arial", 14, "bold"))
        app_name_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Gumbi Posude i Moj Profil
        vases_button = tk.Button(navbar_frame, text="Posude", command=self.open_vases_window)
        vases_button.pack(side=tk.LEFT, padx=10, pady=5)

        profile_button = tk.Button(navbar_frame, text="Moj Profil", command=self.open_update_window)
        profile_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Elementi za unos biljke
        self.naziv_label = tk.Label(self.plant_details_frame, text="Naziv biljke:")
        self.naziv_label.grid(row=0, column=0, sticky="w")

        self.naziv_entry = tk.Entry(self.plant_details_frame)
        self.naziv_entry.grid(row=0, column=1, padx=5, pady=5)

        self.putanja_label = tk.Label(self.plant_details_frame, text="Putanja slike (Path):")
        self.putanja_label.grid(row=1, column=0, sticky="w")

        # Dodajte gumb za ažuriranje
        self.search_button = tk.Button(self.plant_details_frame, text="Traži", command=self.choose_image)
        self.search_button.grid(row=1, column=1, columnspan=3, pady=10)

        self.putanja_entry = tk.Entry(self.plant_details_frame)
        self.putanja_entry.grid(row=1, column=1, padx=5, pady=5)

        self.vlaznost_label = tk.Label(self.plant_details_frame, text="Potrebna vlažnost tla (0-1):")
        self.vlaznost_label.grid(row=2, column=0, sticky="w")

        self.vlaznost_entry = tk.Entry(self.plant_details_frame)
        self.vlaznost_entry.grid(row=2, column=1, padx=5, pady=5)

        self.osvjetljenje_label = tk.Label(self.plant_details_frame, text="Potrebno osvjetljenje (lumen):")
        self.osvjetljenje_label.grid(row=3, column=0, sticky="w")

        self.osvjetljenje_entry = tk.Entry(self.plant_details_frame)
        self.osvjetljenje_entry.grid(row=3, column=1, padx=5, pady=5)

        self.temperatura_label = tk.Label(self.plant_details_frame, text="Potrebna temperatura (stupnjevi celzijusi):")
        self.temperatura_label.grid(row=4, column=0, sticky="w")

        self.temperatura_entry = tk.Entry(self.plant_details_frame)
        self.temperatura_entry.grid(row=4, column=1, padx=5, pady=5)

        self.dohrana_label = tk.Label(self.plant_details_frame, text="Dohrana:")
        self.dohrana_label.grid(row=5, column=0, sticky="w")

        self.dohrana_var = tk.StringVar()  # Uklonili smo inicijalnu vrijednost

        self.dohrana_da_radio = tk.Radiobutton(self.plant_details_frame, text="Da", variable=self.dohrana_var, value="Da")
        self.dohrana_da_radio.grid(row=5, column=1, padx=5, pady=5)

        self.dohrana_ne_radio = tk.Radiobutton(self.plant_details_frame, text="Ne", variable=self.dohrana_var, value="Ne")
        self.dohrana_ne_radio.grid(row=5, column=2, padx=5, pady=5)

        # Prikaz slike
        self.slika_label = tk.Label(self.plant_details_frame)
        self.slika_label.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

    def open_vases_window(self):
        vases_window = MainWindow(self.conn)
        vases_window.mainloop()

    def open_update_window(self):
        update_window = UpdateUserWindow(self.conn)
        update_window.mainloop()

    def __del__(self):
        repo.close_database_connection(self.conn)


    def choose_image(self, event):
        # Otvaranje dijaloga za odabir slike
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])

        # Ažuriranje putanje slike u Entry-ju
        if file_path:
            self.putanja_entry.delete(0, tk.END)
            self.putanja_entry.insert(0, file_path)
        
        # Dohvati unesene podatke iz Entry-eva
        new_naziv = self.naziv_entry.get()
        new_putanja = self.putanja_entry.get()
        new_vlaznost_tla = float(self.vlaznost_entry.get())
        new_osvjetljenje = int(self.osvjetljenje_entry.get())
        new_temperatura = float(self.temperatura_entry.get())
        new_dohrana = True if self.dohrana_var.get() == "Da" else False

        # Prikaži messagebox s izborom
        result = messagebox.askquestion("Dodavanje biljke", "Jeste li sigurni da želite dodati biljku?")

        if result == "yes":
        # Provjeri postoji li biljka s istim nazivom u bazi
            if repo.check_plant_exists(self.conn, new_naziv):
                tk.messagebox.showerror("Greška", "Biljka s tim nazivom već postoji u bazi podataka.")
                return

            # Dodajte novu biljku u bazu podataka
            repo.insert_plant(self.conn, new_naziv, new_putanja, new_vlaznost_tla, new_osvjetljenje, new_temperatura, new_dohrana)

            # Osvježite listbox prikaz s novom biljkom (implementacija ovisi o tome kako prikazujete biljke)
            self.osvjezi_listbox()
            tk.messagebox.showinfo("Dodano", "Nova biljka je uspješno dodana.")

"""         # Prikaz popisa posuda
        self.display_vases()

    # Funkcije
    def display_vases(self):
    # Otvorite vezu s bazom podataka i dohvatite podatke
    #cursor = self.conn.cursor()
   # cursor.execute("SELECT * FROM posude")
    #vases_data = cursor.fetchall()
        pass
    # Iterirajte kroz podatke o vazama i prikažite ih
    for vase_data in vases_data:
        vase_frame = tk.Frame(self)
        vase_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Uzmite podatke o vazi iz rezultata upita
        image_path = vase_data[0]  # Slika biljke
        vase_name = vase_data[1]  # Naziv vaze
        plant_name = vase_data[2]  # Naziv biljke
        moisture = vase_data[3]  # Vlažnost tla
        ph_value = vase_data[4]  # pH vrijednost tla
        light_level = vase_data[5]  # Razina svijetla
        temperature = vase_data[6]  # Temperatura zraka

        # Prikaz podataka o vazi
        # Ovdje možete koristiti Label, Canvas ili druge Tkinter widgete za prikaz podataka
        # Na primjer, za prikaz slike biljke:
        image_label = tk.Label(vase_frame, image=image_path)
        image_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Prikaz ostalih podataka o vazi (naziv vaze, naziv biljke, vlažnost, pH, svjetlost, temperatura)
        vase_info = f"Vaza: {vase_name}\nBiljka: {plant_name}\nVlažnost tla: {moisture}\n\
                     pH vrijednost tla: {ph_value}\nRazina svijetla: {light_level}\n\
                     Temperatura zraka: {temperature}"
        info_label = tk.Label(vase_frame, text=vase_info)
        info_label.pack(side=tk.LEFT, padx=10, pady=5)

    # Zatvorite cursor
    cursor.close() """


"""class PlantsWindow(tk.Tk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.title("PyPosude - Popis biljaka")
        self.geometry("600x400")

        # Gornji traka (navbar)
        navbar_frame = tk.Frame(self)
        navbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Naziv aplikacije
        app_name_label = tk.Label(navbar_frame, text="PyFlora Posude", font=("Arial", 14, "bold"))
        app_name_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Gumbi Biljke i Moj Profil
        plants_button = tk.Button(navbar_frame, text="Biljke", state=tk.DISABLED)
        plants_button.pack(side=tk.LEFT, padx=10, pady=5)

        profile_button = tk.Button(navbar_frame, text="Moj Profil", command=self.open_update_window)
        profile_button.pack(side=tk.LEFT, padx=10, pady=5)

        # User_name prijavljenog korisnika
        user_data = repo.get_user_data(self.conn)
        user_name_label = tk.Label(navbar_frame, text="Korisnik: {}".format(user_data[1]))
        user_name_label.pack(side=tk.RIGHT, padx=10, pady=5)

        # Implementirajte prikaz popisa biljaka

    def open_update_window(self):
        update_window = UpdateUserWindow(self.conn)
        update_window.mainloop()

    def __del__(self):
        repo.close_database_connection(self.conn)"""
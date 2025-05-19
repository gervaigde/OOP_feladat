from abc import ABC, abstractmethod
from datetime import datetime

# ------------------ Absztrakt Auto osztály ------------------
class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def get_ar(self):
        pass

# ------------------ Szemelyauto osztály ------------------
class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ulesek_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ulesek_szama = ulesek_szama

    def get_ar(self):
        return self.berleti_dij

# ------------------ Teherauto osztály ------------------
class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    def get_ar(self):
        return self.berleti_dij

# ------------------ Berles osztály ------------------
class Berles:
    def __init__(self, auto, datum, berlo):
        self.auto = auto
        self.datum = datum
        self.berlo = berlo

# ------------------ User osztály ------------------
class User:
    def __init__(self, nev, szerep="diak"):
        self.nev = nev
        self.szerep = szerep

# ------------------ Autokolcsonzo osztály ------------------
class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def autok_hozzaadasa(self, auto):
        self.autok.append(auto)

    def auto_berlese(self, rendszam, datum_str, user):
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
        except ValueError:
            print("Hibás dátumformátum. (Helyes: ÉÉÉÉ-HH-NN)")
            return

        for b in self.berlesek:
            if b.auto.rendszam == rendszam and b.datum == datum:
                print("Ez az autó már foglalt ezen a napon.")
                return

        for auto in self.autok:
            if auto.rendszam == rendszam:
                uj_berles = Berles(auto, datum, user)
                self.berlesek.append(uj_berles)
                print(f"Sikeres bérlés! Ár: {auto.get_ar()} Ft")
                return

        print("Nincs ilyen rendszámú autó a rendszerben.")

    def berles_lemondasa(self, rendszam, datum_str, user):
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
        except ValueError:
            print("Hibás dátumformátum.")
            return

        for b in self.berlesek:
            if b.auto.rendszam == rendszam and b.datum == datum and b.berlo.nev == user.nev:
                self.berlesek.remove(b)
                print("A bérlés sikeresen lemondva.")
                return

        print("Nincs ilyen bérlés.")

    def listaz_berlesek(self):
        if not self.berlesek:
            print("Nincsenek aktív bérlések.")
            return
        for b in self.berlesek:
            print(f"{b.datum.date()} - {b.auto.rendszam} ({b.auto.tipus}) - Bérelte: {b.berlo.nev}")

# ------------------ Tesztadatok betöltése ------------------
kolcsonzo = Autokolcsonzo("Teszt Kölcsönző")
kolcsonzo.autok_hozzaadasa(Szemelyauto("ABC123", "Toyota Corolla", 10000, 5))
kolcsonzo.autok_hozzaadasa(Szemelyauto("XYZ789", "Ford Focus", 12000, 5))
kolcsonzo.autok_hozzaadasa(Teherauto("DEF456", "Mercedes Sprinter", 15000, 2000))

diak_user = User("Kiss Pista")
tanar_user = User("Tanár Béla", szerep="tanar")
kolcsonzo.auto_berlese("ABC123", "2025-05-20", diak_user)
kolcsonzo.auto_berlese("DEF456", "2025-05-21", tanar_user)
kolcsonzo.auto_berlese("XYZ789", "2025-05-22", diak_user)
kolcsonzo.auto_berlese("DEF456", "2025-05-23", diak_user)

# ------------------ Konzolos menü ------------------
def menu():
    nev = input("Add meg a neved: ")
    szerep = input("Szerepkör (diak/tanar): ")
    user = User(nev, szerep)
    while True:
        print("\n1. Autó bérlése\n2. Bérlés lemondása\n3. Bérlések listázása\n4. Kilépés")
        valasztas = input("Válassz: ")
        if valasztas == "1":
            rendszam = input("Rendszám: ")
            datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
            kolcsonzo.auto_berlese(rendszam, datum, user)
        elif valasztas == "2":
            rendszam = input("Rendszám: ")
            datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
            kolcsonzo.berles_lemondasa(rendszam, datum, user)
        elif valasztas == "3":
            kolcsonzo.listaz_berlesek()
        elif valasztas == "4":
            break
        else:
            print("Érvénytelen választás.")

# Menü elindítása
if __name__ == "__main__":
    menu()

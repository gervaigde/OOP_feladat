from abc import ABC, abstractmethod
from datetime import datetime
import os

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

    def auto_letezik(self, rendszam):
        return any(auto.rendszam == rendszam for auto in self.autok)

    def auto_berlese(self, rendszam, datum_str, user, visszajelzes=True):
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
        except ValueError:
            if visszajelzes:
                print("Hibás dátumformátum. (Helyes: ÉÉÉÉ-HH-NN)")
            return

        for b in self.berlesek:
            if b.auto.rendszam == rendszam and b.datum == datum:
                if visszajelzes:
                    print("Ez az autó már foglalt ezen a napon.")
                return

        for auto in self.autok:
            if auto.rendszam == rendszam:
                uj_berles = Berles(auto, datum, user)
                self.berlesek.append(uj_berles)
                if visszajelzes:
                    print(f"Sikeres bérlés! Ár: {auto.get_ar()} Ft")
                return

        if visszajelzes:
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
            print("\nNincsenek aktív bérlések.")
            return
        print("\n" + "="*75)
        print(f"{'Név':<20}{'Rendszám':<12}{'Típus':<25}{'Dátum':<15}{'Ár (Ft)':<10}")
        print("-"*75)
        for b in self.berlesek:
            print(f"{b.berlo.nev:<20}{b.auto.rendszam:<12}{b.auto.tipus:<25}{b.datum.strftime('%Y-%m-%d'):<15}{b.auto.get_ar():<10}")
        print("="*75)

# ------------------ Tesztadatok betöltése ------------------
def tesztadatok_betoltese(kolcsonzo):
    kolcsonzo.autok_hozzaadasa(Szemelyauto("ABC123", "Toyota Corolla", 10000, 5))
    kolcsonzo.autok_hozzaadasa(Szemelyauto("XYZ789", "Ford Focus", 12000, 5))
    kolcsonzo.autok_hozzaadasa(Teherauto("DEF456", "Mercedes Sprinter", 15000, 2000))

    # Előre definiált nevek
    felhasznalok = [
        User("Cserép Virág"),
        User("Szõke Barna"),
        User("Remek Elek"),
        User("Kandisz Nóra"),
        User("Gipsz Jakab")
    ]

    datumok = ["2025-05-10", "2025-05-12", "2025-05-14", "2025-05-15", "2025-05-18"]
    rendszamok = ["ABC123", "DEF456", "XYZ789", "XYZ789", "DEF456"]

    for nev, rendszam, datum in zip(felhasznalok, rendszamok, datumok):
        kolcsonzo.auto_berlese(rendszam, datum, nev, visszajelzes=False)

# ------------------ Konzolos menü ------------------
def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*40)
    print("         GDE-Autókölcsönző Rendszer")
    print("               Verzió: 1.0")
    print("="*40)

    kolcsonzo = Autokolcsonzo("Teszt Kölcsönző")
    tesztadatok_betoltese(kolcsonzo)

    nev = input("Add meg a neved: ")

    while True:
        print("\nVálassz szerepkört:")
        print("1. Diák")
        print("2. Tanár")
        szerep_valasztas = input("Szerepkör száma (1/2): ")
        if szerep_valasztas == "1":
            szerep = "diak"
            break
        elif szerep_valasztas == "2":
            szerep = "tanar"
            break
        else:
            print("Érvénytelen választás. Próbáld újra.")

    user = User(nev, szerep)

    while True:
        print("\nKiválasztható műveletek:")
        print("1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Bérlések listázása")
        print("4. Kilépés")
        valasztas = input("Kiválasztott művelet: ")
        if valasztas == "1":
            rendszam = input("Rendszám: ")
            if not kolcsonzo.auto_letezik(rendszam):
                print("Nincs ilyen rendszámú autó a rendszerben.")
                continue
            datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
            kolcsonzo.auto_berlese(rendszam, datum, user)
        elif valasztas == "2":
            rendszam = input("Rendszám: ")
            datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
            kolcsonzo.berles_lemondasa(rendszam, datum, user)
        elif valasztas == "3":
            kolcsonzo.listaz_berlesek()
            input("\nA visszalépéshez nyomja meg az ENTER gombot...")
        elif valasztas == "4":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás.")

# Menü elindítása
if __name__ == "__main__":
    menu()

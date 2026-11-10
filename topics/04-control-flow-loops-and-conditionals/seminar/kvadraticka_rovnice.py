import math


def nacti_cislo(nazev: str) -> float:
    """Načte číslo od uživatele a ošetří neplatný vstup."""
    while True:
        try:
            hodnota = input(f"Zadej koeficient {nazev}: ").strip().replace(",", ".")
            return float(hodnota)
        except ValueError:
            print("Neplatny vstup. Zadej prosim platne cislo.")


def vyres_kvadratickou_rovnici():
    print("=== Reseni kvadraticke rovnice (a*x^2 + b*x + c = 0) ===")
    a = nacti_cislo("a")
    b = nacti_cislo("b")
    c = nacti_cislo("c")

    print(f"\nZadana rovnice: {a}*x^2 + ({b})*x + ({c}) = 0")

    # Kontrola, zda jde skutecne o kvadratickou rovnici
    if a == 0:
        print("Koeficient 'a' je roven 0, jedna se tedy o linearni rovnici:")
        if b == 0:
            if c == 0:
                print("Rovnice ma nekonecne mnoho reseni (0 = 0).")
            else:
                print(f"Rovnice nema zadne reseni ({c} = 0 neplati).")
        else:
            x = -c / b
            print(f"Linearni rovnice ma jeden koren: x = {x}")
        return

    # Vypocet diskriminantu
    diskriminant = b**2 - 4 * a * c
    print(f"Diskriminant D = {diskriminant}")

    if diskriminant > 0:
        odmocnina_d = math.sqrt(diskriminant)
        x1 = (-b + odmocnina_d) / (2 * a)
        x2 = (-b - odmocnina_d) / (2 * a)
        print("Diskriminant je kladny (D > 0) -> rovnice ma dva ruzne realne koreny:")
        print(f"  x1 = {x1}")
        print(f"  x2 = {x2}")
    elif diskriminant == 0:
        x = -b / (2 * a)
        print("Diskriminant je roven nule (D = 0) -> rovnice ma jeden dvojnasobny realny koren:")
        print(f"  x = {x}")
    else:
        print("Diskriminant je zaporny (D < 0) -> rovnice NEMA reseni v realnych cislech.")
        # Vypis komplexnich korenu pro uplnost
        realna_cast = -b / (2 * a)
        imaginarni_cast = math.sqrt(-diskriminant) / (2 * a)
        print("Reseni v oboru komplexnich cisel:")
        print(f"  x1 = {realna_cast} + {abs(imaginarni_cast)}i")
        print(f"  x2 = {realna_cast} - {abs(imaginarni_cast)}i")


if __name__ == "__main__":
    vyres_kvadratickou_rovnici()


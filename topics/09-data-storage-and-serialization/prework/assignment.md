# Úkoly

## Úloha na doma — uložení dat do JSONu a CSV

Máte následující data o knihách:

```python
books = [
    {"title": "Duna", "author": "Frank Herbert", "year": 1965, "available": True},
    {"title": "1984", "author": "George Orwell", "year": 1949, "available": False},
    {"title": "R.U.R.", "author": "Karel Čapek", "year": 1920, "available": True},
]
```

Napište program `save_books.py`, který:

1. uloží data do souboru `books.json`,
2. uloží stejná data do souboru `books.csv`,
3. oba soubory znovu načte pomocí odpovídajících knihoven,
4. vypíše načtený obsah z JSONu i CSV pro kontrolu.

Použijte:

- modul `json` pro práci s JSONem,
- modul `csv` pro práci s CSV,
- `with open(...)`,
- explicitní `encoding="utf-8"`,
- u CSV také `newline=""`.

### Co má být v programu vidět

Program by měl obsahovat:

- původní proměnnou `books`,
- zápis do JSONu pomocí `json.dump(...)`,
- zápis do CSV pomocí `csv.DictWriter(...)`,
- načtení JSONu pomocí `json.load(...)`,
- načtení CSV pomocí `csv.DictReader(...)`.

### Na co se při kontrole zaměřit

Po načtení obou souborů si všimněte:

- zda mají data stejnou strukturu,
- zda mají hodnoty `year` a `available` po načtení z CSV stejné datové typy jako původně,
- v čem se liší výstup z JSONu a CSV.

### Smysl domácí přípravy

Před výukou si vyzkoušíte:

- uložit stejná data dvěma různými způsoby,
- použít základní funkce modulů `json` a `csv`,
- ověřit, že při čtení CSV se hodnoty načítají jako text,
- připravit si konkrétní zkušenost, ke které se při výkladu vrátíme.

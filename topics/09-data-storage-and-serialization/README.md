# Efektivní ukládání dat a serializace

## Cíle

- Vysvětlit formáty serializace (JSON, CSV, binární).
- Serializovat a deserializovat jednoduché datové struktury.
- Volit formát podle kompromisů daného použití.

## Klíčová slova

Soubory, IO, JSON, CSV

## Přednáška

Slajdy zatím nejsou k dispozici.

Přehled serializace dat pro ukládání a přenos: JSON, CSV a jednoduché
binární formáty. Studenti se naučí ukládat strukturovaná data,
znovu je načítat a uvažovat o kompromisu mezi čitelností a velikostí dat.

- [Komentované příklady: ukládání dat a serializace](seminar/seminar.md)

### Osnova

1. Formáty: základy JSON, CSV, binární formáty (pickle)
2. Kódování a mapování datových typů
3. Čtení a zápis serializovaných dat
4. Výkonnostní a bezpečnostní aspekty
5. Kdy použít který formát

## Cvičení

Úkol pro domácí přípravu je [zde](prework/assignment.md).

Úkoly pro samostatnou práci na cvičení jsou [zde](lab/tasks.md).


Příklad: uložení a načtení JSON

```python
import json

data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
# zápis pomocí json.dumps pro vytvoření řetězce a vyhnutí se varování statického typování
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=2))

with open('data.json', 'r', encoding='utf-8') as f:
    loaded = json.load(f)
print(loaded)
```

## Zdroje

- Specifikace a tutoriály k JSON
- Dokumentace modulů `json` a `csv` v Pythonu

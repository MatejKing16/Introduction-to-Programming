# Úkoly na cvičení

Úlohy jsou seřazené od jednodušších k náročnějším. Začněte první a pokračujte dál podle času.

## Úloha 1 — Uložení a načtení JSONu

Máte data:

```python
games = [
    {"title": "Portal", "year": 2007, "completed": True},
    {"title": "Hades", "year": 2020, "completed": False},
    {"title": "Celeste", "year": 2018, "completed": True},
]
```

Napište program, který:

1. uloží data do `games.json`,
2. soubor znovu načte,
3. vypíše názvy všech her, které jsou dokončené.

### Procvičuje

- `json.dump`,
- `json.load`,
- práci se seznamem slovníků.

---

## Úloha 2 — Úprava dat v JSONu

Navazujte na soubor `games.json`.

Napište program, který:

1. načte hry,
2. najde hru `"Hades"`,
3. změní její hodnotu `completed` na `True`,
4. uloží upravená data do `games_updated.json`,
5. vypíše počet dokončených her před změnou a po změně.

### Procvičuje

- načtení a opětovné uložení JSONu,
- změnu dat po deserializaci,
- rozdíl mezi daty v souboru a daty v paměti programu.

---

## Úloha 3 — CSV katalog produktů

Máte data:

```python
products = [
    {"id": 1, "name": "keyboard", "price": 89, "in_stock": True},
    {"id": 2, "name": "monitor", "price": 499, "in_stock": False},
    {"id": 3, "name": "mouse", "price": 35, "in_stock": True},
]
```

Napište program, který:

1. uloží produkty do `products.csv`,
2. soubor znovu načte pomocí `csv.DictReader`,
3. obnoví typy:
   - `id` jako `int`,
   - `price` jako `int`,
   - `in_stock` jako `bool`,
4. vypíše produkty, které jsou skladem.

### Procvičuje

- `csv.DictWriter`,
- `csv.DictReader`,
- obnovu datových typů po načtení CSV.

---

## Úloha 4 — Převod plochých dat mezi CSV a JSON

Vytvořte program `convert_products.py`, který:

1. načte `products.csv`,
2. obnoví správné datové typy,
3. uloží data do `products.json`,
4. znovu načte `products.json`,
5. ověří výpisem, že hodnoty `price` jsou po načtení z JSONu opravdu čísla.

### Procvičuje

- převod mezi formáty,
- rozdíl mezi typy po načtení CSV a JSONu,
- kontrolu výsledku po serializaci.

---

## Úloha 5 — Vnořená data v JSONu

Máte data o školních třídách:

```python
school = {
    "classes": [
        {
            "name": "1A",
            "students": [
                {"name": "Anna", "grade": 1},
                {"name": "Petr", "grade": 2},
            ],
        },
        {
            "name": "2B",
            "students": [
                {"name": "Eva", "grade": 1},
                {"name": "Marek", "grade": 3},
            ],
        },
    ]
}
```

Napište program, který:

1. uloží strukturu do `school.json`,
2. znovu ji načte,
3. pro každou třídu vypíše:
   - název třídy,
   - počet studentů,
   - průměrnou známku.

### Procvičuje

- vnořenou strukturu v JSONu,
- průchod seznamem uvnitř slovníku,
- výpočet nad deserializovanými daty.

---

## Úloha 6 — Jedna vnořená struktura, dvě CSV tabulky

Máte data o strojích a uživatelích:

```python
company = {
    "machines": [
        {
            "id": 101,
            "hostname": "alpha",
            "location": "Lab A",
            "users": [
                {"id": 1, "name": "Anna", "role": "admin"},
                {"id": 2, "name": "Petr", "role": "operator"},
            ],
        },
        {
            "id": 102,
            "hostname": "beta",
            "location": "Lab B",
            "users": [
                {"id": 3, "name": "Eva", "role": "operator"},
                {"id": 4, "name": "Marek", "role": "viewer"},
            ],
        },
    ]
}
```

Jeden stroj může mít více uživatelů.

### Část A — export do dvou CSV souborů

Napište program, který z této vnořené struktury vytvoří:

#### `machines.csv`

```text
id,hostname,location
101,alpha,Lab A
102,beta,Lab B
```

#### `users.csv`

```text
id,name,role,machine_id
1,Anna,admin,101
2,Petr,operator,101
3,Eva,operator,102
4,Marek,viewer,102
```

Všimněte si, že vazba mezi tabulkami je uložená přes `machine_id`.

### Část B — načtení a propojení přes ID

Potom napište program, který:

1. načte `machines.csv`,
2. načte `users.csv`,
3. obnoví číselné typy ID,
4. propojí uživatele se stroji podle `machine_id`,
5. vypíše výsledek například takto:

```text
alpha (Lab A)
- Anna [admin]
- Petr [operator]

beta (Lab B)
- Eva [operator]
- Marek [viewer]
```

### Procvičuje

- rozdíl mezi vnořenou strukturou a relační reprezentací,
- rozdělení jedné Python struktury do více CSV tabulek,
- cizí klíč (`machine_id`),
- znovuspojení dat po načtení pomocí ID.

### Bonus

- Po načtení obou CSV souborů znovu sestavte původní strukturu `company`.
- Uložte rekonstruovanou strukturu do `company.json`.
- Přidejte kontrolu, která vypíše chybu, pokud `users.csv` obsahuje `machine_id`, které neexistuje v `machines.csv`.

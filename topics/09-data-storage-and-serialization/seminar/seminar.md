# Komentované příklady: ukládání dat a serializace

V minulém tématu jste pracovali se soubory jako s textem.  
V těchto příkladech půjdeme o krok dál: naučíte se ukládat **strukturovaná data** tak, aby je bylo možné později znovu načíst a dál zpracovávat.

## Co byste měli po společném průchodu umět

Po společném průchodu byste měli zvládnout:

- vysvětlit, co znamená serializace a deserializace,
- uložit Python data do JSONu a znovu je načíst,
- uložit tabulková data do CSV a znovu je načíst,
- popsat základní rozdíl mezi JSONem, CSV a binárním formátem,
- převést jednoduchý dataset mezi CSV a JSON,
- odhadnout, kdy je vhodnější JSON a kdy CSV.

---

## 1. Co je serializace

V programu často pracujeme s daty jako se seznamy a slovníky:

```python
students = [
    {"name": "Anna", "score": 92, "passed": True},
    {"name": "Petr", "score": 71, "passed": True},
    {"name": "Eva", "score": 48, "passed": False},
]
```

Taková data existují pouze za běhu programu.  
Pokud je chceme uložit do souboru nebo poslat jinam, musíme je převést do formátu, který lze zapsat jako text nebo bajty.

Tomu říkáme **serializace**.

Když data ze souboru znovu načteme zpět do Pythonu, jde o **deserializaci**.

---

## 2. JSON: strukturovaná data podobná Pythonu

JSON je vhodný pro:

- seznamy a slovníky,
- konfigurační soubory,
- komunikaci mezi programy,
- data, která nemusí být jen jednoduchá tabulka.

### Uložení dat do JSONu

```python
import json


students = [
    {"name": "Anna", "score": 92, "passed": True},
    {"name": "Petr", "score": 71, "passed": True},
    {"name": "Eva", "score": 48, "passed": False},
]

with open("students.json", "w", encoding="utf-8") as file:
    json.dump(students, file, ensure_ascii=False, indent=2)
```

Výsledný soubor:

```json
[
  {
    "name": "Anna",
    "score": 92,
    "passed": true
  },
  {
    "name": "Petr",
    "score": 71,
    "passed": true
  }
]
```

`indent=2` dělá výstup čitelnější pro člověka.  
`ensure_ascii=False` zachová české znaky v čitelné podobě.

### Načtení JSONu

```python
import json


with open("students.json", "r", encoding="utf-8") as file:
    students = json.load(file)

for student in students:
    print(student["name"], student["score"])
```

Po načtení máme znovu běžný seznam slovníků, se kterým můžeme dál pracovat.

### Návodný úkol

1. Uložte seznam `students` do souboru `students.json`.
2. Otevřete soubor ručně v editoru a podívejte se, jak vypadá.
3. Změňte v Pythonu skóre jednoho studenta, spusťte program znovu a ověřte změnu v JSONu.

---

## 3. `dump` vs. `dumps`, `load` vs. `loads`

Modul `json` nabízí dvě podobné dvojice funkcí:

| Funkce | Pracuje s |
| --- | --- |
| `json.dump(...)` | zapisuje přímo do souboru |
| `json.dumps(...)` | vrací textový řetězec |
| `json.load(...)` | čte přímo ze souboru |
| `json.loads(...)` | čte z textového řetězce |

Příklad s řetězcem:

```python
import json


student = {"name": "Anna", "score": 92}

json_text = json.dumps(student, ensure_ascii=False)
print(json_text)

loaded_student = json.loads(json_text)
print(loaded_student["name"])
```

### Návodný úkol

Vytvořte slovník s informacemi o jedné knize a:

1. převeďte ho na JSON text pomocí `json.dumps`,
2. text vypište,
3. převeďte ho zpět pomocí `json.loads`,
4. vypište pouze název knihy.

---

## 4. CSV: tabulková data

CSV je vhodné hlavně pro data, která mají podobu tabulky:

```text
name,score,passed
Anna,92,True
Petr,71,True
Eva,48,False
```

CSV je často praktické pro:

- tabulkové exporty,
- otevření v Excelu nebo LibreOffice,
- jednoduché seznamy záznamů se stejnými sloupci.

### Zápis do CSV

```python
import csv


students = [
    {"name": "Anna", "score": 92, "passed": True},
    {"name": "Petr", "score": 71, "passed": True},
    {"name": "Eva", "score": 48, "passed": False},
]

fieldnames = ["name", "score", "passed"]

with open("students.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(students)
```

### Načtení CSV

```python
import csv


with open("students.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    students = list(reader)

print(students)
```

Po načtení CSV budou všechny hodnoty textové řetězce:

```python
print(type(students[0]["score"]))   # str
print(type(students[0]["passed"]))  # str
```

Pokud potřebujeme původní typy, musíme je převést sami:

```python
for student in students:
    student["score"] = int(student["score"])
    student["passed"] = student["passed"] == "True"
```

### Návodný úkol

1. Uložte `students` do `students.csv`.
2. Soubor otevřete ručně a porovnejte ho s JSONem.
3. Načtěte ho přes `csv.DictReader`.
4. Ověřte pomocí `type(...)`, že hodnoty `score` a `passed` jsou po načtení textové řetězce.

---

## 5. Převod mezi CSV a JSON

Jedna z běžných úloh je převést data z jednoho formátu do druhého.

Například CSV → JSON:

```python
import csv
import json


with open("students.csv", "r", encoding="utf-8", newline="") as csv_file:
    reader = csv.DictReader(csv_file)
    students = list(reader)

for student in students:
    student["score"] = int(student["score"])
    student["passed"] = student["passed"] == "True"

with open("students.json", "w", encoding="utf-8") as json_file:
    json.dump(students, json_file, ensure_ascii=False, indent=2)
```

Tady je vidět důležitý rozdíl:

- CSV dobře popisuje tabulku,
- JSON lépe zachovává datové typy a složitější strukturu.

### Návodný úkol

Rozšiřte převod CSV → JSON tak, aby po načtení:

1. spočítal průměrné skóre,
2. vypsal jména studentů, kteří prošli,
3. teprve potom data uložil do JSONu.

---

## 6. Vnořená data: kdy CSV nestačí pohodlně

JSON umí přirozeně ukládat i vnořenou strukturu:

```python
course = {
    "name": "Programování",
    "teacher": "Dr. Novák",
    "students": [
        {"name": "Anna", "score": 92},
        {"name": "Petr", "score": 71},
    ],
}
```

Taková data lze do JSONu uložit přímo:

```python
import json


with open("course.json", "w", encoding="utf-8") as file:
    json.dump(course, file, ensure_ascii=False, indent=2)
```

Do CSV by se stejná struktura zapisovala mnohem hůř, protože CSV očekává plochou tabulku.

### Návodný úkol

Zkuste navrhnout, jak by se dala data z proměnné `course` zapsat do CSV:

- co by bylo na jednom řádku,
- které informace by se musely opakovat,
- co by se v CSV zapisovalo nepohodlněji než v JSONu.

---

## 7. Binární formáty a `pickle`

Kromě textových formátů existují i binární formáty. V Pythonu je jednoduchým příkladem `pickle`:

```python
import pickle


data = {"name": "Anna", "scores": [92, 88, 95]}

with open("data.pkl", "wb") as file:
    pickle.dump(data, file)

with open("data.pkl", "rb") as file:
    loaded_data = pickle.load(file)
```

`pickle` umí uložit Python objekty velmi pohodlně, ale má důležité omezení:

> Nikdy nenačítejte `pickle` data z nedůvěryhodného zdroje.

Na rozdíl od JSONu není `pickle` vhodný jako bezpečný výměnný formát mezi cizími systémy.

### Návodný úkol

Porovnejte po uložení tři soubory:

- `students.json`,
- `students.csv`,
- `data.pkl`.

Zkuste odpovědět:

1. Který soubor snadno přečte člověk?
2. Který se snadno otevře jako tabulka?
3. Který je svázaný hlavně s Pythonem?

---

## 8. Jak vybrat formát

| Potřeba | Vhodný formát |
| --- | --- |
| Jednoduchá tabulka | CSV |
| Stromová nebo vnořená data | JSON, YAML nebo XML |
| Čitelnost pro člověka | JSON, YAML nebo CSV |
| Konfigurační soubor psaný člověkem | YAML nebo JSON |
| Data s výraznou hierarchií a značkami | XML |
| Otevření v tabulkovém procesoru | CSV |
| Zachování Python objektu pro vlastní použití | někdy `pickle` |
| Bezpečná výměna mezi systémy | spíše JSON než `pickle` |

Neexistuje jeden nejlepší formát pro všechno.  
Správná volba závisí na tvaru dat a na tom, kdo je bude později číst.

---

## Shrnutí

Nejdůležitější vzory této hodiny:

```python
json.dump(data, file, ensure_ascii=False, indent=2)
loaded_data = json.load(file)
```

a:

```python
writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(rows)
```

Pokud si z hodiny odnesete jistotu v těchto bodech, máte dobrý základ:

1. serializace převádí data do ukládatelné podoby,
2. JSON je vhodný pro strukturovaná data,
3. CSV je vhodné pro tabulky,
4. při čtení CSV musíme často obnovit správné datové typy,
5. formát volíme podle použití, ne podle zvyku.

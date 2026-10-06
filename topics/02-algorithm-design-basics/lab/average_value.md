# Výpočet průměrné hodnoty

Tento úkol slouží jako úvod do **algoritmizace**, práce se **smyčkami**, **proměnnými** a základního **postupného zpracování dat**.  
Studenti se seznámí s tím, jak lze stejný algoritmus popsat pomocí **diagramu**, **pseudokódu** a **programu v Pythonu**.


## Vývojový diagram

Následující diagram znázorňuje krok za krokem algoritmus pro výpočet průměrné hodnoty z pevně daného počtu vstupů:

```mermaid
flowchart TD
    start([Start]) --> init["N = 5<br/>total = 0"]
    init --> prompt["Vypiš výzvu k zadání N čísel"]
    prompt --> setI["i = 1"]
    setI --> loop{"i <= N?"}
    loop -- ano --> read["Načti x"]
    read --> add["total = total + x"]
    add --> increment["i = i + 1"]
    increment --> loop
    loop -- ne --> average["average = total / N"]
    average --> output["Vypiš average"]
    output --> stop([Konec])
```


## Pseudokód

```
NASTAV N = 5
NASTAV total = 0

VYPIŠ "Zadej N čísel"

PRO i od 1 do N
NAČTI x
total = total + x
KONEC PRO

average = total / N
VYPIŠ average
```

## Ukázková implementace v Pythonu

```python
# number of values (constant)
N = 5

total = 0

print(f"Enter {N} numbers:")

for i in range(1, N + 1):
    x = float(input(f"Value #{i}: "))
    total = total + x

average = total / N
print("Average value:", average)
```

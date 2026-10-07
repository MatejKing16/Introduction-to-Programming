# Domácí příprava: datové typy a vstup/výstup

Krátké zopakování typů, převodů a vstupu/výstupu. Úkol 1 řešte nejprve
bez počítače, pak si odhad ověřte. Ukázková řešení otevřete až po
vlastním pokusu.

## Úkol 1: Jaký typ a jaká hodnota?

Odhadněte typ a hodnotu výsledku. Pokud výraz skončí chybou, napište jakou.

| Výraz | Typ | Hodnota |
|-------|-----|---------|
| `7 / 2` | Float | 3,5 | 
| `7 // 2` | Int | 3 |
| `-7 // 2` | Int | -4 |
| `0.1 + 0.2 == 0.3` | Bool | False |
| `"5" * 3` | Str | 555 |
| `int(3.99)` | int | 4 |
| `bool("False")` | bool | False|
| `"5" + 5` | - | Type error  |

Odhad ověříte například takto: `print(type(7 / 2), 7 / 2)`.

<details>
<summary>Ukázkové řešení</summary>

| Výraz | Typ | Hodnota | Poznámka |
|-------|-----|---------|----------|
| `7 / 2` | `float` | `3.5` | Operátor `/` vrací vždy `float`. |
| `7 // 2` | `int` | `3` | Celočíselné dělení. |
| `-7 // 2` | `int` | `-4` | Zaokrouhluje se **dolů**, ne k nule. |
| `0.1 + 0.2 == 0.3` | `bool` | `False` | `0.1 + 0.2` je `0.30000000000000004` — desetinná čísla nejsou uložena přesně. |
| `"5" * 3` | `str` | `'555'` | Řetězec se zopakuje. |
| `int(3.99)` | `int` | `3` | `int()` desetinnou část usekne, nezaokrouhluje. |
| `bool("False")` | `bool` | `True` | Každý neprázdný řetězec je pravdivý. |
| `"5" + 5` | — | `TypeError` | `str` a `int` nelze sčítat; převod musíme zapsat sami. |

</details>

## Úkol 2: Řádek účtenky

Napište program, který načte název položky, cenu za kus (desetinné číslo)
a počet kusů (celé číslo) a vypíše řádek účtenky s cenami na 2 desetinná
místa.

```
Položka: Káva
Cena za kus [Kč]: 29.90
Počet kusů: 3
Káva: 3 × 29.90 Kč = 89.70 Kč
```

Nápověda: `input()` vrací vždy řetězec. Na dvě desetinná místa vypíšete
číslo pomocí `f"{price:.2f}"`.

<details>
<summary>Ukázkové řešení</summary>

```python
name = input("Položka: ")
price = float(input("Cena za kus [Kč]: "))
quantity = int(input("Počet kusů: "))

total = price * quantity
print(f"{name}: {quantity} × {price:.2f} Kč = {total:.2f} Kč")
```

Výpočet `29.90 * 3` ve skutečnosti dá `89.69999999999999`. Díky formátu
`:.2f` se ale vypíše zaokrouhlená hodnota `89.70`.

</details>

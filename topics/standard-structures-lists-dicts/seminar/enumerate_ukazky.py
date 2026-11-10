# %% [markdown]
# ## 1. Co to je `enumerate()`?
# Funkce `enumerate()` nám umožňuje procházet kolekci (např. seznam) a **zároveň sledovat index (pořadové číslo)** každého prvku.
# Vrací iterátor, který produkuje **n-tice (tuples)** ve tvaru `(index, prvek)`.

# %%
# Základní příklad: Převod na seznam n-tic (tuples)
pismena = ["A", "B", "C"]
vysledek = list(enumerate(pismena))
print(vysledek)

# %% [markdown]
# ## 2. Funkce `next()` a lenivá vyhodnocení (Lazy evaluation)
# Objekt `enumerate` vrací data postupně pomocí iterátoru. Můžeme si vyžádat další prvek ručně přes funkci `next()`.

# %%
znaky = ["x", "y", "z"]
iterator = enumerate(znaky)

print(next(iterator))
print(next(iterator))
# print(next(iterator))  # Další zavolání by vrátilo ('z', 2)

# %% [markdown]
# ## 3. Klasické použití v cyklu `for`
# Nejčastější použití elegantní procházení seznamu s číslováním řádků (bez nutnosti ručně zakládat proměnnou `i = 0`).

# %%
# Vlastní začátek číslování (start=1)
ukoly = ["Koupit chleba", "Uklidit kuchyň", "Napsat kód"]

for cislo, ukol in enumerate(ukoly, start=1):
    print(f"{cislo}. {ukol}")

# %% [markdown]
# ## 4. Kombinace se slovníky (`.items()`)
# Pokročilejší použití, kdy procházíme slovník a potřebujeme znát pořadí položky, její klíč i hodnotu.

# %%
slovnik = {"a": 10, "b": 20}

for i, (klic, hodnota) in enumerate(slovnik.items()):
    print(f"Index: {i}, Klíč: {klic}, Hodnota: {hodnota}")

# %%
ukoly = ["Koupit chleba", "Uklidit kuchyň", "Napsat kód"]
test = enumerate(ukoly)

print(test)

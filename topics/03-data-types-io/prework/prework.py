name = str(input("Zadej položku: "))
price = float(input(f"Zadej cenu {name} v Kč: "))
quantity = int(input(f"Zadej množství {name}: "))

total_cost = round(price * quantity, 2)
print (f"Celková cena za {quantity} kusů položky '{name}' je: {total_cost} Kč")

    
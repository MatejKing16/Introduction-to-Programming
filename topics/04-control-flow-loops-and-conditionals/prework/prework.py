count = 0
max_value = None

while True:
    vstup = (input("Zadej celé číslo: "))

    if vstup == "":
        break 

    if vstup == 0:
        print("nezedali jste číslo")
        continue
    
    if max_value == None or vstup > max_value:
        max_value = vstup

    count = count + 1

    

print(count)
print(max_value)
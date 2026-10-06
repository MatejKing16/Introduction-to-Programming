n = 5
total = 0

for i in (range(0, n)):
    x = float(input(f"Value #{i}: "))
    total = total + x


average = total / n

print ("Total:", total)
print ("Average:", average)
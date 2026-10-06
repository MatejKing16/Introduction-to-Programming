n = 5
positive = 0
negative = 0
zero = 0

for i in range(1, n+1):
    x = float(input(f"Enter a number:{i}:"))
    if x > 0:
        positive += 1
    elif x < 0:
        negative += 1
    else:
        zero += 1


print("Positive numbers:", positive)
print("Negative numbers:", negative)   
print("Zero numbers:", zero)


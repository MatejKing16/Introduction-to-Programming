

b = [1, 2, 3, 4, 5]
x = 0


def Test():
    for i in b:
        print(i)
        i += i
    print("Total:", i)

Test()

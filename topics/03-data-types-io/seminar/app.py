def cost_analysis():

    import math


    speakers = 40000
    screen = 90000
    lights = 40000
    fence = 20000
    stage = 80000
    constructions = 50000
    toilets = 7500
    cables = 15000
    cable_SongMaker_7days = 50000
    cable_SongMaker_1days = cable_SongMaker_7days / 7
    number_of_lights = 5
    donations = 150000



    print("Cost of speakers: ", speakers, "Kč")
    print("Cost of screen: ", screen, "Kč")
    print("Cost of lights: ", lights, "Kč")
    print("Cost of fence: ", fence, "Kč")
    print("Cost of stage: ", stage, "Kč")
    print("Cost of constructions: ", constructions, "Kč")
    print("Cost of toilets: ", toilets, "Kč")
    print("Cost of cables: ", cables, "Kč")

    total_cost = speakers + screen + lights + fence + stage + constructions + toilets + cables

    print("Total cost of the event: ", total_cost, "Kč")

    one_light_cost = lights / number_of_lights
    print("Cost of one light: ", one_light_cost, "Kč")


    difference_cost_cables = cables - cable_SongMaker_1days * 2
    print("Difference in cost of cables for 2 days: ", round(difference_cost_cables), "Kč")

    if donations > total_cost:
        print("The event is profitable. The profit is: ", donations - total_cost, "Kč")
    elif donations < total_cost:
        print("The event is not profitable. The loss is: ", total_cost - donations, "Kč")
    else:
        print("The event breaks even. No profit, no loss.")

    number_of_lights_songMaker = 3
    discount_from_songMaker = math.factorial(number_of_lights_songMaker)
    print("Discount from SongMaker for 3 lights: ", discount_from_songMaker*10, "%")



def analyze_temputerature():
    temputer_2026_5_5 = 22
    temputer_2025_5_5 = 25
    temputer_2024_5_5 = 17
    temputer_2023_5_5 = 14
    temputer_2022_5_5 = 16
    temputer_2021_5_5 = 11

    average_temperature = (temputer_2026_5_5 + temputer_2025_5_5 + temputer_2024_5_5 + temputer_2023_5_5 + temputer_2022_5_5 + temputer_2021_5_5) / 6
    max_temperature = max(temputer_2026_5_5, temputer_2025_5_5, temputer_2024_5_5, temputer_2023_5_5, temputer_2022_5_5, temputer_2021_5_5)
    min_temperature = min(temputer_2026_5_5, temputer_2025_5_5, temputer_2024_5_5, temputer_2023_5_5, temputer_2022_5_5, temputer_2021_5_5)

    print("Average temperature from 2021 to 2026 on May 5th: ", average_temperature, "°C")
    print("Maximum temperature from 2021 to 2026 on May 5th: ", max_temperature, "°C")
    print("Minimum temperature from 2021 to 2026 on May 5th: ", min_temperature, "°C")

    for year, temp in [("2026", temputer_2026_5_5), ("2025", temputer_2025_5_5), ("2024", temputer_2024_5_5), ("2023", temputer_2023_5_5), ("2022", temputer_2022_5_5), ("2021", temputer_2021_5_5)]:
        if temp > 13:
            print(f"The temperature in {year} was above average: 13 °C")
        elif temp < 13:
            print(f"The temperature in {year} was below average: 13 °C")
        else:
            print(f"The temperature in {year} was exactly average: 13 °C")






user = input("Enter your name: ")
password = input("Enter your password: ")

if user == "admin" and password == "admin":
    print("Welcome, admin!")

    cost_analysis()
    analyze_temputerature()
else:
    print("Access denied. Invalid username or password.")

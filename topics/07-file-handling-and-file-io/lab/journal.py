from pathlib import Path

def journal():
    LINES_LIST = 10


    while True:
        file = input("Zadejte nazave souboru nebo příkaz pro upuštění: ")
        
        if file == "/exit":
            print("Program uspěšně opuštěn")
            break            
        else:
            path = Path(file)
            try:
                with open(path,"r",encoding="utf-8") as f:
                    print("Soubor byl ušpěšně načten.")
                    
                    pass
            except FileNotFoundError:
                print("Soubor nexistuje. (FileNotFoundError)")
                break
            
            

            ## Prace se souborem
            while True:
                command = input("Zadej přikaz pro pracovaní se souborem: ")
                if command == "/add":
                    with open(path,"a",encoding="utf-8") as f:
                        while True:
                         
                            add = input("Co chceš přidat nebo command? ")
                            if add == "/exit":
                                print("Psaní ukončeno")
                                break
                            else:
                                f.writelines("\n" + add)
                                print("Uspěšně zapsáno")

                elif command == "/exit":
                    break
                
                elif command == "/list":
                    with open(path,"r",encoding="utf-8") as f:
                        read = f.readlines()
                        
                    for c,i in enumerate(read[-LINES_LIST:], start=max(1, len(read)-LINES_LIST-1)):
                        print(f"{c} - {i}")

                    print(f"\nVypsáno poslendích {LINES_LIST} řádku. Pro změnu použí commad (/change)")
                    
                elif command == "/change":
                    while True:
                        try:
                            LINES_LIST = abs(int(input(f"Akutalni hodnota {LINES_LIST} \n Zadej kolik řadku se vypíše. ")))
                            print(f"Uspěšně přepsano na {LINES_LIST}")
                            pass
                            break
                        except ValueError:
                            print("Špatna hodnota ValueError. Zkus to znova")
                            pass

                elif command == "/delete":
                    while True: 
                        delete = input("Zadej jak řadek chceš odstrani nebo commad (/exit, /delete -m)")

                        if delete == ("/exit"):
                            break

                        elif delete ==("delete -m"):
                            pass

                        else:
                            with open(path, "r", encoding="utf-8") as f:
                                line = f.readlines
                                                             

                
                elif command == "/search":
                    with open(path,"r",encoding="utf-8") as f:
                        while True:
                            search = input("Zadej co hledáš nebo command: ")
                            if search == "/exit":
                                print("Vyhledavaní ukončeno")
                                break
                            else:
                                f.seek(0)
                                for i, line in enumerate(f, start=1):
                                    if search in line:
                                        print(i, "-" ,line)


                elif command == "/help":
                    print("Příkazy: \n/add \n/search \n/list \n/exit")
                else: 
                    print("Nevalidní command zkus to znovu (/help)")








if __name__=="__main__":
    journal()
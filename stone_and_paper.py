import random

choise = ["камень" , "ножницы" , "бумага"]

while True:
    user = input("Введите ваш выбор(для выхода Q):").lower()
    if user not in choise:
        print("Erro")
    elif user == "q":
        break
    computer = random.choice(choise)
    if user == computer:
        print("Ничья")
    elif(user == "камень"and computer == "ножницы" or
         user == "бумага" and computer == "камень" or
         user == "ножницы"and computer == "бумага"):
        print(f"Вы победили! Компьютор выбрал {computer}")
    else:
         print(f"Вы проиграли! Компьютер выбрал".format(computer))






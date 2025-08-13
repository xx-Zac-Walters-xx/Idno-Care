import random
from typing import NoReturn, Dict
from dataclasses import dataclass

@dataclass
class Idno: 
    name: str
    age: int
    health: int
    happiness: int
    hunger: int
    cleanliness: int

@dataclass
class Inventory:
    munny: int
    medicine: dict[str, int]
    toys: dict[str, int]
    food: dict[str, int]
    #changed the list to dict to have the item name and quantity

#store inventory and prices stored as dictionaries, open to easier ideas
# @dataclass
# class Store:
#     #dict of tuple format I'm using, the tuple is the item name and cost and the other int is quantity
#     # toys: dict[tuple[str, int], int]
#     # medicine: dict[tuple[str, int], int]
#     # food: dict[tuple[str, int], int]
#     type: str # food, toys, medicine
#     name: str # treats, kibble, etc.
#     price: int
#     quantity: int

# im crashing out

def create_idno() -> Idno:
    new_name = input("Name your new Idno!\n> ")
    new_idno = Idno(
        name = new_name,
        age = 1,
        health = 50,
        happiness = 50,
        hunger = 0,
        cleanliness = 100,
    )
    print(f"Congratulations on your new Idno! Now you must take care of {new_idno.name}.\nYou must feed it and clean it, and monitor its health and happiness.\nAt the end of each day, you get paid your wage.\nIf {new_idno.name} is in good condition, you earn more munny.\nYou can access the shop to buy supplies to care for {new_idno.name}.\nYou can also access your inventory to see what supplies you already own.")
    return new_idno

def create_save_file() -> str:
    new_file_name = input("New save file name: ")
    formatted_name = new_file_name.replace(" ", "_")
    new_file = open(f"{formatted_name}.txt", "w")
    new_file.close()
    return f"{formatted_name}.txt"

def save_idno_state(idno: Idno, filename: str):
    with open(filename, 'w') as file:
        file.write(f"{idno.name}\n")
        file.write(f"{idno.age}\n")
        file.write(f"{idno.health}\n")
        file.write(f"{idno.happiness}\n")
        file.write(f"{idno.hunger}\n")
        file.write(f"{idno.cleanliness}\n")

# tweaked this function a little bit
def load_idno_state(filename: str) -> Idno:
    try:
        with open(f"{filename}.txt", 'r') as file:
            lines = file.readlines()
            return Idno(
                name = lines[0].strip(),
                age = int(lines[1].strip()),
                health = int(lines[2].strip()),
                happiness = int(lines[3].strip()),
                hunger = int(lines[4].strip()),
                cleanliness = int(lines[5].strip())
            )
    except FileNotFoundError:
        print("File name not found.")

def create_user_inventory():
    user_inventory = Inventory
    user_inventory.munny = 5
    user_inventory.toys = {
        "ball": 0,
        "squeaky toy": 0,
        "stuffed toy": 0
    }
    user_inventory.medicine = {
        "weak medicine":0, 
        "basic medicine":0, 
        "strong medicine":0, 
        "xtra strong medicine":0
    }
    user_inventory.food = {
        "treat":0, 
        "kibble":0, 
        "steak":0
    }
    return user_inventory

def get_paid(user_inventory: Inventory, idno_status: Idno):
    #editing so that the happier/healthier idno is, the more money the user earns
    wage = 5

    if idno_status.cleanliness >= 75:
        wage += 1
    elif idno_status.cleanliness <= 25:
        wage -= 1

    if idno_status.happiness >= 75:
        wage += 1
    elif idno_status.happiness <= 25:
        wage -= 1

    if idno_status.health >= 75:
        wage += 1
    elif idno_status.health <= 25:
        wage -= 1

    user_inventory.munny += wage
    print(f"You've earned {wage} munny!")

def create_store_inventory():
    #formatted as a dict with a tuple (item name, price): stock quantity,set all at 10 for now can change or randomize later
    # new_store = Store
    daily_store = []
    # new_store.toys = {
    #     ("ball", 1): 10,
    #     ("squeaky toy", 3): 10,
    #     ("stuffed toy", 5): 10
    # }
    # new_store.medicine = {
    #     ("weak medicine", 1): 10, 
    #     ("basic medicine", 3): 10, 
    #     ("strong medicine", 5): 10, 
    #     ("xtra strong medicine", 7): 10
    # }
    # new_store.food = {
    #     ("treat", 1): 10, 
    #     ("kibble", 3): 10, 
    #     ("steak", 5): 10
    # }

    # i attempted to reformat the inventory into a list of dictionaries and just get rid of the dataclass element of it
    # because i couldnt figure out how to access certain values for the process of buying things from the shop in the check_shop() function
    # its not as pretty as it was before but i got it working soooo
    ball = {"type": "toys", "name": "ball", "price": 1, "quantity": 10}
    squeaky_toy = {"type": "toys", "name": "squeaky toy", "price": 3, "quantity": 10}
    stuffed_toy = {"type": "toys", "name": "stuffed toy", "price": 5, "quantity": 10}
    weak = {"type": "medicine", "name": "weak medicine", "price": 1, "quantity": 10}
    basic = {"type": "medicine", "name": "basic medicine", "price": 3, "quantity": 10}
    strong = {"type": "medicine", "name": "strong medicine", "price": 5, "quantity": 10}
    xtra_strong = {"type": "medicine", "name": "xtra strong medicine", "price": 7, "quantity": 10}
    treat = {"type": "food", "name": "treat", "price": 1, "quantity": 10}
    kibble = {"type": "food", "name": "kibble", "price": 3, "quantity": 10}
    steak = {"type": "food", "name": "steak", "price": 5, "quantity": 10}

    daily_store.append(ball)
    daily_store.append(squeaky_toy)
    daily_store.append(stuffed_toy)
    daily_store.append(weak)
    daily_store.append(basic)
    daily_store.append(strong)
    daily_store.append(xtra_strong)
    daily_store.append(treat)
    daily_store.append(kibble)
    daily_store.append(steak)

    return daily_store

def check_shop(user_inventory: Inventory, store_inventory: list, category_name: str):
    while True:
        print(f"Available {category_name}:")
        for i in store_inventory:
            if i["type"] == f"{category_name}":
                print(f"x{i["quantity"]} {i["name"]}, {i["price"]} munny")

        print(f"You have {user_inventory.munny} munny to spend.")
        choice = input(f"Which {category_name} would you like to buy? Enter [exit] to leave the shop.\n> ")
            
        if choice.lower() == "exit":
            break
        
        item_key = None
        for item in store_inventory:
            if item["name"].lower() == choice.lower():
                item_key = item
                break
                
        if item_key is None:
            print("Invalid choice.")
            continue

        product = item_key["name"]
        cost = item_key["price"]
        stock_quantity = item_key["quantity"]

        
        if stock_quantity > 0:
            if user_inventory.munny >= cost:
                user_inventory.munny -= cost
                stock_quantity -= 1
                # I CANNOT FIGURE OUT HOW TO UPDATE THE PRODUCT QUANTITY IN THE USER INVENTORY PLS HELP
                print(f"You bought {product}!")
                
            else:
                print("You don't have enough munny!")
        else:
            print("Item not in stock.")

def feed_idno(user_inventory: Inventory, idno: Idno):
    while True:
        print(f"What would you like to feed {idno.name}? Enter [exit] to quit feeding your Idno.")
        for item in user_inventory.food.items():
            print(f"{item[0].title()} x{item[1]}")
        choice = input("> ").strip().lower()

        if choice == "exit":
            break

        item_key = None
        for item in user_inventory.food.items():
            if item[0].lower() == choice:
                item_key = item[0]
                break

        if item_key is None:
            print("Invalid choice.")
            continue
        
        if user_inventory.food.get(item_key, 0) < 1:
            print("You don't have any of that food to use.")
            continue

        print(f"{idno.name} is less hungry now that they've had a {item_key} to eat.")
        if item_key.lower() == "treat":
            idno.hunger -= 5
            idno.happiness += 5                
        elif item_key.lower() == "kibble":
            idno.hunger -= 10
        elif item_key.lower() == "steak":
            idno.hunger -= 25
            idno.happiness += 10
        
        idno.hunger = max(0, min(idno.hunger, 100))

        user_inventory.food[item_key] = max(0, user_inventory.food[item_key] - 1)

        print(f"{idno.name}'s hunger is now {idno.hunger}/100.")

def play_with_idno(user_inventory: Inventory, idno: Idno):

    while True:
        print(f"How would you like to play with your Idno? Enter [exit] to quit playing with {idno.name}.")
        for item in user_inventory.toys.items():
            print(f"{item[0].title()} x{item[1]}")
        choice = input("> ").strip().lower()

        if choice == "exit":
            break

        item_key = None
        for item in user_inventory.toys.items():
            if item[0].lower() == choice:
                item_key = item[0]
                break

        if item_key is None:
            print("Invalid choice.")
            continue
        
        if user_inventory.toys.get(item_key, 0) < 1:
            print("You don't have any of that toy to use.")
            continue

        print(f"{idno.name} is happier now that they have a {item_key} to play with.")
        if item_key.lower() == "squeaky toy":
            idno.happiness += 5                    
        elif item_key.lower() == "ball":
            idno.happiness += 10
        elif item_key.lower() == "stuffed toy":
            idno.happiness += 20
        idno.happiness = max(0, min(idno.happiness, 100))

        user_inventory.toys[item_key] = max(0, user_inventory.toys[item_key] - 1)

        print(f"{idno.name}'s happiness is now {idno.happiness}/100.")

def clean_idno(idno: Idno):
    idno.cleanliness += 20 # i need to fix this so that the max is 100 cause we dont need it to be higher than that
    print(f"{idno.name} is now a bit cleaner!")

def administer_medicine(user_inventory: Inventory, idno: Idno):
    while True:
        print(f"What medicine would you like to give {idno.name}? Enter [exit] to stop administering medicine.")
        for item in user_inventory.medicine.items():
            print(f"{item[0].title()} x{item[1]}")
        choice = input("> ").strip().lower()

        if choice == "exit":
            break

        item_key = None
        for item in user_inventory.medicine.items():
            if item[0].lower() == choice:
                item_key = item[0]
                break

        if item_key is None:
            print("Invalid choice.")
            continue
        
        if user_inventory.medicine.get(item_key, 0) < 1:
            print("You don't have any of that medicine to use.")
            continue

        print(f"{idno.name} is feeling better after receiving the medicine.")
        if item_key.lower() == "weak":
            idno.health += 20                   
        elif item_key.lower() == "basic":
            idno.health += 40
        elif item_key.lower() == "strong":
            idno.health += 60
        elif item_key.lower() == "xtra strong":
            idno.health += 80
        idno.health = max(0, min(idno.health, 100))

        user_inventory.medicine[item_key] = max(0, user_inventory.medicine[item_key] - 1)

        print(f"{idno.name}'s health is now {idno.health}/100.")

def check_inventory(user_inventory: Inventory) -> None:
    print("Inventory:")
    print(f"Munny: {user_inventory.munny}")
    for item, quantity in user_inventory.medicine.items():
        print(f"{item}: {quantity}")
    for item, quantity in user_inventory.toys.items():
        print(f"{item}: {quantity}")
    for item, quantity in user_inventory.food.items():
        print(f"{item}: {quantity} servings")

def main():

    # user_inventory = create_user_inventory()
    # daily_store = create_store_inventory()
    # check_shop(user_inventory, daily_store, "food")
    # was just testing functionality of the shopping process, it works until you get to the part where the product would be added to your inventory

    while True:
        try:
            logging_in = int(input("Welcome to the Idno simulator! Are you a returning player, or would you like to start a new save file?\n[1] load save file\n[2] create save file\n> "))
            if logging_in == 1:
                filename = input("Please enter the name of your existing save file.\n> ")
                idno = load_idno_state(filename)
                if idno:
                    print(f"Welcome back! {idno.name} missed you.")
                    break
                else:
                    filename = create_save_file()
                    idno = create_idno()
                    save_idno_state(idno, filename)
                    break
            elif logging_in == 2:
                filename = create_save_file()
                idno = create_idno()
                save_idno_state(idno, filename)
                break
            else:
                print("Input must be either [1] or [2].")
        except ValueError:
            print("Input must be either [1] or [2].")

    user_inventory = create_user_inventory()
    daily_store = create_store_inventory()

    num_of_actions = 5
    
    print("\nWhat would you like to do?\n[1] check shop\n[2] check inventory\n[3] feed idno\n[4] clean idno\n[5] play with idno\n[6] administer medicine\n[7] end day\n[8] save and exit")
    action = int(input("> "))
    while action != 8:
        if num_of_actions > 0:
            if action == 1:
                category = input("What are you looking to buy?\n[food]\n[toys]\n[medicine]\n> ")
                check_shop(user_inventory, daily_store, category)
                num_of_actions -= 1
            elif action == 2:
                check_inventory(user_inventory)
            elif action == 3:
                feed_idno(user_inventory, idno)
                num_of_actions -= 1
            elif action == 4:
                clean_idno(user_inventory, idno)
                num_of_actions -= 1
            elif action == 5:
                play_with_idno(user_inventory, idno)
                num_of_actions -= 1
            elif action == 6:
                administer_medicine(user_inventory, idno)
                num_of_actions -= 1
            elif action == 7:
                print("You have chosen to end the day.")
                #end day / adjust
                num_of_actions = 0

            print("What would you like to do?\n[1] check shop\n[2] check inventory\n[3] feed idno\n[4] clean idno\n[5] play with idno\n[6] administer medicine\n[7] end day\n[8] save and exit")
            action = int(input("> "))

        else:
            print("You are out of actions for the day!")
            #insert function to end the day and adjust stats

    if action == 8:
        print("Ending current day and saving stats...")
        #end day / adjust
        save_idno_state(idno, filename)

if __name__ == "__main__":
    main()

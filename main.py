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

#not sure what all we need to track for the inventory
@dataclass
class Inventory:
    munny: int
    medicine: dict[str, int]
    toys: dict[str, int]
    food: dict[str, int]
    #changed the list to dict to have the item name and quantity

#store inventory and prices stored as dictionaries, open to easier ideas
@dataclass
class Store:
    #dict of tuple format I'm using, the tuple is the item name and cost and the other int is quantity
    toys: dict[tuple[str, int], int]
    medicine: dict[tuple[str, int], int]
    food: dict[tuple[str, int], int]

def create_idno() -> Idno:
    new_name = input("Name your new idno!\n> ")
    new_idno = Idno(
        name = new_name,
        age = 1,
        health = 50,
        happiness = 50,
        hunger = 0,
        cleanliness = 100,
    )
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

def load_idno_state(filename: str) -> Idno:
    try:
        with open(filename, 'r') as file:
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
        return create_idno()

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
    print({f"You've earned {wage} munny!"})

def create_store_inventory(new_store: Store):
    #formatted as a dict with a tuple (item name, price): stock quantity,set all at 10 for now can change or randomize later
    new_store.toys = {
        ("ball", 1): 10,
        ("squeaky toy", 3): 10,
        ("stuffed toy", 5): 10
    }
    new_store.medicine = {
        ("weak", 1): 10, 
        ("basic", 3): 10, 
        ("strong", 5): 10, 
        ("xtra strong", 7): 10
    }
    new_store.food = {
        ("treat", 1): 10, 
        ("kibble", 3): 10, 
        ("steak", 5):10
    }

def check_shop(user_inventory: Inventory, store_inventory: dict, category_name:str):
    while True:
        print(f"Available {category_name}:")
        for (item, price), qty in store_inventory.items():
            print(f"  {qty}x {item}(s): {price} munny")

        print(f"You have {user_inventory.munny} munny to spend.")
        choice = input(f"Which {category_name} would you like to buy? Enter <exit> to leave the shop.")
        
        if choice.lower() == "exit":
            break
        
        item_key = None
        for item in store_inventory:
            if item[0].lower() == choice.lower():
                item_key = item
                break
                
        if item_key is None:
            print("Invalid choice.")
            continue

        product = (item_key[0])
        cost = (item_key[1])
        stock_quantity = int(store_inventory[item_key])

        
        if stock_quantity > 0:
            if user_inventory.munny >= cost:
                user_inventory.munny -= cost
                store_inventory[item_key] -= 1
                inventory_addition = getattr(user_inventory, category_name)
                inventory_addition[product] = inventory_addition.get(product, 0) + 1
                print(f"You bought {product}!")
                
            else:
                print("You don't have enough munny!")
        else:
            print("Item not in stock.")

def feed_idno(user_inventory: Inventory, idno: Idno):
    while True:
        print(f"What would you like to feed {idno.name}? Enter <exit> to quit feeding your Idno.")
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

        print(f"{idno.name} is less hungry now that they have a {item_key} to eat.")
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
        print("How would you like to play with your Idno? Enter <exit> to quit playing with Idno.")
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

def administer_medicine(user_inventory: Inventory, idno: Idno):
    while True:
        print(f"What medicine would you like to give {idno.name}? Enter <exit> to stop administering medicine.")
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



def get_inventory(user_inventory: Inventory) -> None:
    print("Inventory:")
    print(f"  Munny: {user_inventory.munny}")
    for item, quantity in user_inventory.medicine.items():
        print(f"{item}: {quantity}")
    for item, quantity in user_inventory.toys.items():
        print(f"{item}: {quantity}")
    for item, quantity in user_inventory.food.items():
        print(f"{item}: {quantity} servings")

#starting on the basic structure, please make changes if needed
def main():

    filename = create_save_file()
    idno = create_idno()
    save_idno_state(idno, filename)

    print(f"""Congratulations on your new Idno! Now you must take care of {idno.name}.
            You must feed it and clean it, and monitor its health and happiness.
            At the end of each day, you get paid your wage.
            If {idno.name} is in good condition, you earn more munny.
            You can access the shop to buy supplies to care for {idno.name}.
            You can also access your inventory to see what supplies you already own.""")
    #probably need to format this ginormous string to fit better in the terminal but im too lazy
    #fixed formatting with triple quotes which preserve the spacing and line breaks with \n

if __name__ == "__main__":
    main()

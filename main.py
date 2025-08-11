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

def get_paid(user_inventory: Inventory):
    user_inventory.munny += 5
    print("You received 5 munny!")

def create_store_inventory(new_store: Store):
    #formatted as a dict with a tuple (item name, price): stock quantity,set all at 10 for now can change or randomize later
    new_store.toys = {
        ("Ball", 1): 10,
        ("Squeaky toy", 3): 10,
        ("Stuffed toy", 5): 10
    }
    new_store.medicine = {
        ("Weak", 1): 10, 
        ("Basic", 3): 10, 
        ("Strong", 5): 10, 
        ("Xtra strong", 7): 10
    }
    new_store.food = {
        ("Treat", 1): 10, 
        ("Kibble", 3): 10, 
        ("Steak", 5):10
    }

def buy_item(user_inventory: Inventory, store_inventory: dict, category_name:str):
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



def get_inventory(user_inventory: Inventory) -> None:
    print("Inventory:")
    print(f"  Munny: {user_inventory.munny}")
    for item, quantity in user_inventory.medicine.items():
        print(f"{item}: {quantity}")
    for item, quantity in user_inventory.toys.items():
        print(f"{item}: {quantity}")
    for item, quantity in user_inventory.food.items():
        print(f"{item}: {quantity} servings")

def main():
    pass

if __name__ == "__main__":
    main()

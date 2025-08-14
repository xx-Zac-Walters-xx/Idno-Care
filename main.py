import random
from dataclasses import dataclass, asdict
import json

@dataclass
class Idno: 
    name: str
    age: int
    health: int
    happiness: int
    nourishment: int
    cleanliness: int

@dataclass
class Inventory:
    munny: int
    medicine: dict[str, int]
    toys: dict[str, int]
    food: dict[str, int]
    #changed the list to dict to have the item name and quantity

#store inventory and prices stored as dictionaries, open to easier ideas
@dataclass
class Store_item:

    type: str # food, toys, medicine
    name: str # treats, kibble, etc.
    price: int
    quantity: int


random_events = ["mess", "sickness", "growth", "sad", "happy"]

def get_random_event_message(idno: Idno) -> str:
    event_type = random.choice(random_events)
    if event_type == "mess":
        idno.cleanliness -= 10
        with open("mess.txt", "r") as file:
            return random.choice(file.readlines()).strip()
    elif event_type == "sickness":
        idno.health -= 10
        with open("sickness.txt", "r") as file:
            return random.choice(file.readlines()).strip()
    elif event_type == "growth":
        idno.age += 1
        with open("growth.txt", "r") as file:
            return random.choice(file.readlines()).strip()
    elif event_type == "sad":
        idno.happiness -= 10
        with open("sad.txt", "r") as file:
            return random.choice(file.readlines()).strip()
    elif event_type == "happy":
        idno.happiness += 10
        with open("happy.txt", "r") as file:
            return random.choice(file.readlines()).strip()
    else:
        return "Unknown event."

def create_idno() -> Idno:
    new_name = input("Name your new Idno!\n> ")
    new_idno = Idno(
        name = new_name,
        age = 1,
        health = 50,
        happiness = 50,
        nourishment = 100,
        cleanliness = 100,
    )
    print(f"Congratulations on your new Idno! Now you must take care of {new_idno.name}.\nYou must feed it and clean it, and monitor its health and happiness.\nAt the end of each day, you get paid your wage.\nIf {new_idno.name} is in good condition, you earn more munny.\nYou can access the shop to buy supplies to care for {new_idno.name}.\nYou can also access your inventory to see what supplies you already own.\nGood luck and have fun!")
    return new_idno

def save_idno_state(idno: Idno, filename: str):
    with open(f"{filename}.txt", 'w') as file:
        file.write(f"{idno.name}\n")
        file.write(f"{idno.age}\n")
        file.write(f"{idno.health}\n")
        file.write(f"{idno.happiness}\n")
        file.write(f"{idno.nourishment}\n")
        file.write(f"{idno.cleanliness}\n")

def save_user_inventory(inv: Inventory, filename: str):
    inv_filename = f"{filename}_inv.json"
    with open(inv_filename, "w") as f:
        json.dump(asdict(inv), f, indent=4)

def load_user_inventory(filename: str):
    inv_filename = f"{filename}_inv.json"
    try:
        with open(inv_filename, "r") as f:
            data = json.load(f)
        return Inventory(**data)
    except FileNotFoundError:
        print("File name not found.")


# tweaked this function a little bit
def load_idno_state(filename: str):
    try:
        with open(f"{filename}.txt", 'r') as file:
            lines = file.readlines()
            return Idno(
                name = lines[0].strip(),
                age = int(lines[1].strip()),
                health = int(lines[2].strip()),
                happiness = int(lines[3].strip()),
                nourishment = int(lines[4].strip()),
                cleanliness = int(lines[5].strip())
            )
    except FileNotFoundError:
        print("File name not found.")

def create_user_inventory() -> Inventory:
    return Inventory(
        munny=5,
        toys={"ball": 0, "squeaky toy": 0, "stuffed toy": 0},
        medicine={
            "weak medicine": 0,
            "basic medicine": 0,
            "strong medicine": 0,
            "xtra strong medicine": 0,
        },
        food={"treat": 0, "kibble": 0, "steak": 0},
    )

def get_paid(user_inventory: Inventory, idno: Idno):
    #editing so that the happier/healthier idno is, the more money the user earns
    wage = 5

    if idno.cleanliness >= 75:
        wage += 1
    elif idno.cleanliness <= 25:
        wage -= 1

    if idno.happiness >= 75:
        wage += 1
    elif idno.happiness <= 25:
        wage -= 1

    if idno.health >= 75:
        wage += 1
    elif idno.health <= 25:
        wage -= 1

    if idno.nourishment >= 75:
        wage += 1
    elif idno.nourishment <= 25:
        wage -= 1

    user_inventory.munny += wage
    print(f"You've earned {wage} munny!")

def get_idno(idno: Idno):
    print(f"Here's how {idno.name} is doing:\n{idno.age} days old\nHealth: {idno.health}/100\nHappiness: {idno.happiness}/100\nHunger: {idno.nourishment}/100\nCleanliness: {idno.cleanliness}/100")

def create_store_inventory():

    #formatted as a dict with a tuple (item name, price): stock quantity,set all at 10 for now can change or randomize later
    # new_store = Store
    
    ball = Store_item("toys","ball", 1, random.randint(1, 5))
    squeaky_toy = Store_item("toys", "squeaky toy", 3, random.randint(1, 4))
    stuffed_toy = Store_item("toys", "stuffed toy", 5, random.randint(1, 3))
    weak =  Store_item("medicine", "weak medicine", 1, random.randint(1, 5))    
    basic = Store_item("medicine", "basic medicine", 3, random.randint(1, 4))
    strong = Store_item("medicine", "strong medicine", 5, random.randint(1, 3))
    xtra_strong = Store_item("medicine", "xtra strong medicine", 7, 1)
    treat = Store_item("food", "treat", 1, random.randint(1, 10))
    kibble = Store_item("food", "kibble", 3, random.randint(1, 5))
    steak = Store_item("food", "steak", 5, random.randint(1, 2))
    daily_store = [ball, squeaky_toy, stuffed_toy, weak, basic, strong, xtra_strong, treat, kibble, steak]

    return daily_store

def check_shop(user_inventory: Inventory, store_inventory: list, category_name: str):
    while True:
        print(f"Available {category_name}:")
        for i in store_inventory:
            if i.type == f"{category_name}":
                print(f"x{i.quantity} {i.name}, {i.price} munny")

        print(f"You have {user_inventory.munny} munny to spend.")
        choice = input(f"Which {category_name} would you like to buy? Enter [exit] to leave the shop.\n> ")
            
        if choice.lower() == "exit":
            break
        
        item_key = None
        for item in store_inventory:
            if item.name.lower() == choice.lower():
                item_key = item
                break
                
        if item_key is None:
            print("Invalid choice.")
            continue

        product = item_key.name
        cost = item_key.price
        stock_quantity = item_key.quantity

        if stock_quantity > 0:
            if user_inventory.munny >= cost:
                user_inventory.munny -= cost

                for item in store_inventory:
                    if product == item.name:
                        item.quantity -=1

                update_user_inv = getattr(user_inventory, category_name)
                update_user_inv[product] = update_user_inv.get(product, 0) + 1
                
                # I CANNOT FIGURE OUT HOW TO UPDATE THE PRODUCT QUANTITY IN THE USER INVENTORY PLS HELP
                print(f"You bought {product}!")
                
            else:
                print("You don't have enough munny!")
        else:
            print("Item not in stock.")

def feed_idno(user_inventory: Inventory, idno: Idno):
    while True:
        print(f"What would you like to feed {idno.name}? Enter [exit] to quit feeding your Idno.\n> ")
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
            idno.nourishment += 5
            idno.happiness += 5                
        elif item_key.lower() == "kibble":
            idno.nourishment += 10
        elif item_key.lower() == "steak":
            idno.nourishment += 25
            idno.happiness += 10
        
        idno.nourishment = max(idno.nourishment, 100)

        user_inventory.food[item_key] = max(0, user_inventory.food[item_key] - 1)

        print(f"{idno.name}'s nourishment is now {idno.nourishment}/100.")

def play_with_idno(user_inventory: Inventory, idno: Idno):

    while True:
        print(f"How would you like to play with your Idno? Enter [exit] to quit playing with {idno.name}.\n> ")
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
    idno.cleanliness += 20
    idno.cleanliness = min(idno.cleanliness, 100)
    print(f"{idno.name} is now a bit cleaner! Cleanliness is now {idno.cleanliness}/100.")

def administer_medicine(user_inventory: Inventory, idno: Idno):
    while True:
        print(f"What medicine would you like to give {idno.name}? Enter [exit] to stop administering medicine.\n> ")
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
        if item_key.lower() == "weak medicine":
            idno.health += 20                   
        elif item_key.lower() == "basic medicine":
            idno.health += 40
        elif item_key.lower() == "strong medicine":
            idno.health += 60
        elif item_key.lower() == "xtra strong medicine":
            idno.health += 80
        idno.health = max(0, min(idno.health, 100))

        user_inventory.medicine[item_key] = max(0, user_inventory.medicine[item_key] - 1)

        print(f"{idno.name}'s health is now {idno.health}/100.")

def check_inventory(user_inventory: Inventory):
    print("Inventory:")
    print(f"Munny: {user_inventory.munny}")
    for item, quantity in user_inventory.medicine.items():
        print(f"{item}: {quantity}")
    for item, quantity in user_inventory.toys.items():
        print(f"{item}: {quantity}")
    for item, quantity in user_inventory.food.items():
        print(f"{item}: {quantity} servings")

def main():

    while True:
        try:
            logging_in = int(input("Welcome to the Idno simulator! Are you a returning player, or would you like to start a new save file?\n[1] load save file\n[2] create save file\n> "))
            if logging_in == 1:
                filename = input("Please enter the name of your existing save file.\n> ")
                idno = load_idno_state(filename)
                if idno:
                    user_inventory = load_user_inventory(filename)
                    print(f"Welcome back! {idno.name} missed you.")
                    break
                else:
                    idno = create_idno()
                    save_idno_state(idno, filename)
                    user_inventory = create_user_inventory()
                    save_user_inventory(user_inventory, filename)
                    break
            elif logging_in == 2:
                #filename = create_save_file()
                filename = input("New save file name: ")
                idno = create_idno()
                save_idno_state(idno, filename)
                user_inventory = create_user_inventory()
                save_user_inventory(user_inventory, filename)
                break
            else:
                print("Input must be either [1] or [2].")
        except ValueError:
            print("Input must be either [1] or [2].")


    while True:
        print("\nIt's a new day!")
        
        get_paid(user_inventory, idno)
        daily_store = create_store_inventory()
        idno.age += 1
        idno.nourishment -= 10
        idno.cleanliness -= 5
        num_of_actions = 5
        random_event_message = get_random_event_message(idno)
        print(f"\n{random_event_message}\n")

        # print(f"\nWhat would you like to do? {num_of_actions} actions left.\n[1] check shop\n[2] check inventory\n[3] feed idno\n[4] clean idno\n[5] play with idno\n[6] administer medicine\n[7] end day\n[8] save and exit")
        # action = int(input("> "))

        try:
            while num_of_actions > 0:
                get_idno(idno)
                print(f"\nWhat would you like to do? {num_of_actions} actions left for today.\n[1] check shop\n[2] check inventory\n[3] feed idno\n[4] clean idno\n[5] play with idno\n[6] administer medicine\n[7] end day\n[8] save and exit")
                action = int(input("> "))
                if action == 1:
                    category = input("What are you looking to buy?\n[food]\n[toys]\n[medicine]\n> ")
                    check_shop(user_inventory, daily_store, category)
                    num_of_actions -= 1
                    continue
                elif action == 2:
                    check_inventory(user_inventory)
                    continue
                elif action == 3:
                    feed_idno(user_inventory, idno)
                    num_of_actions -= 1
                    continue
                elif action == 4:
                    clean_idno(user_inventory, idno)
                    num_of_actions -= 1
                    continue
                elif action == 5:
                    play_with_idno(user_inventory, idno)
                    num_of_actions -= 1
                    continue
                elif action == 6:
                    administer_medicine(user_inventory, idno)
                    num_of_actions -= 1
                    continue
                elif action == 7:
                    print("You have chosen to end the day.")
                    num_of_actions = 0
                elif action == 8:
                    # num_of_actions = 0
                    print("Ending current day and saving stats...")
                    save_idno_state(idno, filename)
                    save_user_inventory(user_inventory, filename)
                    break
                else:
                    print("Input must be an integer between 1 and 8.")
            
            if action == 8:
                break

            if num_of_actions == 0:
                print("You are out of actions for the day!")

        except ValueError:
            print("Input must be an integer between 1 and 8.")

if __name__ == "__main__":
    main()

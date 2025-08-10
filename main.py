import random 
from typing import NoReturn
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
    medicine: list[str]
    toys: list[str]
    food_units: int

#store inventory and prices stored as dictionaries, open to easier ideas
@dataclass
class Store:
    toys: dict[str, int] 
    medicine: dict[str, int]
    food: dict[int, int]

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

def save_idno_state(idno: Idno, filename: str) -> NoReturn:
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

def get_paid(user_inventory: Inventory) -> NoReturn:
    user_inventory.munny += 5
    print("You received 5 munny!")

def buy_medicine(user_inventory: Inventory, store: Store) -> NoReturn:
    while True:
        print("Available medicine:")
        for item, price in store.medicine.items():
            print(f"  {item}: {price} munny")
        choice = input("Which medicine would you like to buy? ")
        if choice in store.medicine:
            if user_inventory.munny >= store.medicine[choice]:
                user_inventory.munny -= store.medicine[choice]
                user_inventory.medicine.append(choice)
                print(f"You bought {choice}!")
                break
            else:
                print("You don't have enough munny! Press [exit] to leave.")
        elif choice.lower() == "exit":
            break
        else:
            print("Invalid choice.")

def get_inventory(user_inventory: Inventory) -> None:
    print("Inventory:")
    print(f"  Munny: {user_inventory.munny}")
    print(f"  Medicine: {', '.join(user_inventory.medicine)}")
    print(f"  Toys: {', '.join(user_inventory.toys)}")
    print(f"  Food Units: {user_inventory.food_units}")

def main():
    pass

if __name__ == "__main__":
    main()

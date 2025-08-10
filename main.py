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

def main():
    pass

if __name__ == "__main__":
    main()

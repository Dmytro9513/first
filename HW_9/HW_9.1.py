import sys # ;D

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Invalid input. Please try again."

    return inner

contacts = {}

@input_error
def add_contact(command):
    _, name, phone = command.split()
    contacts[name] = phone
    return f"Contact '{name}' with phone '{phone}' has been added."

@input_error
def change_phone(command):
    _, name, phone = command.split()
    contacts[name] = phone
    return f"Phone number for contact '{name}' has been changed to '{phone}'."

@input_error
def show_phone(command):
    _, name = command.split()
    return f"Phone number for contact '{name}': {contacts[name]}"

def show_all_contacts():
    if not contacts:
        return "No contacts found."
    result = "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
    return result

def main():
    print("How can I help you?")

    while True:
        command = input("> ").lower()

        if command == "good bye" or command == "close" or command == "exit":
            print("Good bye!")
            break
        elif command == "hello" or command == "hi" or command == "hallo":
            print("How can I help you?")
        elif command.startswith("add"):
            response = add_contact(command)
            print(response)
        elif command.startswith("change"):
            response = change_phone(command)
            print(response)
        elif command.startswith("phone"):
            response = show_phone(command)
            print(response)
        elif command == "show all":
            response = show_all_contacts()
            print(response)
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()

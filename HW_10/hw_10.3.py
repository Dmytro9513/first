import sys
from collections import UserDict


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


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(
        self, name: str, phone: Phone = None
    ):  # телефон не обовязковий агрумент, тому може бути і None
        self.name = name
        self.phones = []  # по замовчюванню стовримо пустий список
        if phone:
            self.phones.append(phone)  # якщо телефон прийде, то додамо в список

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number.value not in [phone.value for phone in self.phones]:
            self.phones.append(phone_number)

    def find_phone(self, value):
        found_phones = [phone for phone in self.phones if value in phone.value]
        if found_phones:
            return [str(phone) for phone in found_phones]
        else:
            return "Phone not found."

    def delete_phone(self, phone_value):
        for phone in self.phones:
            if phone_value == phone.value:
                self.phones.remove(phone)
                return f"Phone '{phone_value}' deleted."
        return f"Phone '{phone_value}' not found."

    def edit_phone(self, old_phone_value, new_phone_value):
        for phone in self.phones:
            if old_phone_value == phone.value:
                phone.value = new_phone_value
                return f"Phone '{old_phone_value}' updated to '{new_phone_value}'."
        return f"Phone '{old_phone_value}' not found."


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)

    def show_all_contacts(self):
        if not self.data:
            return "No contacts found."
        result = "\n".join(
            [f"{name}: {record.phones[0].value}" for name, record in self.data.items()]
        )
        return result


def main():
    address_book = AddressBook()

    while True:
        command = input("> ").lower()

        if command == "bye" or command == "close" or command == "exit":
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
        elif command == "show all" or command == "show list":
            response = show_all_contacts()
            print(response)
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
    name = Name("Bill")
    phone = Phone("1234567890")
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)
    assert isinstance(ab["Bill"], Record)
    assert isinstance(ab["Bill"].name, Name)
    assert isinstance(ab["Bill"].phones, list)
    assert isinstance(ab["Bill"].phones[0], Phone)
    assert ab["Bill"].phones[0].value == "1234567890"
    print("All Ok)")

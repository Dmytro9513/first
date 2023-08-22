from datetime import datetime
from collections import UserDict

class Field:
    def __init__(self, value = None):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self,instance, value):
        self.value = value


class Phone(Field):
    def __set__(self, instance, value):
        self.value = value

class Birthday(Field):
    def __set__(self, instance, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD")
        self.value = value

class Name(Field):
    def __set__(self,instance, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self.value = value

class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            self.phones.remove(old_phone)
            self.add_phone(new_phone)

    def edit_birthday(self, new_birthday):
        try:
            datetime.strptime(new_birthday, "%Y-%m-%d")
            self.birthday = Birthday(new_birthday)
        except ValueError:
            print("Invalid birthday format. Use YYYY-MM-DD")

    def show_phones(self):
        return [phone.value for phone in self.phones]

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, int(self.birthday.value[5:7]), int(self.birthday.value[8:10]))
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left
        return None

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search_by_name(self, name):
        results = []
        for record in self.data.values():
            if name.lower() in record.name.value.lower():
                results.append(record)
        return results

    def search_by_phone(self, phone):
        results = []
        for record in self.data.values():
            if any(phone in p.value for p in record.phones):
                results.append(record)
        return results

if __name__ == "__main__":
    book = AddressBook()

    while True:
        command = input(">").lower()

        if command in ["bye", "good bye", "exit"]:
            print("До побачення,повертайтесь!")
            break
        elif command in ["hi", "hello"]:
            print("Вітаю,друже!")
        elif command == "add":
            name = input("Enter name: ").lower()
            phone = input("Enter phone number: ")
            while not phone.isdigit() or len(phone) != 10:
                print("Цей номер не є дійсний.Ведіть 10 цифр.")
                phone = input("Enter phone number: ")
            if name.lower() in book.data:
                print("Контакт з цим імʼям вже створений!")
            else:
                record = Record(name, phone)
                book.add_record(record)
                print("Contact added.")
        elif command == "add_birthday":
            name = input("Enter name: ")
            if name.lower() in book.data:
                birthday_input = input("Enter birthday (YYYY-MM-DD): ")
                try:
                    datetime.strptime(birthday_input, "%Y-%m-%d")
                    record = book.data[name.lower()]
                    record.birthday = Birthday(birthday_input)
                    print("Birthday added.")
                except ValueError:
                    print("Невірний формат дати народження. Введи YYYY-MM-DD")
            else:
                print("Контакт з таким іменем ще не доданий.")
        elif command.startswith("edit_phone"):
            try:
                name = input("Enter name: ")
                record = book.get(name)
                if record:
                    print(f"Current phone(s):")
                    phone_to_edit = input("Enter phone to edit: ")
                    new_phone = input("Enter new phone: ")
                    for phone in record.phones:
                        if phone.value == phone_to_edit:
                            phone.value = new_phone
                            print("Phone edited.")
                            break
                    else:
                        print("Телефон не знайдений.")
                else:
                    print(f"Contact '{name}' not found.")
            except Exception as e:
                print(f"Error: {e}")
        elif command == "edit_birthday":
            name = input("Enter name: ")
            if name.lower() in book.data:
                record = book.data[name.lower()]
                new_birthday = input("Enter new birthday (YYYY-MM-DD): ")
                record.edit_birthday(new_birthday)
            else:
                print("Контакт не знайдений.")
        elif command == "show all":
            for record in book.data.values():
                print(f"Name: {record.name.value}, Phone: {record.show_phones()}")
                if hasattr(record, 'birthday'):
                    print(f"Days to birthday: {record.days_to_birthday()} days")
                print("-" * 20)
        elif command == "search name":
            name_query = input("Enter name to search: ")
            search_results = book.search_by_name(name_query.lower())
            if search_results:
                print("Search results:")
                for result in search_results:
                    print(f"Name: {result.name.value}, Phone: {result.show_phones()}")
                    if hasattr(result, 'birthday'):
                        print(f"Days to birthday: {result.days_to_birthday()} days")
                    print("-" * 20)
            else:
                print("Контакт не знайдений.")
        elif command == "search phone":
            phone_query = input("Enter phone to search: ")
            search_results = book.search_by_phone(phone_query)
            if search_results:
                print("Search results:")
                for result in search_results:
                    print(f"Name: {result.name.value}, Phone: {result.show_phones()}")
                    if hasattr(result, 'birthday'):
                        print(f"Days to birthday: {result.days_to_birthday()} days")
                    print("-" * 20)
            else:
                print("Контакт не знайдений.")
        else:
            print("Невірна команда.")
